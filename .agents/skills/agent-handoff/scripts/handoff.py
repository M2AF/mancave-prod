#!/usr/bin/env python3
"""Shared Claude/Codex handoff board + journal. Stdlib only, Python 3.8+.

Files (same directory):
  HANDOFF.md          board: live state, rewritten in place, read first
  HANDOFF_LOG.md      journal: append-only, newest entry at the bottom
  HANDOFF_ARCHIVE.md  rotated journal entries

Commands:
  status  [-n N]                          board + live git drift + lease + last N entries
  claim   AGENT TASK [--hours H] [--force]
  log     AGENT KIND [-m LINE]... [--verified RESULT] [--next TEXT]   (`-m -` reads stdin)
  release AGENT [--next TEXT] [-m LINE]...
  rotate  [--keep N]
  init    [--project NAME] [--repo PATH] [--verify CMD] [--adopt]

Directory: --dir, else $HANDOFF_DIR, else nearest HANDOFF.md / research/HANDOFF.md
walking up from the current directory.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import os
import re
import subprocess
import sys
import time
import scoped_leases
from pathlib import Path

BOARD, JOURNAL, ARCHIVE, LOCK = "HANDOFF.md", "HANDOFF_LOG.md", "HANDOFF_ARCHIVE.md", ".handoff.lock"
FIELDS = ["owner", "task", "lease_until", "repo", "verify", "verified", "head", "updated", "resources"]
KINDS = {"claim", "checkpoint", "handoff", "release", "correction", "note", "verify"}
FIELD_RE = re.compile(r"^([a-z_]+):[ \t]*(.*)$")
ENTRY_RE = re.compile(r"^### \d{4}-\d\d-\d\dT\d\d:\d\d")
NONE_OWNERS = {"", "-", "none"}

BOARD_TEMPLATE = """# Handoff board — {project}
<!-- handoff v1. LIVE STATE ONLY: rewrite in place, keep under ~60 lines.
     History goes in HANDOFF_LOG.md. Machine fields above the first ## are managed by handoff.py. -->

owner: none
task: -
lease_until: -
repo: {repo}
verify: {verify}
verified: -
head: -
updated: {now}

## Now
- Nothing in flight.

## Next
- (exact next action, specific enough to start without asking)

## Traps
- (durable gotchas; delete a line only when it is resolved)

## Skills
- (task/trigger -> exact skill name; why it helped; source and verified runtime paths)

## Pointers
- (paths to evidence, specs, state docs; never paste large artifacts here)
"""

JOURNAL_TEMPLATE = """# Handoff journal — {project}
<!-- Append-only. Never edit or delete entries; correct with a new `correction` entry.
     Header: ### <iso-time> · <agent> · <kind> · <head> <clean|dirty N>. Use handoff.py log. -->
