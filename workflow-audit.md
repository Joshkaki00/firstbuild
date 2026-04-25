# Workflow Audit — task-cli / firstbuild

---

## 1. Context Management Audit

### What the course recommends (Memory Is Everything + House Rules)

| Recommendation | Status |
|---|---|
| Root `CLAUDE.md` under 100 lines | ✅ 97 lines |
| Pointers to files, not pasted snippets | ✅ References `spec.md`, `src/task_cli/store.py` by path |
| Layer context (global → project → subdirectory) | ⚠️ Partial — only project root layer exists |
| Hooks for enforcement (PreToolUse / PostToolUse) | ❌ No `settings.json`, no hooks configured |
| Custom commands encode workflows | ✅ `/test`, `/tdd`, `/qg`, `/verify` all exist |
| Linter config separate from CLAUDE.md | ❌ No `ruff.toml` or linter config — lint rules are advisory in CLAUDE.md |
| Global `~/.claude/CLAUDE.md` for personal preferences | ❌ Not set up |
| Subdirectory `CLAUDE.md` for module-specific rules | ❌ No `src/task_cli/CLAUDE.md` |

### What's missing

**Biggest gap — no hooks.** The course is explicit: "If something is critical, make it a hook." Right now nothing is enforced. The CLAUDE.md says "write tests first" and "don't commit to main" but both are advisory. A `PreToolUse` hook blocking commits without a passing test run, and a `PostToolUse` hook running the linter after every file edit, would enforce what currently only advises.

**Second gap — no linter config.** `ruff` or `flake8` should be in `pyproject.toml` with rules defined there, not in CLAUDE.md. The agent shouldn't need to be told "check for unused imports" — the linter should catch it automatically. The unused `pytest` import in `test_cli.py` was caught manually, not by tooling.

**Third gap — no subdirectory context.** A `src/task_cli/CLAUDE.md` scoped to the module layer (schema shape, the load→mutate→save pattern, `ValueError`/`KeyError` error contract) would mean that layer-specific rules don't pollute the root file.

### What I'd change

1. Add `settings.json` to `.claude/` with a PostToolUse hook: run `python3 -m py_compile` after every Edit.
2. Add `ruff` to `pyproject.toml` with `[tool.ruff]` config so style is enforced by tooling, not instruction.
3. Move the JSON schema detail and the `cmd_*` pattern description out of root `CLAUDE.md` into `src/task_cli/CLAUDE.md`.
4. Set up `~/.claude/CLAUDE.md` with personal preferences (Python 3.11+, pytest, functions over classes) so they don't have to repeat in every project.

---

## 2. Command and Feature Inventory

### Features used in firstbuild

| Feature | Used? | Where |
|---|---|---|
| `@` file mentions | ✅ | Referenced lesson files, README, CLAUDE.md during sessions |
| `/init` | ✅ | Used to bootstrap initial `CLAUDE.md` |
| Custom slash commands | ✅ | `/test`, `/tdd`, `/qg`, `/verify` in `.claude/commands/` |
| Plan Mode | ✅ | Used for V1.2 priority feature design |
| Agent Mode | ✅ | All implementation sessions |
| Ask Mode | ✅ | Analysis and review sessions |
| `CLAUDE.md` project context | ✅ | Root-level, updated iteratively |
| `spec.md` with quality gates | ✅ | 3 gates, 5 ACs, test mapping |
| Red/green/refactor TDD cycles | ✅ | 3 core features + 2 V1.2 features |
| Named agent lanes (domain/store/cli) | ✅ | V1.2 priority feature |
| Hallucination gotcha log | ✅ | In CLAUDE.md |
| Verification pipeline command | ✅ | `/verify` — 4 steps |
| Context7 MCP | ✅ | Added in Part 3 — live doc verification |

### Features from the course not yet used

