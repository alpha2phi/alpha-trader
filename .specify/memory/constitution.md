<!--
Sync Impact Report
- Version change: 1.0.0 -> 2.0.0
- Modified principles:
  - Market Data Fidelity & Compliance -> Good Taste – Prefer the General Solution
  - Deterministic Analytics Contracts -> Never Break Userspace
  - Scenario-First Delivery -> Pragmatism Over Perfection
  - Explainable Insights & Observability -> Simplicity Obsession
  - Test-Enforced Risk Controls -> Domain Guardrails (Operational)
- Added sections: Purpose; Communication Principles; Requirement Analysis Workflow; Decision Output Format; Code Review Standards; Language-Specific Guidelines; 🧪 Testing & Tooling; 📥 Commit & PR Guidelines; 📄 PR Template
- Removed sections: None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->
# alpha-trader Constitution

## Purpose
This constitution sets operational guardrails for AI coding agents working on alpha-trader. It
combines universal engineering doctrine with asset-class-specific controls so every change keeps
the dashboard trustworthy, testable, and user-ready.

## Core Principles

### Good Taste – Prefer the General Solution
We pursue general, data-structure-driven solutions instead of piling on conditionals or ad-hoc
patches. Every feature proposal must show how it collapses special cases and elevates the design.
- Replace branching cascades with cohesive abstractions; a new `if` must demonstrate why a data
  model, lookup table, or configuration cannot solve the case.
- Keep modules extensible for fresh tickers, timeframes, or analytics without rewiring flows.
- When balancing flexible design vs. velocity, default to the option that keeps future features
  linear in effort rather than exponential.
Rationale: Tasteful, general solutions age well and prevent the dashboard from turning brittle as
new asset classes and indicators arrive.

### Never Break Userspace
Backward compatibility is sacred. If users rely on a CLI flag, contract field, or alert format, we
must preserve it or ship a migration path with tooling.
- Treat regressions as critical bugs; halting delivery is preferable to silent schema drift.
- Default to additive versioning (new fields, new endpoints). If removal is unavoidable, document
  upgrade steps, notify stakeholders, and gate merges on review approval.
- Automated tests must cover compatibility promises before code review completes.
Rationale: Traders depend on stable signals; breakage erodes trust faster than any new feature can
restore it.

### Pragmatism Over Perfection
Solve real, current problems with proven techniques. Theory is welcome only when paired with
production evidence.
- Anchor specs and plans to concrete user scenarios and current constraints; de-prioritize
  speculative architecture without supporting data.
- Prefer boring, observable components to flashy, untested stacks; experiments belong behind
  feature flags with rollback hooks.
- Communicate trade-offs explicitly so reviewers can judge whether complexity buys tangible
  upside.
Rationale: Practical, scenario-first iterations ensure shipping value beats endless ideation.

### Simplicity Obsession
Simplicity is mandatory in code, docs, and tooling.
- Keep functions and modules tight; if nesting exceeds three levels, refactor.
- Name things with crisp, descriptive language; avoid abbreviation soup.
- When in doubt, delete dead code, collapse layers, and document the resulting clarity.
Rationale: Simple systems are auditable, easier to onboard, and reduce operational risk.

## Communication Principles
- **Style**: Communicate directly, concisely, and with technical precision. Critique artifacts, not
  people.
- **Output**: Deliver structured, actionable summaries with explicit decisions.
- **Priority**: Correctness, maintainability, and backward compatibility always outrank speed.

## Requirement Analysis Workflow
1. **Data Structure Analysis** – Identify core entities, ownership, and data flow.
2. **Special Case Identification** – Replace branching or isolated code paths with better
   modeling.
3. **Complexity Review** – Repeatedly simplify until the essence is obvious and reviewable.
4. **Backward Compatibility Check** – Validate that existing contracts, scripts, and docs remain
   valid.
5. **Practicality Verification** – Confirm real-world necessity; defer speculative features.

## Decision Output Format
- **Core Judgment**: State whether the proposal is worth doing and why.
- **Key Insights**: Capture data ownership, complexity hotspots, and risk.
- **Solution Guidance**: Outline how to simplify data, eliminate special cases, and prevent
  destructive changes.

## Code Review Standards
- **Taste Score**: Classify as Good Taste, Acceptable, or Needs Work with justification.
- **Fatal Issues**: Call them out immediately; blocking items stop the merge until fixed.
- **Improvements**: Focus on reducing branching, clarifying data models, and tightening
  abstractions.

## Language-Specific Guidelines

### 🐍 Python
- Follow PEP 8, apply type hints, and keep functions small. Prefer pure functions.
- Use pytest or unittest; keep analytics runnable via CLI (no notebook-only logic).
- Avoid unnecessary classes; simple functions plus dataclasses work best.

### ⚡ JavaScript
- Adhere to ESLint (Airbnb or Standard rules); prefer `const`/`let`.
- Keep modules modular; avoid sprawling scripts and callback pyramids.
- Use async/await, lint prior to commit, and pin toolchains in package configs.

### 📘 TypeScript
- Enable `strict: true`; treat stray `any` as bugs.
- Prefer interfaces for contracts and leverage generics for reuse.
- Run `tsc --noEmit` pre-commit.

