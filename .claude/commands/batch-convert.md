# /batch-convert

Batch convert all SQL files in a directory using the tsql-converter agent.

## Usage

```
/batch-convert <synapse/sql/directory/>
```

## What Happens

1. Glob all `.sql` files in the specified directory
2. Dispatches `tsql-converter` agent for each file
3. Writes all converted files to the corresponding `fabric/warehouse/` path
4. Writes a consolidated JSON artifact to `migration/state/phase2_convert_sql.json`

## Examples

```
/batch-convert stored-procedures/
/batch-convert views/
/batch-convert functions/
```
