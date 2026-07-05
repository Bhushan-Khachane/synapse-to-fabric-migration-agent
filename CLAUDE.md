# CLAUDE.md — Synapse → Fabric Migration Agent

> This file is loaded at the start of every Claude Code session. Keep it concise.

## Project Purpose
Migrate Azure Synapse Analytics workspaces to Microsoft Fabric using a multi-agent system.
- Source: `synapse/` (READ-ONLY — never modify)
- Target: `fabric/` (written by agents)
- Artifacts: pipelines, SQL objects, notebooks, semantic models

## Agent System
8-agent orchestrator-worker system:
- **migration-orchestrator** (Opus): lead agent — dispatches, validates JSON output against schemas, pauses at human gates
- **pipeline-assessor**: Phase 1 — read-only assessment
- **tsql-converter**: Phase 2 — SQL conversion (worktree isolation)
- **pipeline-converter**: Phase 3 — pipeline JSON conversion (worktree isolation)
- **fabric-deployer**: Phase 4 — deployment to Fabric DEV workspace
- **data-validator**: Phase 5 — row count and schema parity check
- **report-migrator**: Phase 6 — semantic model and Power BI report migration (worktree isolation)
- **security-auditor**: Phase 7 — pre-commit secret scan (read-only, no Write)

## Typed Handoff Protocol
Every agent writes output to `migration/state/phaseN_<name>.json`.
Orchestrator validates each output against schemas in `.claude/schemas/` before proceeding.
data-validator reads phase2_convert_sql.json for `tables_referenced` and `validation_queries`.

## Security Rules — NON-NEGOTIABLE
- NEVER paste production data, query results, or sample rows into prompts
- NEVER include credentials, connection strings, or secrets in any file
- `synapse/` is READ-ONLY — bash_guard and settings.json both enforce this
- Kill switch: `touch .claude/KILL_SWITCH` halts all agents immediately
- Hooks run mechanically — they cannot be bypassed

## Cost Management
Per-phase budgets (tokens): Assess 50K | SQL 200K | Pipelines 150K | Deploy 75K | Validate 100K | Reports 125K | Security 50K
Total per segment: 750K tokens

## Common Commands
- `/migrate-segment <name>` — Launch full 7-phase migration
- `/convert-sql <file>` — Convert one SQL object
- `/batch-convert <dir>` — Batch convert a directory
- `/assess-pipeline <file>` — Assess one pipeline
- `/validate-migration <dir>` — Validate converted artifacts

## Key File Locations
- State file: `migration/state/migration_state.json`
- Audit trail: `migration/audit/audit_trail.jsonl`
- Architecture differences: `docs/architecture-differences.md`
- Deployment config: `migration/config/deploy_config.json`

## Coding Conventions
- SQL: PascalCase, schema-qualified names, one object per file
- JSON: 2-space indentation
- Python: PEP 8, type hints, docstrings
