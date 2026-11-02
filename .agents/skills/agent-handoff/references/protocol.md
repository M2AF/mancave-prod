# Handoff protocol reference

## Why board + journal instead of one log

A single log makes the reader find the live state. If the file is append-only, the state is
spread across many entries. If one top section gets rewritten, it goes stale the first time
someone forgets to update it, and both conventions end up mixed in the same file. Splitting
them fixes this:

- **Board** = state (overwrite). Reading it costs roughly the same however long the project runs.
- **Journal** = events (append). It gives an audit trail and shows *why* the state is what it is.
- **Lease** = ownership. It prevents two agents editing the same tree at once.

## Board machine fields (managed by the script)

| Field | Meaning |
|---|---|
| `owner` | `claude`, `codex` or `none` |
| `task` | the claimed unit of work, short |
| `lease_until` | ISO time. After it passes, the lease is STALE and may be claimed |
| `repo` | git repo path relative to the board's folder (`-` if none). Used for HEAD and drift checks |
| `verify` | the command whose output proves the project state |
| `verified` | `<head> · <result> · <time>` from the last `--verified`. Stale if the HEAD differs |
| `head` | `<sha> (<branch>) clean\|dirty N` at the last write |
| `updated` | `<time> · <agent>` of the last write |

You may hand-edit `repo` and `verify`. Leave the other fields to the script.

## Journal entry format

```
### 2026-10-01T01:53-03:00 · codex · checkpoint · b284006 (rsbe01_01-support) clean
- verified: OK 127/127
- recovered class stDxYorster, alloc size 0x250
- evidence: evidence/nonmatching/dxyorster/ranking.txt
- next: recover RTTI/data ownership, then draft splits
```

The header is generated, and `rotate` and `status` rely on the `### <iso-time>` prefix.

## Good versus bad entries

Bad: `- Worked on the stage, mostly matching now, will continue.`

Good:
```
- 27/29 functions match; setupAttack and setSoundInfo differ (stack slot for Vec2f temp)
- tried explicit Vec2f args: worse (logged in Traps)
- running: ninja full rebuild, log build/full.log, started 02:10, ~6 min
- next: if 127/127, promote MatchingFor + allowlist, then log verify
```

## Commands

```
H status [-n N]
H claim AGENT TASK [--hours H] [--force] [-m LINE]...
H claim AGENT TASK --resource fighter/ft_donkey
H lease-claim AGENT ID TASK --repo PATH --resource RESOURCE [--resource RESOURCE] [--hours H]
H lease-log AGENT ID [-m LINE]... [--verified RESULT] [--next TEXT] [--hours H]
H lease-release AGENT ID [-m LINE]... [--next TEXT]
H leases [--require-clear | --require-integration]
H log AGENT KIND [-m LINE]... [--verified RESULT] [--next TEXT] [--hours H]
H release AGENT [--next TEXT] [-m LINE]... [--force]
H rotate [--keep 30]
H init [--dir D] [--project NAME] [--repo PATH] [--verify CMD] [--adopt]
```

- `-m -` splices stdin into the body (for long multi-line entries via heredoc).
- `--next` replaces the board's `## Next` section and echoes it into the entry.
- Exit code 2 means refused (lease held by the other agent, or a release by a non-owner).
  Only use `--force` after the user confirms the other agent is not working.
- Writes are serialized with `.handoff.lock`. A lock older than 2 minutes is treated as crashed and broken.
- Parallel records live in HANDOFF_LEASES.json, version 1. Each record has ID,
  owner, task, absolute checkout, resources, expiry, updated time and scoped
  verification. Checkout ownership is implicit; hierarchical logical resources
  are explicit. Expired records are shown but stop blocking new claims.
- A held legacy main lease reserves its checkout and declared scope, or one
  inferred Brawl fighter. Unknown scopes reserve the project; integration is
  exclusive across all resources. Legacy main claim checks parallel conflicts.
- Scoped mutations append worktree-stamped journal entries under the same lock
  and leave HANDOFF.md unchanged. --next/--verified refer only to that record.
- --require-clear tests only active parallel records. --require-integration also
  requires a live main integration lease, preventing a check-then-merge race
  with a newly arriving parallel agent. The integrator retains that lease until
  all merges and verification finish.

## Directory discovery

The script looks in this order: `--dir`, then `$HANDOFF_DIR`, then the nearest `HANDOFF.md` or
`research/HANDOFF.md` walking up from the current directory.

## Portable skill mappings

`## Skills` is live board state, maintained by the lease owner like Now/Next/Traps.
Use task-specific mappings with the exact skill name, observed benefit (or a clear
untried suggestion), source/package, and verified runtime locations. The receiver
loads the relevant skill through its own catalog or provider before using it.

Example (paths must be checked on the current machine):
```
## Skills
- Shared-agent resumption -> agent-handoff | used: lease and drift checks | source: local skill | Claude: C:/Users/balla/.claude/skills/agent-handoff/SKILL.md | Codex: C:/Users/balla/.codex/skills/agent-handoff/SKILL.md
```

Keep the board under ~60 lines. If mappings need detail, link a project document
from this section. Existing boards need only an owner-authored section addition;
`claim`, `log` and `release` preserve custom sections without reinitialization.
