---
name: agent-handoff
description: Shared Claude and Codex handoff protocol using a live state board (HANDOFF.md), an append-only journal (HANDOFF_LOG.md) and a lease, so either agent can resume an ongoing project exactly where the other stopped. Use at the start of any session on a project that has HANDOFF.md, before stopping or context compaction, after each milestone, before long-running jobs, and immediately when the user mentions low credits, usage limits, switching agents, or a handoff.
---

# Agent Handoff (Claude and Codex)

Both agents follow this same skill. Credits can run out without warning, so the other
agent must be able to resume from the files alone, without asking the user.

## Model: board + journal + lease

| File | Role | Rule |
|---|---|---|
| `HANDOFF.md` | **Board.** The live state, and the only thing a fresh session must read | Rewrite in place. Under ~60 lines. Only the present tense |
| `HANDOFF_LOG.md` | **Journal.** History of what happened and why | Append-only through the script. Never edit old entries |
| `HANDOFF_ARCHIVE.md` | Rotated old journal entries | Read only when digging into history |

The **lease** (`owner` and `lease_until` on the board) says who is actively working.
The board owner changes the main checkout. An expired lease is stale, and the other agent may claim it.
For independent work in separate checkouts, use the scoped leases below; another
agent's main lease does not prohibit a successfully claimed disjoint worktree.

All writes go through `scripts/handoff.py` in this skill's directory (stdlib Python 3.8+).
The script stamps time, agent, git HEAD and dirty state, locks against concurrent writes,
and keeps the format identical for both agents. Below, `H` means
`python <this-skill-dir>/scripts/handoff.py` (add `--dir <folder>` if not discoverable).

## 1. Session start (receiver)

1. Run `H status`. It prints the board, the live git drift, the lease state and the last 3 entries.
   Do not read the whole journal.
2. If the main lease is held by the other agent, preserve that checkout and board.
   Work elsewhere only after claiming a disjoint scoped lease in an isolated
   checkout. A rejected claim needs coordination or another independent task.
3. Reconcile: if `status` shows DRIFT or a `verified` HEAD different from the live one, run the
   board's `verify` command before trusting the recorded state.
4. Claim the task: `H claim <claude|codex> "<task>" [--hours 3]`.
5. Read `## Skills` and load the skills relevant to the current task before doing that work.
   Resolve them in your own runtime as described below; a recorded path alone is not enough.
6. If the verification was re-run: `H log <agent> verify --verified "<result summary>"`.

## 2. While working

### Parallel work: scoped leases

`HANDOFF_LEASES.json` is an additive, script-managed resource ledger. The old board
and commands remain the main lease. `H status` shows both. Example:

```text
H lease-claim codex codex-purin "Purin special_hi" --repo ../brawl-codex-parallel --resource fighter/ft_purin
H lease-log codex codex-purin -m "boundary proven" --next "draft source"
H lease-release codex codex-purin -m "commit ready" --next "integrator reverify"
```

Each claim owns its physical checkout plus declared logical resources. Use
`fighter/ft_donkey`, `shared/include/ft/header.h`, or another stable hierarchy;
parents conflict with children. Same-fighter work conflicts even in different
trees. Shared-resource changes need their own declared resource. Unknown main
tasks are conservatively project-wide; main claims can use repeatable
`--resource` to declare scope. Legacy Brawl tasks naming one `ft_*` infer that
fighter, while integration/autopilot tasks are always exclusive.

Claims, heartbeats and releases use the same file lock as the journal; conflicting
or corrupt records fail closed. A heartbeat cannot revive an expired lease; claim
again and check conflicts. Scoped log/release never rewrite the main board or its
Next/verified fields. Only the main owner edits PROJECT_STATE and board sections;
parallel agents maintain their own pickup files and use scoped journal commands.

Use separate branches, builds and private evidence paths. Local commits in the
worktree are independent; do not merge/rebase onto the live main tree. Before
integration, release all parallel claims, then claim main with a task containing
`integration` (or `--resource integration`). `H leases --require-integration`
must succeed before merging. This exclusive claim blocks new parallel claims.
Do not use `--force` to bypass a resource collision; it overrides only the legacy
owner and still respects active scoped leases. The lease system coordinates
cooperating agents; it does not sandbox filesystem writes.

