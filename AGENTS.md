# clinical-env — Agent Instructions

Shared contract for Claude Code, Codex and Cursor (`CLAUDE.md` imports it). Workflow revision: 2026-10-20.

## Context

Working name: clinical-env (a launch name comes later).

**Who.** The clinical lead: a doctor and founder; time comes in short bursts. The agent is the
engineer and planning partner and owns the code, plan and docs. The clinical lead owns
clinical judgement.

**What.** A simulator and harness that tests how an AI clinician manages a complex older adult
across 2 to 3 visits, when the patient, a carer and several records disagree. Good care turns on
function, falls, ADLs, the medicines actually taken, and whether the package of care still fits.
Often there is no single diagnosis. v0 answers one question: do frontier models fail at this?
Its transcripts are also the first sales sample.

**How to work with the clinical lead.**
- Start every session with `PROGRESS.md` (next step, waiting-on) and **Active decisions** in
  `DECISIONS.md`. A fresh session must be able to pick up from those alone.
- `docs/build-v0.md` is the starting spec, not a contract. Challenge it: propose changes, agree
  them with the clinical lead, then log them in `DECISIONS.md` (date, what, why) and update the spec.
- Before each milestone, give a plan of 10 lines or fewer. Build after he says go.
- Keep messages short. Lead with what you need from him.
- Do research yourself (web, papers, subagents). Ask him only for clinical judgement, his
  accounts or his contacts, one specific question at a time.

**Rules that don't move without the clinical lead's explicit say-so.**
- All case content is fictional. Never commit real patient data: no real names, dates of birth,
  NHS numbers, addresses or copied clinic letters.
- Pilot failure criteria are frozen in a commit before the first real run and never changed
  after seeing results.
- The model under test never sees the hidden truth, the rubric or the other parties' views.
- Private GitHub repo. Keys in `.env`, never committed.
- Ask before spending more than $20 on API calls in one go.
- Stop at M1 and show him two full transcripts. Clinical realism is his call.

**Models and keys.** OpenAI and Gemini keys; an Anthropic key is
being added so the pilot covers three labs. Gemini's free tier runs no Pro or flagship model, so
the pilot needs Gemini billing. All model calls go through Inspect AI's model API, selected by
config and model role. Cheap models for simulators and checker; strong models for judges.

**Reference.**
- `DECISIONS.md`: what's agreed, proposed and open. `PROGRESS.md`: where we are and what's next.
- `docs/build-v0.md`: the v0 spec, milestones and pilot criteria.
- `docs/research-summary.md`: the papers, whether their code is public, what to copy from ResidencyRL.
- `docs/brief.md`: the thesis and early business decisions.
- `docs/research-report.md`: full market and evidence report. Long; search it, don't read it whole.
- `docs/case-template.md`: the plain-English template the clinical lead writes cases in (drafts in `cases/drafts/`).
- `docs/papers/residencyrl-2608.07418.pdf`: sections 3.1 to 3.3 describe the simulator and
  grader we copy (CC BY 4.0).

## Start / resume

1. Find the project root and worktree; check the branch and `git status`. Preserve existing edits.
   On a fresh clone, `./scripts/setup` restores the locked dependencies.
2. Read `PROGRESS.md` and the **Active decisions** in `DECISIONS.md` fresh, also after an agent
   switch; chat or injected context may be stale. Check `LEARNINGS.md`, if present, before debugging.
3. State the next step and continue the user's request within the accepted gates.
4. With other agents in this checkout, split files or tasks and re-read shared files before
   writing. Never reset, stash or switch branches over someone else's unfinished work.

## Stack

- Python 3.12+ managed with **uv**. Choose the model/provider for the product; verify the
  current SDK API and model IDs before use, and put the chosen model in configuration.
- Validate structured outputs with Pydantic before they drive application logic.
- Keep prompts easy to locate and version. Add representative evaluation cases for changes
  to prompt, agent or retrieval behavior, including failure cases and input/output limits.
- RAG answers should carry supporting sources; test access isolation where users share a
  retrieval service. Bound retries and cost, and record usage without sensitive content.
- Use synthetic/de-identified data in prompts, traces, fixtures and evaluations.

## Commands

- One gate from any agent or CI: `./scripts/check` (Ruff formatting/lint, strict mypy, pytest).
- After `uv init`: `uv add --dev pytest ruff mypy`; add the chosen SDK only when needed and
  keep `uv.lock`. Restore dependencies with `uv sync --locked`.
- Format changed Python files with `uv run ruff format <paths>` before the gate.
- Missing tests fail. Include deterministic schema/retrieval tests in pytest; run relevant
  live-model evaluations separately and report their model, cases, cost and results.

## Engineering

- Plan multi-file work briefly. Read code and config first; verify unfamiliar APIs in installed
  types or official docs. Restructure new/touched code freely with behaviour tests; leave
  unrelated old code alone. Reuse what fits and avoid speculative abstractions.
