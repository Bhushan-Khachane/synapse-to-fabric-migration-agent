# /validate-migration

Validate migrated data in Fabric against source Synapse data.

## Usage

```
/validate-migration [table-name | directory]
```

## What Happens

1. Reads `migration/state/phase2_convert_sql.json` for table list and validation queries
2. Dispatches `data-validator` agent
3. Runs row count, schema parity, and checksum checks
4. Writes results to `migration/state/phase5_validate.json`
5. Prints pass/fail summary

## Examples

```
/validate-migration dbo.SalesOrders
/validate-migration dbo.SalesItems
/validate-migration
```

Run with no argument to validate all tables in the current segment.
