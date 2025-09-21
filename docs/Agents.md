# Agents.md

## Purpose
This repository uses **AI coding agents**. This file defines behavior, review principles, and communication standards for all supported languages. It encodes universal coding philosophy, language-specific guidelines, tooling expectations, and contribution rules to ensure clarity, maintainability, and compatibility.

---

## Core Philosophy (Universal)

1. **Good Taste – Prefer the General Solution**  
   - Eliminate special cases with better data structures.  
   - Avoid unnecessary `if/else` branching.  
   - Favor elegance and simplicity.  

2. **Never Break Userspace**  
   - Maintain backward compatibility.  
   - Treat regressions as bugs.  
   - Code must serve real users, not theoretical purity.  

3. **Pragmatism Over Perfection**  
   - Solve actual problems, not hypothetical ones.  
   - Prefer practical, proven solutions over overly complex ideals.  

4. **Simplicity Obsession**  
   - Functions/modules should be short and focused.  
   - More than 3 levels of nesting → redesign.  
   - Naming should be concise and descriptive.  

---

## Communication Principles

- **Style**: Direct, concise, technically precise. Critique code, not people.  
- **Output**: Clear, structured, and actionable.  
- **Priority**: Correctness, maintainability, backward compatibility.  

---

## Requirement Analysis Workflow

When evaluating a feature or request:

1. **Data Structure Analysis** – identify core data and ownership.  
2. **Special Case Identification** – remove unnecessary branching.  
3. **Complexity Review** – simplify until essence is clear.  
4. **Backward Compatibility Check** – never break existing functionality.  
5. **Practicality Verification** – confirm real-world necessity.  

---

## Decision Output Format

- **Core Judgment**: Worth doing / Not worth doing (with reason).  
- **Key Insights**: data, complexity, risks.  
- **Solution Guidance**: simplify data, remove special cases, guarantee zero destructiveness.  

---

## Code Review Standards

- **Taste Score**: Good taste / Acceptable / Needs work.  
- **Fatal Issues**: Call out immediately.  
- **Improvement Suggestions**: reduce branching, simplify, refactor data.  

---

## Language-Specific Guidelines

### 🐍 Python
- Follow **PEP 8** for style and formatting.  
- Use type hints (`typing`) when possible.  
- Keep functions small; prefer pure functions.  
- Use `pytest` or `unittest` for testing.  
- Avoid overusing classes; use simple functions where sufficient.  

### ⚡ JavaScript
- Follow **ESLint (airbnb or standard rules)**.  
- Prefer `const`/`let` over `var`.  
- Keep functions modular and avoid large monolithic scripts.  
- Use async/await instead of nested callbacks.  
- Always lint before committing.  

### 📘 TypeScript
- Use strict typing (`strict: true`).  
- Prefer interfaces over type aliases for contracts.  
- Catch `any` usage — replace with explicit types.  
- Leverage generics for reusable code.  
- Run `tsc --noImplicitAny` before committing.  

### 🌐 Node.js
- Follow **12-factor app** principles.  
- Use async/await for async flows.  
- Handle errors with try/catch or `.catch()`.  
- Keep dependencies minimal.  
- Scripts should exit cleanly (no unhandled promises).  

### ⚛️ React
- Use **functional components** with hooks.  
- Keep components small and composable.  
- Use `prop-types` or TypeScript for props validation.  
- Avoid unnecessary re-renders (`React.memo`, key usage).  
- Follow **React Testing Library** or Jest for tests.  

### 🐹 Golang
- Follow **Effective Go** guidelines.  
- Keep functions short; prefer readability over cleverness.  
- Always handle errors explicitly.  
- Use `go fmt` and `golangci-lint`.  
- Favor interfaces for abstractions; avoid unnecessary OOP.  

### 🦀 Rust
- Follow **Rust API guidelines**.  
- Use idiomatic error handling (`Result`, `?` operator).  
- Avoid unsafe unless absolutely necessary.  
- Write unit tests in the same file as code.  
- Prefer immutability and ownership clarity.  

### 🖥️ PowerShell
- Follow **Verb-Noun** naming for functions (e.g., `Get-User`).  
- Use `Write-Verbose` and `Write-Error` appropriately.  
- Keep scripts idempotent when possible.  
- Comment scripts with `#` to explain non-obvious logic.  

### 🖊️ Bash / Zsh
- Start scripts with `#!/usr/bin/env bash` (or zsh).  
- Use `set -euo pipefail` to catch errors early.  
- Quote variables (`"$VAR"`) to avoid word-splitting.  
- Prefer functions over inline blocks for reusability.  
- Keep scripts POSIX-compatible where possible.  

---

## 🧪 Testing & Tooling

Before committing or merging code, run the following checks:

### Python
- `pytest` (unit tests)  
- `flake8` or `ruff` (lint)  
- `black` (format)  
- `mypy` (type check)  

### JavaScript / TypeScript / Node.js / React
- `npm test` or `yarn test`  
- `eslint .` (lint)  
- `prettier --check .` (format check)  
- `tsc --noEmit` (for TypeScript type checking)  

### Golang
- `go fmt ./...` (format)  
- `golangci-lint run` (lint)  
- `go test ./...` (tests)  

### Rust
- `cargo fmt --check` (format)  
- `cargo clippy -- -D warnings` (lint)  
- `cargo test` (tests)  

### PowerShell
- `Invoke-Pester` (tests if present)  
- `pwsh -Command { . .\script.ps1 }` (basic syntax check)  

### Bash / Zsh
- `shellcheck script.sh` (lint)  
- `bash -n script.sh` (syntax check)  
- Run scripts with safe flags (`set -euo pipefail`).  

---

## 📥 Commit & PR Guidelines

### Commit Messages
- Use [Conventional Commits](https://www.conventionalcommits.org/):  
  - `feat:` → new feature  
  - `fix:` → bug fix  
  - `docs:` → documentation only  
  - `test:` → add/modify tests  
  - `chore:` → maintenance  
- Example:  
  ```
  feat(auth): add JWT refresh token support
  fix(api): correct null pointer in user lookup
  ```

### Pull Requests
- **Title**: Clear, concise, follows commit style if possible.  
- **Description**: Must include:  
  - **Context**: What problem this solves.  
  - **Changes**: What was done.  
  - **Testing**: How it was verified.  
  - **Impact**: Any breaking changes, migrations, or risks.  

### Review Standards
- PRs must pass **all tests and tooling checks** before merge.  
- Keep PRs **small and focused** (single concern).  
- Avoid mixing refactors with feature changes.  

### Branching
- Use feature branches: `feature/short-description`  
- Use bugfix branches: `fix/short-description`  
- Keep `main` (or `master`) always stable.  

---

## 📄 PR Template

Copy the following into `.github/PULL_REQUEST_TEMPLATE.md` to auto-fill PRs:

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