"""


def now() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="minutes")


def find_dir(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    if os.environ.get("HANDOFF_DIR"):
        return Path(os.environ["HANDOFF_DIR"]).resolve()
    cur = Path.cwd().resolve()
    for d in [cur, *cur.parents]:
        for cand in (d, d / "research"):
            if (cand / BOARD).exists():
                return cand
    sys.exit(f"handoff: no {BOARD} found from {cur}; pass --dir or run `init`.")


@contextlib.contextmanager
def locked(d: Path, timeout: float = 15.0):
    lock = d / LOCK
    deadline = time.monotonic() + timeout
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"{os.getpid()} {now()}".encode())
            os.close(fd)
            break
        except FileExistsError:
            # Break locks older than 2 minutes (crashed writer).
            with contextlib.suppress(OSError):
                if time.time() - lock.stat().st_mtime > 120:
                    lock.unlink()
                    continue
            if time.monotonic() > deadline:
                sys.exit(f"handoff: {lock} held by another writer; retry shortly.")
            time.sleep(0.25)
    try:
        yield
    finally:
        with contextlib.suppress(OSError):
            lock.unlink()


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def write_atomic(p: Path, text: str) -> None:
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, p)


def parse_board(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        m = FIELD_RE.match(line)
        if m and m.group(1) in FIELDS:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def set_fields(text: str, updates: dict[str, str]) -> str:
    lines = text.splitlines()
    seen = set()
    first_section = next((i for i, l in enumerate(lines) if l.startswith("## ")), len(lines))
    for i in range(first_section):
        m = FIELD_RE.match(lines[i])
        if m and m.group(1) in updates:
            lines[i] = f"{m.group(1)}: {updates[m.group(1)]}"
            seen.add(m.group(1))
    missing = [f"{k}: {v}" for k, v in updates.items() if k not in seen]
    if missing:
        lines[first_section:first_section] = missing + [""]
    return "\n".join(lines) + "\n"


def set_section(text: str, name: str, body: str) -> str:
    """Replace the body of `## name` (created at end if absent)."""
    pat = re.compile(rf"(^## {re.escape(name)}[ \t]*\n)(.*?)(?=^## |\Z)", re.S | re.M)
    new_body = "".join(f"- {l}\n" for l in body.splitlines() if l.strip()) + "\n"
    if pat.search(text):
        return pat.sub(lambda m: m.group(1) + new_body, text, count=1)
    return text.rstrip("\n") + f"\n\n## {name}\n{new_body}"


def git_state(d: Path, repo: str) -> tuple[str, str] | None:
    if not repo or repo == "-":
        return None
    root = (d / repo).resolve()
    try:
        head = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, timeout=20)
        if head.returncode:
            return None
        branch = subprocess.run(["git", "-C", str(root), "branch", "--show-current"],
                                capture_output=True, text=True, timeout=20).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "-uno"],
                               capture_output=True, text=True, timeout=60).stdout.splitlines()
    except (OSError, subprocess.TimeoutExpired):
        return None
    state = "clean" if not dirty else f"dirty {len(dirty)}"
    return f"{head.stdout.strip()}", f"({branch or 'detached'}) {state}"


def head_label(d: Path, fields: dict[str, str]) -> str:
    g = git_state(d, fields.get("repo", ""))
    return f"{g[0]} {g[1]}" if g else "no-git"


def lease_status(fields: dict[str, str]) -> tuple[str, bool]:
    owner = fields.get("owner", "").lower()
    if owner in NONE_OWNERS:
        return "free", False
    until = fields.get("lease_until", "-")
    try:
        exp = dt.datetime.fromisoformat(until)
    except ValueError:
        return f"held by {owner} (no expiry)", True
    remaining = exp - dt.datetime.now().astimezone()
    if remaining.total_seconds() <= 0:
        return f"STALE: {owner}'s lease expired {until}", False
    return f"held by {owner} for {int(remaining.total_seconds() // 60)} more min", True


def entries(journal: str) -> tuple[str, list[str]]:
    """Split journal into (preamble, [entry, ...]) on ### <iso-time> headers."""
    lines = journal.splitlines(keepends=True)
    idx = [i for i, l in enumerate(lines) if ENTRY_RE.match(l)]
    if not idx:
        return journal, []
    pre = "".join(lines[: idx[0]])
    out = ["".join(lines[a:b]) for a, b in zip(idx, idx[1:] + [len(lines)])]
    return pre, out


def append_entry(d: Path, agent: str, kind: str, body: list[str], fields: dict[str, str]) -> str:
    header = f"### {now()} · {agent} · {kind} · {head_label(d, fields)}"
    lines = [l.strip() for l in body if l.strip()]
    text = header + "\n" + "".join(f"- {l.lstrip('- ').rstrip()}\n" for l in lines)
    jp = d / JOURNAL
    cur = read(jp)
    sep = "" if not cur or cur.endswith("\n\n") else ("\n" if cur.endswith("\n") else "\n\n")
    with jp.open("a", encoding="utf-8", newline="\n") as f:
        f.write(sep + text)
    return header


def body_lines(m: list[str]) -> list[str]:
    """-m lines; a literal `-m -` splices stdin in (opt-in so tool calls never block)."""
    out: list[str] = []
    for line in m:
        out.extend(sys.stdin.read().splitlines() if line == "-" else [line])
    return out


# ---------------------------------------------------------------- commands

