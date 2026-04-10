# CLAUDE.md — Token Efficiency Rules

**These rules are mandatory. The user is paying per token. Violating these wastes their money.**

## Coordination protocol (zedobackend / zedofrontend / boobinho)

`COORDINATION.md` is the async channel between agents. Cheap protocol:

1. At session start: `git log -3 --oneline COORDINATION.md`
2. **If no recent commits since you last touched it → skip the file entirely.**
3. **If recent commits → Grep only your section + questions for you:**
   - zedobackend: `Grep "## 🔧 Backend status" -A 40 COORDINATION.md` + `Grep "→ backend" -A 10 COORDINATION.md`
   - zedofrontend: `Grep "## 🎨 Frontend status" -A 40 COORDINATION.md` + `Grep "→ frontend" -A 10 COORDINATION.md`
   - boobinho: `Grep "## 📚 Knowledge updates" -A 40 COORDINATION.md` + `Grep "→ boobinho" -A 10 COORDINATION.md`
4. **Never read COORDINATION.md fully.** It will grow.
5. At session end: append a short update to your section + commit. Don't rewrite other agents' content.

**File ownership** (don't refactor outside scope):
- **zedobackend**: `backend.py`, `pf_models.py`, `minutes_generator.py`, `pf_export.py`, `slides.py`, `constants.py`
- **zedofrontend**: `_design_tokens.py`, `app.py` (CSS/layout), `pages/*.py` (presentation only)
- **boobinho**: `boobinho_knowledge_base.json`, `/research/*`
- **shared** (any agent can edit): `translations.py`, `COORDINATION.md`, `requirements.txt`

## Reading files

- **Never** read a file > 200 lines without `offset` + `limit`.
- **Grep first, Read second.** Find the exact line via Grep, then Read 10-30 lines around it.
- **Never re-read** a file you read in this session unless it was modified AND you need to edit it.
- **Never read whole .md specs.** Grep for the section, then Read targeted lines.
- For multi-thousand-line page files (`pages/*.py`), always Grep + Read offset.

## Editing files

- **Max ~150 lines per Edit call.** Big features = multiple smaller edits, not one monolith.
- **Trust the file state cache.** Don't re-Read after a successful Edit.
- If a linter modified a file, only re-read the **specific section** you need to edit, not the whole file.

## Verification

- **No `curl`/`wc -l`/`ls` for verification.** Trust syntax checks (`py -3 -c "import ast..."`) and tracking.
- **Only run syntax check on files you actually edited**, not all 11 files.
- **Don't restart Streamlit** unless explicitly asked or the change requires runtime testing. The user can restart manually.

## Subagents

- **Explore agent prompts must be Y/N or list-of-3-things.** Never "thorough audit", never "very detailed report".
- **Max 1 paragraph per agent prompt.** Specify the exact output format.
- **Don't run multiple agents** when 1 Grep + 1 Read does the same job.

## Web search / fetch

- **No WebSearch unless the user explicitly asks for external research.**
- **No WebFetch on big sites** without targeted prompt.

## Bash

- **No `git log`/`git status`** unless about to commit.
- **No exploratory `ls`** — use Glob.
- **Single-line commands**, no multi-step verification chains.

## Task management

- **Create tasks only when working on 3+ parallel items.** Linear work = no tasks.
- **Don't split single edits into multiple "tasks"** just to look organized.

## Output to user

- **No tables for simple decisions.** Plain text answer.
- **No "Resumo do que foi feito" sections** unless user asks. They see the diffs.
- **Lead with the answer**, not the reasoning.
- **Max ~200 words** for status updates. If longer needed, say "want details?"

## Stack — current state (decided 2026-04-10)

- **Streamlit is the MVP stack.** Build features in Streamlit. Migration to Next.js + FastAPI is a future option, not the current plan.
- New features → add them to existing `pages/*.py` or create new pages.
- Keep backend logic in pure Python modules (`backend.py`, `pf_models.py`, `minutes_generator.py`, etc.) so they're reusable if/when migration happens later.

## Project context (current state)

- 7 financial pages: Business Case, M&A, Project Finance, DCF, Startup, Hedging, LBO
- `_design_tokens.py` exists with Section 4 design system
- Calculation engine in `backend.py` (IRR, MIRR, WACC, DSCR, Monte Carlo, etc.)
- Translations in `translations.py` (PT/EN)
- Constants/defaults in `constants.py`
- SPE Diagram + Contract Minutes tabs in `pages/03_Project_Finance.py` (form-based MVP)
- Migration plan: backend extraction → React/Next.js → retire Streamlit