- Add behaviour tests for new logic and bug fixes, including failure cases. After a fix, look
  for the same bug elsewhere and say what you checked.
- Format, then push: the pre-push hook runs `./scripts/check` in its fast scope (format, lint,
  types, unit tests) on the committed revision (no hook: run those yourself). The full gate,
  with build and browser tests, runs once in CI; fix it there. Between pushes run only the
  checks your edits affect. Record the command, result, revision and dirty state. Never weaken
  a check to get green, and report skipped or failing checks as such.
- Automatically verify changed behaviour through the real interface, then review once per PR,
  not per chunk or fix commit. Self-review small changes; otherwise use one fresh-context
  code-review subagent briefed to cover security too. Add a separate security-review subagent
  only when sign-in, sessions, tokens, permissions or tenant isolation change, or personal
  data goes to a third party. Fix blocking findings (wrong behaviour, data exposure, an
  exploitable security flaw, a broken journey) in the PR; record the rest with a
  concrete next step in the task list or `PROGRESS.md` and list them in the PR. Self-review the
  fixes; re-review only a large rework. Read-only reviewer delegation in the current host/model
  is authorised; reviewers do not delegate again. If unavailable, self-review and report the
  gap. Cross-model review only on request.
  Never leave checks for the owner to run or remind you about.
- Record consequential decisions with the reason; skip routine ones. An architecture decision
  (undoing would cost more than a day or touch stored data or users) goes in `DECISIONS.md` in
  the same commit, tagged `[arch]`, with **Instead of**, **To undo** and **By**. The draft PR
  lists them under **Decisions to review**, or "None". Ask first for one-way doors: data loss,
  a migration that cannot be undone without losing data, paid or contractual lock-in.

## Verify / review / pre-push (fallback without shared skills)

1. Resolve the base: the PR target or remote default branch, not an assumed `main`. Review
   `git diff BASE...HEAD` plus staged, unstaged and intended untracked files. An empty working
   diff does not mean nothing is outgoing.
2. Look for bugs, missing tests, weakened checks and needless complexity. Report file/line,
   impact and a concrete fix.
3. If auth, user input, files/URLs, secrets or data handling changed, check those boundaries.
   Before a push, scan outgoing history and current files with the secret scanner.
4. Use `docs/verification.md` and the changed real interface. New web apps require `test:e2e`
   (Playwright) in the gate; other stacks use integration tests. Add/update changed journey tests,
   use synthetic data and isolated services; retain reports and useful screenshots. Check web
   error/empty states, keyboard and narrow screens; migrations need recovery checks, AI synthetic
   evaluations. Report devices/accessibility checks that could not be performed.
5. `./scripts/check` must pass on the final files. A CI file alone does not prove that a failed
   check blocks deployment.

## Wrap-up (when the shared skill is unavailable)

- Re-read `PROGRESS.md`; check branch, revision, status and new files.
- If code changed since the last passing check, rerun the affected checks unless told to stop
  now; the full gate runs at the next push.
- Rewrite `PROGRESS.md` in under ~60 lines: current state, gates, last check (command, result,
  revision, dirty state), unfinished work, next action, blockers. Drop stale claims.
- Add only consequential decisions (refresh **Active decisions**) and real lessons. Delete
  one-off handoff notes once their content is folded in.
- Report the outcome and one next action. Wrap-up alone does not trigger delivery.

## Security and Git

- Secrets live in ignored env files or a secret store; `.env.example` names every variable the
  project reads, never a value. No real user or patient data in code, fixtures, prompts or
  logs. Validate external input at boundaries.
- Say early when work needs something this session lacks: a secret or `.env` value, an
  external service, another repo, or a Mac-only or UI step. Stop that part, report it in the
  handoff and the PR, and finish the rest. Never invent values, mock real credentials or skip
  a check silently.
- Implementation uses feature branches, conventional commits, passing gate/verification/review,
  then autonomous feature push and draft PR; fix CI within scope. Verify the shared pre-push
  hook is active first; without it (a fresh cloud clone) run `CHECK_SCOPE=push ./scripts/check`
  and the secret scan yourself before pushing, and say so. If the guard blocks the push for a
  missing hook, run `./scripts/setup` or report it. No pushes/deletions to `main`,
  `master` or the remote default branch.
- Use `gh pr create --draft --base BASE --title TITLE --body-file FILE` in that order. Where
  `gh` is not signed in (cloud sessions), use the GitHub tool's create-pull-request with draft
  set, and never its merge or auto-merge tools.
- Agents never merge, enable auto-merge or deploy to production: stop at a ready draft PR; the
  owner merges on GitHub. No bypass via other APIs, `--no-verify` or plain `--force`. Preview
  data/secrets must be isolated.
- Rules are current preferences: explain blockers and propose a change when sensible.
- If blocked, gather evidence and re-plan rather than repeating a failed attempt.