def cmd_status(d: Path, a) -> int:
    board = read(d / BOARD)
    fields = parse_board(board)
    print(board.rstrip())
    print("\n---- live checks")
    lease, _ = lease_status(fields)
    print(f"lease: {lease}")
    try:
        scoped_leases.display(d, sys.modules[__name__])
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    g = git_state(d, fields.get("repo", ""))
    if g:
        live = f"{g[0]} {g[1]}"
        recorded = fields.get("head", "-")
        drift = "" if recorded == live else f"  <-- DRIFT: board says {recorded}"
        print(f"git:   {live}{drift}")
        vhead = fields.get("verified", "-").split(" ")[0]
        if vhead not in ("-", g[0]):
            print(f"verify: recorded at {vhead}, HEAD is now {g[0]} -> re-verify before trusting it")
    pre, ents = entries(read(d / JOURNAL))
    print(f"journal: {len(ents)} entries" + ("  (run `rotate`)" if len(ents) > 60 else ""))
    if ents and a.n:
        print(f"\n---- last {min(a.n, len(ents))} journal entries")
        print("".join(ents[-a.n:]).rstrip())
    return 0


def cmd_claim(d: Path, a) -> int:
    with locked(d):
        board = read(d / BOARD)
        fields = parse_board(board)
        try:
            scoped_leases.check_main_claim(d, a.task, sys.modules[__name__], a.resource)
        except ValueError as exc:
            print(f"handoff: refused: {exc}", file=sys.stderr)
            return 2
        lease, held = lease_status(fields)
        owner = fields.get("owner", "").lower()
        if held and owner != a.agent and not a.force:
            print(f"handoff: refused, {lease}. Coordinate via the user or pass --force.", file=sys.stderr)
            return 2
        until = (dt.datetime.now().astimezone() + dt.timedelta(hours=a.hours)).isoformat(timespec="minutes")
        head = head_label(d, fields)
        board = set_fields(board, {"owner": a.agent, "task": a.task, "lease_until": until,
                                   "resources": scoped_leases.encode_resources(a.resource),
                                   "head": head, "updated": f"{now()} · {a.agent}"})
        write_atomic(d / BOARD, board)
        note = [f"task: {a.task}", f"lease until {until}"]
        if held and owner != a.agent:
            note.append(f"FORCED over {lease}")
        print(append_entry(d, a.agent, "claim", note + body_lines(a.m), fields))
    return 0


def cmd_log(d: Path, a) -> int:
    body = body_lines(a.m)
    if not body and not a.verified:
        sys.exit("handoff: empty entry; pass -m lines or pipe a body.")
    with locked(d):
        board = read(d / BOARD)
        fields = parse_board(board)
        head = head_label(d, fields)
        updates = {"head": head, "updated": f"{now()} · {a.agent}"}
        if a.verified:
            updates["verified"] = f"{head.split(' ')[0]} · {a.verified} · {now()}"
            body = [f"verified: {a.verified}"] + body
        if fields.get("owner", "").lower() == a.agent:  # every owner entry is a heartbeat
            updates["lease_until"] = (dt.datetime.now().astimezone()
                                      + dt.timedelta(hours=a.hours)).isoformat(timespec="minutes")
        board = set_fields(board, updates)
        if a.next:
            board = set_section(board, "Next", a.next)
            body.append(f"next: {a.next}")
        write_atomic(d / BOARD, board)
        print(append_entry(d, a.agent, a.kind, body, fields))
    return 0


def cmd_release(d: Path, a) -> int:
    with locked(d):
        board = read(d / BOARD)
        fields = parse_board(board)
        owner = fields.get("owner", "").lower()
        if owner not in NONE_OWNERS and owner != a.agent and not a.force:
            print(f"handoff: refused, owner is {owner}. Pass --force if the user confirmed.", file=sys.stderr)
            return 2
        board = set_fields(board, {"owner": "none", "task": "-", "lease_until": "-",
                                   "head": head_label(d, fields), "updated": f"{now()} · {a.agent}"})
        body = body_lines(a.m)
        if a.next:
            board = set_section(board, "Next", a.next)
            body.append(f"next: {a.next}")
        write_atomic(d / BOARD, board)
        print(append_entry(d, a.agent, "handoff", body or ["released, see board"], fields))
    return 0