| Feature | Lesson | Why not used yet |
|---|---|---|
| **Hooks** (PreToolUse / PostToolUse) | House Rules | No `settings.json` created |
| **`settings.json`** permissions config | House Rules | Never set up |
| **Subdirectory `CLAUDE.md`** | Memory Is Everything | Only root-level context used |
| **Global `~/.claude/CLAUDE.md`** | Memory Is Everything | Personal preferences not encoded |
| **Git worktrees** for parallel agents | Thirteen Tiny Coworkers | Simulated lanes in one session instead |
| **`gh` CLI integration** (issue → branch → PR loop) | Ticket to Merge | No GitHub issues created; committed directly |
| **Full ticket-to-merge loop** | Ticket to Merge | No issue creation, no PR workflow used |
| **Linter config** (`ruff.toml` / `pyproject.toml [tool.ruff]`) | House Rules | No linter installed or configured |
| **`/project:onboard` command** | House Rules | No onboarding command created |
| **Model selection** (Haiku / Sonnet / Opus) | Copilot ≠ Coworker | Default model used throughout |
| **Parallel subagents via Task tool** | Thirteen Tiny Coworkers | Lanes were sequential, not truly parallel |

---

## 3. Workflow Replay

### Task chosen: V1.2 — task priorities (multi-file feature)

**How I approached it:**
Named the work as three "agent lanes" (domain-agent, store-agent, cli-agent) and ran them sequentially in one session. Tests before implementation for each layer. Committed each red/green pair before moving to the next lane.

**How I'd approach it now, using course techniques:**

**Step 1 — Write the spec first (Words Before Code)**
Before opening a terminal, write `spec-priority.md` with the full Given/When/Then ACs for priority — including the edge cases (invalid priority, missing field on old tasks, `list_by_priority` returning all when filter is `None`). That spec would have caught the "old tasks missing priority field" edge case before the test gap analysis forced me to find it later.

**Step 2 — Create a GitHub issue**
Open an issue: "feat: add task priorities (high/medium/low)". This creates a traceable unit of work and lets Claude Code reference it during the full ticket-to-merge loop.

**Step 3 — Real parallel subagents with worktrees (Thirteen Tiny Coworkers)**
Instead of simulating lanes in one session, spawn three actual subagents:
- `domain-agent` on `feature/priority-domain` worktree → owns `tasks.py`
- `store-agent` on `feature/priority-store` worktree → owns `store.py` (verify only)
- `cli-agent` on `feature/priority-cli` worktree → owns `cli.py`

Each writes failing tests, commits, implements, commits. The orchestrator (main session) stays light — it only reviews and merges.

**Step 4 — Hooks enforce the gates**
A PostToolUse hook runs `pytest tests/` after every Edit. The agent can't move to the next step if tests are red. No manual "confirm tests are green before committing" — the hook makes it non-negotiable.

**Step 5 — Close the loop with `gh`**
After all lanes merge: `claude "Create a PR for the priority feature. Reference issue #1."` The agent reads the diff across all three files, writes the PR description, and links the issue. Human reviews the PR, not the raw diff.

**What would have been different:**
- The "old tasks missing priority field" edge case would have been caught by the spec, not discovered post-hoc in a test gap analysis.
- The coverage report confusion (0% on `cli.py`) would have been in the spec upfront as a known limitation, not discovered mid-session.

---

## 4. Part 3 — Apply One New Technique: Context7 MCP

### What I chose and why

**Context7 MCP** — an MCP server by Upstash that fetches live, version-specific library documentation and injects it directly into the agent's context during a session.

I chose this because it directly addresses the hallucination problem already documented in `CLAUDE.md`. Two of the four gotchas in the hallucination log (wrong build backend, `<placeholder>` shell syntax) came from the agent pattern-matching on stale training data instead of verifying against real docs. Context7 is the tooling solution to that problem.

### What I did

**Installation** — added Context7 scoped to the `firstbuild` project:

```bash
claude mcp add --scope project context7 -- npx -y @upstash/context7-mcp
```

This writes the MCP server config into `.mcp.json` at the project root so it loads automatically for this project without affecting other repos. No API key required for basic use; a free key from context7.com/dashboard unlocks higher rate limits.

Verified with:
```
$ claude mcp get context7
context7:
  Scope: Project config (shared via .mcp.json)
  Status: ✓ Connected
  Type: stdio
  Command: npx
  Args: -y @upstash/context7-mcp
```

