"""Additive resource leases; the existing board remains the main-checkout lease."""
import datetime as dt
import json
import math
import os
from pathlib import Path
import re

FILE = "HANDOFF_LEASES.json"


def active(record):
    try:
        expiry = dt.datetime.fromisoformat(record["lease_until"])
        if expiry.tzinfo is None:
            raise ValueError("Lease expiry needs a timezone")
        return expiry > dt.datetime.now().astimezone()
    except (KeyError, TypeError, ValueError):
        raise ValueError("Invalid lease expiry; inspect ledger rather than bypassing it")


def load(d):
    path = d / FILE
    if not path.exists():
        return {"version": 1, "leases": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        if state["version"] != 1 or not isinstance(state["leases"], dict):
            raise ValueError()
        for key, record in state["leases"].items():
            if record["id"] != key or not isinstance(record["resources"], list) or not record["resources"]:
                raise ValueError()
            if not record["owner"] or not record["repo"] or not record["task"]:
                raise ValueError()
            for resource in record["resources"]:
                normalize(resource)
            active(record)
        return state
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid {path}; no claims allowed until repaired") from exc


def normalize(resource):
    if not isinstance(resource, str):
        raise ValueError("Resource names must be strings")
    resource = resource.strip().replace("\\", "/").casefold().rstrip("/")
    if not resource or any(part in ("", ".", "..") for part in resource.split("/")):
        raise ValueError(f"Invalid resource: {resource!r}")
    return resource


def checkout_resource(repo):
    # Separate physical worktrees always own distinct checkout resources.
    path = os.path.normcase(str(Path(repo).resolve())).replace("\\", "/")
    return "checkout/" + path.lstrip("/").casefold()


def overlaps(left, right):
    if left in ("project", "integration") or right in ("project", "integration"):
        return True
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def encode_resources(resources):
    return json.dumps(sorted({normalize(x) for x in resources})) if resources else "-"


def legacy(d, h, task=None, declared=None):
    fields = h.parse_board(h.read(d / h.BOARD))
    if task is None and not h.lease_status(fields)[1]:
        return None
    text = task if task is not None else fields.get("task", "")
    fighters = set(re.findall(r"\bft_[a-z0-9]+", text.casefold()))
    # Unknown main task is conservatively project-wide. Integration is global.
    resources = ["fighter/" + next(iter(fighters))] if len(fighters) == 1 else ["project"]
    if declared:
        resources = [normalize(x) for x in declared]
    elif task is None and fields.get("resources", "-") != "-":
        try:
            declared = json.loads(fields["resources"])
            if not isinstance(declared, list) or not declared:
                raise ValueError()
            resources = [normalize(x) for x in declared]
        except (ValueError, TypeError):
            raise ValueError("Invalid main resources; repair the board before claiming")
    if re.search(r"\b(integrat\w*|autopilot|rebase|merge)\b", text, re.I):
        resources = ["integration"]
    repo = (d / fields.get("repo", ".")).resolve()
    return {"id": "legacy-main", "owner": fields.get("owner", "none"), "task": text,
            "repo": str(repo), "resources": resources + [checkout_resource(repo)],
            "lease_until": fields.get("lease_until", "-")}


def check(resources, records):
    for record in records:
        collisions = [(a, b) for a in resources for b in record["resources"] if overlaps(a, b)]
        if collisions:
            raise ValueError(f"Conflicts with {record['id']} ({record['owner']}): {collisions}")


def check_main_claim(d, task, h, resources=None):
    prospective = legacy(d, h, task, resources)
    check(prospective["resources"], [r for r in load(d)["leases"].values() if active(r)])


def expiry(hours):
    if not math.isfinite(hours) or not 0 < hours <= 24:
        raise ValueError("Lease duration must be greater than zero and at most 24 hours")
    return (dt.datetime.now().astimezone() + dt.timedelta(hours=hours)).isoformat(timespec="minutes")


def configure(sub):
    p = sub.add_parser("leases", help="show parallel resource leases plus legacy main")
    p.add_argument("--require-clear", action="store_true", help="fail if any parallel lease is active (integration gate)")
    p.add_argument("--require-integration", action="store_true", help="require a live exclusive integration main lease")
    p = sub.add_parser("lease-claim", help="claim a resource in an isolated checkout")
    p.add_argument("agent"); p.add_argument("id"); p.add_argument("task")
    p.add_argument("--repo", required=True); p.add_argument("--resource", action="append", required=True)
    p.add_argument("--hours", type=float, default=3)
    for command in ("lease-log", "lease-release"):
        p = sub.add_parser(command)
        p.add_argument("agent"); p.add_argument("id")
        p.add_argument("-m", action="append", default=[])
        p.add_argument("--next")
        if command == "lease-log":
            p.add_argument("--hours", type=float, default=3)
            p.add_argument("--verified")


def display(d, h):
    state = load(d)
    current = legacy(d, h)
    records = ([current] if current else []) + list(state["leases"].values())
    print("\n---- resource leases")
    for record in records:
        live = True if record["id"] == "legacy-main" else active(record)
        print(f"{record['id']}: {record['owner']} | {'active' if live else 'expired'} | {record['task']} | "
              f"{', '.join(record['resources'])} | until {record['lease_until']}")
    if not records:
        print("none")
    return state


def run(d, a, h):
    try:
        with h.locked(d):
            if a.cmd == "leases":
                state = display(d, h)
                parallel = any(active(r) for r in state["leases"].values())
                if a.require_integration:
                    main = legacy(d, h)
                    return 0 if not parallel and main and "integration" in main["resources"] else 2
                return 2 if a.require_clear and parallel else 0
            state = load(d)
            existing = state["leases"].get(a.id)
            if not re.fullmatch(r"[a-zA-Z0-9_-]+", a.id) or a.id == "legacy-main":
                raise ValueError("Use a unique simple lease ID (legacy-main is reserved)")
            if a.cmd == "lease-claim":
                repo = (d / a.repo).resolve()
                if not repo.is_dir() or h.git_state(d, str(repo)) is None:
                    raise ValueError("Lease --repo must be an existing Git checkout")
                resources = sorted({normalize(x) for x in a.resource} | {checkout_resource(repo)})
                if existing and active(existing):
                    if existing["owner"] != a.agent or existing["repo"] != str(repo) or existing["task"] != a.task or existing["resources"] != resources:
                        raise ValueError("Active lease ID cannot be replaced; release it first")
                peers = [r for key, r in state["leases"].items() if key != a.id and active(r)]
                main = legacy(d, h)
                check(resources, peers + ([main] if main else []))
                record = {"id": a.id, "owner": a.agent, "task": a.task, "repo": str(repo),
                          "resources": resources, "lease_until": expiry(a.hours), "updated": h.now(),
                          "verified": existing.get("verified", "-") if existing and active(existing) else "-"}
                state["leases"][a.id] = record
                body = [f"scoped lease {a.id}: {a.task}", f"resources: {', '.join(resources)}", f"until: {record['lease_until']}"]
                kind = "claim"
            else:
                if not existing or existing["owner"] != a.agent:
                    raise ValueError("Only this scoped lease's owner may log or release it")
                record = existing
                body = h.body_lines(a.m)
                kind = "handoff" if a.cmd == "lease-release" else "checkpoint"
                if a.cmd == "lease-log":
                    if not active(record):
                        raise ValueError("Expired lease: claim again and check conflicts before continuing")
                    peers = [r for key, r in state["leases"].items() if key != a.id and active(r)]
                    main = legacy(d, h)
                    check(record["resources"], peers + ([main] if main else []))
                    record["lease_until"] = expiry(a.hours)
                    if a.verified:
                        record["verified"] = f"{h.head_label(d, record)} | {a.verified} | {h.now()}"
                        body.insert(0, "verified: " + record["verified"])
                    record["updated"] = h.now()
                else:
                    del state["leases"][a.id]
                if a.next:
                    record["next"] = a.next
                    body.append("next: " + a.next)
                body.insert(0, "scoped lease: " + a.id)
            h.write_atomic(d / FILE, json.dumps(state, indent=2) + "\n")
            # Main board stays byte-for-byte unchanged; journal header uses this worktree.
            print(h.append_entry(d, a.agent, kind, body, record))
            return 0
    except ValueError as exc:
        print("handoff: refused: " + str(exc), file=h.sys.stderr)
        return 2