def cmd_rotate(d: Path, a) -> int:
    with locked(d):
        pre, ents = entries(read(d / JOURNAL))
        if len(ents) <= a.keep:
            print(f"handoff: {len(ents)} entries <= keep {a.keep}; nothing to rotate.")
            return 0
        old, keep = ents[: -a.keep], ents[-a.keep:]
        ap = d / ARCHIVE
        arch = read(ap) or "# Handoff archive (rotated journal entries, oldest first)\n\n"
        write_atomic(ap, arch.rstrip("\n") + "\n\n" + "".join(old).rstrip("\n") + "\n")
        write_atomic(d / JOURNAL, pre.rstrip("\n") + "\n\n" + "".join(keep).rstrip("\n") + "\n")
        print(f"handoff: moved {len(old)} entries to {ARCHIVE}; kept {len(keep)}.")
    return 0


def cmd_init(d: Path, a) -> int:
    d.mkdir(parents=True, exist_ok=True)
    bp, jp = d / BOARD, d / JOURNAL
    if bp.exists():
        sys.exit(f"handoff: {bp} already exists; not overwriting.")
    project = a.project or (d.parent.name if d.name == "research" else d.name)
    if jp.exists():
        if not a.adopt:
            sys.exit(f"handoff: {jp} exists. Re-run with --adopt to archive it (renamed, not deleted).")
        legacy = d / "HANDOFF_LOG.legacy.md"
        n = 1
        while legacy.exists():
            n += 1
            legacy = d / f"HANDOFF_LOG.legacy{n}.md"
        os.replace(jp, legacy)
        print(f"handoff: archived existing journal as {legacy.name}")
    write_atomic(bp, BOARD_TEMPLATE.format(project=project, repo=a.repo or "-",
                                           verify=a.verify or "-", now=now()))
    write_atomic(jp, JOURNAL_TEMPLATE.format(project=project))
    print(f"handoff: created {bp} and {jp}. Fill ## Now/Next/Traps/Skills/Pointers, then `log`.")
    return 0


def main(argv: list[str] | None = None) -> int:
    with contextlib.suppress(AttributeError):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Claude/Codex shared handoff board + journal")
    p.add_argument("--dir", help="directory holding HANDOFF.md")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status"); s.add_argument("-n", type=int, default=3)
    s = sub.add_parser("claim"); s.add_argument("agent"); s.add_argument("task")
    s.add_argument("--resource", action="append", default=[], help="logical main-checkout scope; repeat for shared resources")
    s.add_argument("--hours", type=float, default=3.0); s.add_argument("--force", action="store_true")
    s.add_argument("-m", action="append", default=[])
    s = sub.add_parser("log"); s.add_argument("agent"); s.add_argument("kind", choices=sorted(KINDS))
    s.add_argument("-m", action="append", default=[]); s.add_argument("--verified"); s.add_argument("--next")
    s.add_argument("--hours", type=float, default=3.0, help="lease renewal if you are the owner")
    s = sub.add_parser("release"); s.add_argument("agent"); s.add_argument("--next")
    s.add_argument("-m", action="append", default=[]); s.add_argument("--force", action="store_true")
    s = sub.add_parser("rotate"); s.add_argument("--keep", type=int, default=30)
    s = sub.add_parser("init"); s.add_argument("--project"); s.add_argument("--repo")
    s.add_argument("--verify"); s.add_argument("--adopt", action="store_true")
    scoped_leases.configure(sub)

    a = p.parse_args(argv)
    if hasattr(a, "agent"):
        a.agent = a.agent.lower()
    if a.cmd == "init":
        d = Path(a.dir or os.environ.get("HANDOFF_DIR") or ".").resolve()
    else:
        d = find_dir(a.dir)
    if a.cmd.startswith("lease-") or a.cmd == "leases":
        return scoped_leases.run(d, a, sys.modules[__name__])
    return {"status": cmd_status, "claim": cmd_claim, "log": cmd_log, "release": cmd_release,
            "rotate": cmd_rotate, "init": cmd_init}[a.cmd](d, a)


if __name__ == "__main__":
    sys.exit(main())
