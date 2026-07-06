# CLAUDE.md — Synapse → Fabric Migration Agent

## Project Overview
This repository contains a multi-agent system for migrating Azure Synapse Analytics workspaces
to Microsoft Fabric. It uses Claude Code's orchestrator-worker pattern with human approval gates.

- **Source:** Azure Synapse Analytics (dedicated SQL pools, Spark notebooks, pipelines, linked services)
- **Target:** Microsoft Fabric (Warehouse, Lakehouse, Data Factory pipelines, semantic models)
- **Architecture:** migration-orchestrator (Opus) dispatches 7 Sonnet subagents, each outputting typed JSON

## Architecture Quick Reference
- Orchestrator: `.claude/agents/migration-orchestrator.md` (Opus, dispatches all)
- Subagents: `.claude/agents/*.md` (Sonnet, scoped tools, some with worktree isolation)
- Hooks: `.claude/hooks/*.py` (mechanical enforcement, cannot be bypassed)
- Schemas: `.claude/schemas/*.schema.json` (typed handoff contracts between agents)
- Rules: `.claude/rules/*.md` (stable migration conversion rules)
- State: `migration/state/migration_state.json` (resumable)
- Audit: `migration/audit/audit_trail.jsonl` (immutable, append-only)

## Migration Phases
1. **Assess** → `pipeline-assessor` (read-only, Sonnet)
2. **Convert SQL** → `tsql-converter` (worktree isolation, Sonnet)
3. **Convert Pipelines** → `pipeline-converter` (worktree isolation, Sonnet)
4. **Deploy** → `fabric-deployer` (Bash, DEV workspace only, Sonnet)
5. **Validate Data** → `data-validator` (read-only DB queries, Sonnet)
6. **Convert Reports** → `report-migrator` (worktree isolation, Sonnet)
7. **Final Review** → `security-auditor` (read-only, no Write permission, Sonnet)

## Security Rules — READ BEFORE EVERY SESSION
- **NEVER** paste production data, query results, or sample rows into prompts
- **NEVER** include credentials, connection strings, or secrets in any file
- `synapse/` directory is **READ-ONLY** — never modify source artifacts
- All subagent outputs must conform to schemas in `.claude/schemas/`
- Hooks enforce security mechanically — bypassing them requires removing hook config
- Kill switch: `touch .claude/KILL_SWITCH` halts all agents immediately
- Kill switch reset: `rm .claude/KILL_SWITCH`

## Common Commands
- `/migrate-segment <segment-name>` — Launch full migration for a segment
- `/convert-sql <path/to/file.sql>` — Convert a single SQL object
- `/batch-convert <directory/>` — Batch convert a directory of SQL files
- `/assess-pipeline <path/to/pipeline.json>` — Assess a single pipeline
- `/validate-migration <directory/>` — Validate converted artifacts

## Cost Management
- Per-phase token budgets enforced by orchestrator (see orchestrator agent)
- Total budget per segment: 750,000 tokens
- If exceeded: orchestrator triggers kill switch and pauses for human intervention
- Orchestrator (Opus) is used ONLY for planning + synthesis — keeps cost lean
- All heavy work delegated to Sonnet subagents

## Coding Conventions
- SQL files: PascalCase naming, schema-qualified object names (e.g., `dbo.SalesOrders`)
- One SQL object per file (one stored proc per `.sql` file)
- Pipeline JSON: 2-space indentation
- Header comment on every converted file:
  ```sql
  -- Object: dbo.sp_SalesReport
  -- Migrated from: Synapse dedicated pool
  -- Migration status: converted | needs_review | blocked
  -- Migration date: YYYY-MM-DD
  ```
