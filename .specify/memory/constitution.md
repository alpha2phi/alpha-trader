<!--
Sync Impact Report
- Version change: template -> 1.0.0
- Modified principles:
  - Template principle 1 -> Market Data Fidelity & Compliance
  - Template principle 2 -> Deterministic Analytics Contracts
  - Template principle 3 -> Scenario-First Delivery
  - Template principle 4 -> Explainable Insights & Observability
  - Template principle 5 -> Test-Enforced Risk Controls
- Added sections: Operational Constraints; Delivery Workflow & Quality Gates
- Removed sections: None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->
# alpha-trader Constitution

## Core Principles

### Market Data Fidelity & Compliance
All market, sentiment, and macro inputs must be sourced from documented providers with
reproducible retrieval parameters so trading insights are always auditable.
- Declare every provider, endpoint, and refresh cadence inside each spec and keep credentials
  in approved secrets storage; no unvetted feeds or manual copy/paste data.
- Cache data with timestamps and checksum metadata to prove integrity; expired caches must be
  explicitly invalidated before re-use.
- Honor licensing, rate limits, and jurisdictional requirements; compliance violations block
  delivery regardless of feature pressure.
Rationale: Traders trust this dashboard only when every datapoint can withstand regulatory
scrutiny.

### Deterministic Analytics Contracts
All analysis engines (fundamental, technical, sentiment, AI) expose stable contracts so their
outputs can be stitched together without surprises.
- Each module must declare input schema, required indicators, and output fields using the
  shared spec contract format; undocumented fields are not accepted at review.
- CLI-automation is mandatory: every analytic is runnable headless with identical arguments for
  CI pipelines and manual analysts.
- Breaking a contract (field removal, semantic change) requires a new semantic version and
  migration notes before merge.
Rationale: Deterministic contracts prevent hidden coupling between dashboards, alerts, and APIs.

### Scenario-First Delivery
Work is sliced by independently shippable trading scenarios so the team can deliver incremental
value without blocking on mega-features.
- Every feature spec names the primary user scenario (e.g., "swing trader earnings play") and
  delivers it end-to-end before optional polish.
- Plans and tasks must keep stories isolated in files/modules to enable parallel effort and
  independent demos.
- Scope creep that combines scenarios must be split or justified in the Complexity Tracking
  table with explicit risk acknowledgements.
Rationale: Scenario slices guarantee the dashboard always has a usable, testable increment.

### Explainable Insights & Observability
Insights must be explainable to humans and observable by machines so regressions surface before
users open the dashboard.
- Every surfaced insight includes a short explanation (data sources used + indicator math) in
  the UI or CLI output; no opaque "AI says so" text.
- Emit structured logs for each pipeline stage (ingestion, feature engineering, inference,
  visualization) with correlation IDs.
- Baseline dashboard metrics (latency, failed data pulls, anomaly counts) feed into CI and must
  gate releases when thresholds are exceeded.
Rationale: Explainability and observability keep analysts confident and shorten MTTR.

### Test-Enforced Risk Controls
Testing is the first consumer of any change; failed risk controls halt work until resolved.
- Tests cover (1) data ingestion validation, (2) indicator math verification, (3) scenario
  acceptance flows, and (4) alerting/notification wiring when applicable.
- Contract, unit, and integration suites must be written before implementation for each story;
  failing tests are the definition of ready-to-build.
- Critical numeric outputs require golden datasets checked into the repo (or referenced via
  fixtures) to prevent drift.
Rationale: Automated risk controls prevent incorrect trading guidance from ever reaching users.

## Operational Constraints
- Python 3.11 with vetted libraries (documented in specs) is the baseline runtime; alternative
  stacks require governance approval.
- Secrets (API keys, tokens) never live in source files or specs; use environment variables and
  document the names in the plan.
- Deployment targets must define their monitoring hooks and data residency considerations before
  first release.

## Delivery Workflow & Quality Gates
1. **Research Gate**: Constitution Check in plan.md must confirm data-source registry, analytic
   contracts, scenario definition, observability plan, and pre-implementation test suite outline.
2. **Build Gate**: CI must run headless analytics CLI workflows plus scenario acceptance scripts;
   logs and metrics exported to artifacts for reviewer inspection.
3. **Review Gate**: PR reviewers verify explainability notes and adherence to task isolation;
   unresolved Constitution violations block merge.
4. **Release Gate**: Before tagging, update success metrics dashboards and attach provenance
   evidence for all new data feeds.

## Governance
- This constitution supersedes conflicting playbooks. Amendments require a proposal referencing
  observed gaps, reviewer approval from at least one engineering lead plus one product/data
  stakeholder, and a migration plan for impacted templates.
- Semantic versioning applies: MAJOR for removed/rewritten principles, MINOR for new sections or
  materially expanded guidance, PATCH for clarifications.
- Every sprint demo reviews Constitution Check items; teams log compliance status in the feature
  plan so drift is caught early.
- Runtime guidance (README, templates, scripts) must be updated in the same change as any
  constitutional amendment; reviewers verify via the Sync Impact Report.

**Version**: 1.0.0 | **Ratified**: 2025-11-23 | **Last Amended**: 2025-11-23
