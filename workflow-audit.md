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
| **MCP servers** | Give It Eyes and Ears | Not covered in firstbuild scope |

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
- The "old tasks missing priority field" bug would have been caught by the spec, not discovered post-hoc in a test gap analysis.
- The coverage report confusion (0% on `cli.py`) would have been in the spec upfront as a known limitation, not discovered mid-session.