### 🌐 Node.js
- Follow 12-factor principles, embrace async/await, and keep dependencies lean.
- Handle errors explicitly and ensure scripts exit cleanly with no unhandled promises.

### ⚛️ React
- Use functional components with hooks plus prop-types or TypeScript for validation.
- Control re-renders via `React.memo`, stable keys, and memoized selectors.
- Test with React Testing Library or Jest to lock in behavior.

### 🐹 Golang
- Follow Effective Go; keep functions short and readable.
- Handle errors explicitly and run `go fmt` + `golangci-lint`.
- Use interfaces when abstraction is needed; avoid unnecessary OOP structures.

### 🦀 Rust
- Adhere to Rust API guidelines with idiomatic error handling using `Result` and `?`.
- Avoid `unsafe` unless there is a compelling, reviewed reason.
- Co-locate unit tests with code for fast verification.

### 🖥️ PowerShell
- Use Verb-Noun naming (`Get-User`), annotate logic with comments, and keep scripts idempotent.
- Emit `Write-Verbose`/`Write-Error` output appropriately.

### 🖊️ Bash / Zsh
- Start scripts with `#!/usr/bin/env bash` (or zsh) and `set -euo pipefail`.
- Quote variables, prefer functions, and stay POSIX-compatible when possible.

## 🧪 Testing & Tooling
Before any merge, agents run the stack-specific suites below (expand as needed for new stacks).

### Python
- `pytest`
- `flake8` or `ruff`
- `black`
- `mypy`

### JavaScript / TypeScript / Node.js / React
- `npm test` or `yarn test`
- `eslint .`
- `prettier --check .`
- `tsc --noEmit` for TS work

### Golang
- `go fmt ./...`
- `golangci-lint run`
- `go test ./...`

### Rust
- `cargo fmt --check`
- `cargo clippy -- -D warnings`
- `cargo test`

### PowerShell
- `Invoke-Pester`
- `pwsh -Command { . .\script.ps1 }` (syntax check)

### Bash / Zsh
- `shellcheck script.sh`
- `bash -n script.sh`
- Execute scripts with `set -euo pipefail`

## 📥 Commit & PR Guidelines

### Commit Messages
- Follow Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- Keep subject lines under 72 characters and scoped (`feat(auth): add refresh token`).

### Pull Requests
- **Title**: concise and commit-style when possible.
- **Description** must cover context, changes, testing evidence, and impact/breaking notes.
- Require green CI before requesting review; keep PRs focused on a single concern.
- Avoid mixing refactors with features; if unavoidable, explain the coupling.

### Branching
- Use `feature/<slug>` or `fix/<slug>` branches.
- Keep `main` shippable with release-ready dashboards; rebase noisy histories before merge.

## 📄 PR Template
Copy into `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## 🔍 Context
Explain why this change is needed. What problem does it solve? Link to issue/task if applicable.

## ✨ Changes
- [ ] Feature: ...
- [ ] Fix: ...
- [ ] Refactor: ...
- [ ] Docs/Tests/Chore: ...

## 🧪 Testing
Describe how you tested this change.  
- Commands run:  
- Unit/Integration tests:  
- Manual validation steps:  

## ⚠️ Impact
- [ ] Breaking change  
- [ ] Requires migration  
- [ ] No breaking changes  

## ✅ Checklist
- [ ] Code is linted and formatted  
- [ ] All tests pass locally (`npm test`, `pytest`, `go test`, etc.)  
- [ ] Follows commit guidelines (Conventional Commits)  
- [ ] Updated docs/tests if necessary  
```

## Domain Guardrails
- Python 3.11 is the baseline runtime; alternative stacks require governance approval and updated
  tooling entries.
- Declare every data provider, endpoint, and refresh cadence in specs; keep credentials only in
  approved secret stores.
- Cache financial data with timestamps and checksum metadata; explicitly invalidate expired caches
  before reuse.
- Honor licensing, rate limits, and jurisdictional requirements before delivering a feature.

## Delivery Workflow & Quality Gates
1. **Research Gate**: Plans must document general solutions, compatibility promises, pragmatic
   scope, and simplicity risks before design begins.
2. **Build Gate**: CI executes headless analytics plus story-focused tests; logs/metrics are
   attached for reviewer inspection.
3. **Review Gate**: Reviewers enforce principle alignment; unresolved violations block merge.
4. **Release Gate**: Update README/docs with new capabilities, verify data provenance evidence, and
   restate compatibility impact before tagging.

## Governance
- Amendments require a written proposal citing observed gaps, approval from one engineering lead
  and one product/data stakeholder, plus migration notes for impacted templates.
- Semantic versioning governs the constitution: MAJOR for rewritten principles, MINOR for new
  sections or material guidance, PATCH for clarifications and typo fixes.
- Each sprint demo highlights Constitution compliance; teams log their status in feature plans so
  drift is caught early.
- Runtime guidance (README, templates, scripts) must update within the same change set as any
  constitutional amendment; reviewers verify via the Sync Impact Report.

**Version**: 2.0.0 | **Ratified**: 2025-11-23 | **Last Amended**: 2025-11-23
