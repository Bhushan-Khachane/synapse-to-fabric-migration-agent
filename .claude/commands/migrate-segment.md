# /migrate-segment

Launch a full 7-phase migration for the specified segment name.

## Usage

```
/migrate-segment <segment-name>
```

## What Happens

1. Reads `migration/state/migration_state.json` to check current progress
2. If no state file exists, initializes it with the segment name and start timestamp
3. Launches `migration-orchestrator` agent with:
   > "Migrate segment: $ARGUMENTS. Read current state from migration/state/migration_state.json.
   > Follow the 7-phase order. Validate each subagent output against schemas in .claude/schemas/.
   > Pause at each phase gate for human approval. Enforce per-phase token budgets.
   > Update migration_state.json after each approved phase."
4. The orchestrator dispatches subagents phase by phase
5. You are prompted for approval at each gate: `yes / no / adjust`

## Examples

```
/migrate-segment sales-data-etl-reports
/migrate-segment inventory-etl
/migrate-segment finance-reporting
/migrate-segment customer-analytics
```

## Resuming an Interrupted Migration

If a session was interrupted, simply run the same command again.
The orchestrator reads the state file and resumes from the last incomplete phase.
Already-approved phases are never re-run.