Note: `claude mcp list` does not show project-scoped servers — known display bug ([issue #5963](https://github.com/anthropics/claude-code/issues/5963)). Use `claude mcp get <name>` or `jq -r '.mcpServers | keys[]' .mcp.json` to verify project servers are registered.

**Added a CLAUDE.md instruction** to trigger Context7 automatically on any library or API question:

> When referencing any stdlib module, third-party package, or CLI tool behavior, use context7 to pull current documentation before generating code or examples.

**Test query 1** — verified the exact call used in `tasks.py`:

```
Verify that datetime.date.fromisoformat accepts YYYY-MM-DD strings in Python 3.11
and confirm the correct exception type for invalid input. use context7
```

Context7 fetched the official Python 3.11 `datetime` docs, confirmed `fromisoformat` raises `ValueError` on bad input, and noted it was added in Python 3.7 — validating the implementation already in `tasks.py`.

**Test query 2** — checked `argparse` `choices` exit behavior (used for `--priority`):

```
Confirm that argparse choices validation raises SystemExit with code 2 on invalid input. use context7
```

Context7 confirmed: argparse prints to stderr and exits with code 2 for invalid choices — which is why `test_add_invalid_priority_exits_nonzero` passes (asserts `returncode != 0`, satisfied by exit code 2).

**Test query 3** — the hallucination that actually hurt this project:

```
What is the correct build-backend value for setuptools in pyproject.toml? use context7
```

Context7 fetched current setuptools docs and returned `setuptools.build_meta` — exactly the fix that had to be made manually after the agent hallucinated `setuptools.backends.legacy:build`. With Context7 installed, that mistake would have been caught before `pip install -e .` failed.

### What happened

Context7 resolved all three queries by fetching doc chunks from official sources, version-pinned to the libraries actually in use. For the two confirmatory queries (datetime, argparse) the implementation was already correct — but "I verified this is right" is a stronger claim than "I think this is right." For the setuptools query, Context7 gave the exact answer that would have prevented a real bug.

### Did it improve the workflow?

**For firstbuild (stdlib only): moderately.** The implementation didn't change, but verification became tool-backed instead of memory-backed. The hallucination log now has a procedural answer: "run `use context7` before accepting any package config or API call the agent generates."

**For future projects (third-party deps): significantly.** Every project that touches `requests`, `fastapi`, `sqlalchemy`, `pytest` plugins, or any rapidly-changing package benefits from live doc injection. Training data lags; Context7 doesn't.

**Workflow change going forward:** Added `use context7` as a standard step in the `/verify` command's Step 1 (import check) — before accepting any new import or package config, Context7 confirms the API exists in the version being used. This closes the gap between "the agent is confident" and "the docs agree."

---

## 5. Custom Command + Hook

### What was tedious

Every new feature required manually creating three test file stubs (domain, store, CLI layer) with identical boilerplate: same import block, same `run()` helper, same file header comment. The priority and due date features both needed this, and it was pure copy-paste work.

Before committing, there was also a 4-step mental checklist to remember: run tests, check syntax, verify CLAUDE.md line count, check store/tasks coverage. Missing any step meant discovering the problem later.

### `/scaffold <feature>` — new custom command

**File:** `.claude/commands/scaffold.md`

Generates all three test stub files for a new feature in one command:

```
/scaffold tags
```

Creates:
- `tests/test_tasks_tags.py` — domain layer stub with import and TODO
- `tests/test_store_tags.py` — store roundtrip stub with pattern comment
- `tests/test_cli_tags.py` — CLI layer stub with the full `run()` helper pre-filled

Then confirms they collect 0 tests (stubs only — correct at red phase start) and hands off to `/tdd`.

**What this eliminates:** The copy-paste setup tax before every feature's red phase. The `run()` helper alone is 10 lines that previously had to be manually duplicated into every CLI test file.

### PostToolUse syntax-check hook

**File:** `.claude/settings.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -m py_compile \"$CLAUDE_TOOL_INPUT_PATH\" ..."
          }
        ]
      }
    ]
  }
}
```

After every `Write` or `Edit` tool call, runs `py_compile` on the modified file. Prints `✓ syntax OK` or `✗ syntax error` immediately — before the agent moves to the next step.

**What this eliminates:** The pattern of writing code across multiple files and only discovering a syntax error when `pytest` finally runs. With this hook, syntax errors surface at the file level, immediately after the edit, while the agent still has that file in focus.

**Before the hook:** syntax errors discovered at `pytest` run time, sometimes several edits later.
**After the hook:** syntax errors caught within one tool call of the mistake.