Log **early and small**. A cutoff loses everything after the last entry.

`H log <agent> checkpoint -m "<fact>" -m "<fact>" [--verified "<result>"] [--next "<action>"]`

Log at these moments:
- after each milestone: a commit, a passing verification, an accepted unit of work
- **before** starting any long build, test run or search job, naming the process and its log path
- when an approach fails and the failure is worth not repeating (that goes under Traps too)
- immediately when the user mentions low credits, limits, or switching agents

Each owner entry renews the lease (`--hours`, default 3).

Also **edit the board's sections directly** whenever they change, keeping them true *now*:
- `## Now`: what is in flight, including dirty files, running processes and partial results.
- `## Next`: the exact next action, concrete enough to start without asking.
- `## Traps`: durable gotchas. Remove a line only when it is resolved.
- `## Pointers`: paths to evidence, specs and state docs.
- `## Skills`: task-to-skill mappings that help the next agent choose and load the right skills.

Leave the machine fields above the first `##` to the script.

## 3. Stopping or handing off

1. Update `## Now`, `## Next`, `## Traps` and `## Skills` on the board.
2. `H release <agent> -m "<state summary>" --next "<exact next action>"`.
   This frees the lease and writes a `handoff` entry.
3. If work must stay claimed (a job still running), use `log ... handoff` instead of `release`,
   and state in `## Now` what is running and how to check it.

## Skills that help with the task

Maintain a compact `## Skills` section on the board so any receiving model can find
and use the skills that helped, even when its skill catalog or installation paths differ.

- Record the exact skill name, the task or trigger it applies to, and the concrete reason
  it helped (for example a reliable workflow, validation gate or tool choice). Distinguish
  skills actually used successfully from suggestions that have not been tried.
- Include a portable locator: package/plugin name or source link when known, plus the
  local `SKILL.md` paths for Claude and Codex when verified. Mark unknown paths as unknown;
  do not assume that a path or installation on one runtime exists on another.
- The receiver matches the name and purpose against its available skill catalog, resolves
  its own installation or provider, and reads the relevant `SKILL.md` before applying it.
  Follow its referenced resources as needed and the current user/runtime instructions.
  A handoff recommendation does not grant tool access, permissions or new authorization.
- If a recommended skill is missing, search the local catalog or recorded source. State
  the gap and use the best available equivalent or documented fallback. If the task
  explicitly requires that skill and cannot proceed without it, report the blocker.
- Update mappings after a skill proves useful or unsuitable. Keep only current mappings
  on the board, log meaningful discoveries with `H log`, and put longer rationale in a
  project document linked from `## Skills`. Avoid copying whole skills into the board.
- For existing boards, the lease owner adds `## Skills` during the next authorized board
  update; do not reinitialize or migrate the project just to add this section.

Compact entry format:
`- <task/trigger> -> <exact skill name> | used: <what helped> (or suggested: <why>) | source: <package/link> | Claude: <path/unknown> | Codex: <path/unknown>`

## Entry content rules

- Facts, not narrative. One line per fact. Record what *was verified*, the exact command
  and what it covers. Never claim more than the evidence shows.
- Include evidence paths, not evidence. Never paste large artifacts, secrets or private
  material (for example target disassembly) into either file.
- Kinds: `claim`, `checkpoint`, `verify`, `handoff`, `correction`, `note`.
  Fix a wrong entry with a new `correction` entry. Never edit the old one.
- Run `H rotate` when `status` reports more than 60 entries (keeps the last 30).

## Setup or migration

- New project: `H init --dir <folder> --repo <path-to-git-repo-relative-to-folder> --verify "<command>"`.
- Existing free-form log: add `--adopt`. The old `HANDOFF_LOG.md` is renamed to
  `HANDOFF_LOG.legacy.md` (never deleted). Then hand-fill the board from it and add a pointer to the legacy file.
- Project-specific rules (acceptance gates, privacy, which state docs to sync) go on the
  board under `## Traps` / `## Pointers`, so both agents see them on every start.

See `references/protocol.md` for field definitions, examples and the reasoning behind each rule.
