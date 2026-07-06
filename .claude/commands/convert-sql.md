# /convert-sql

Convert a single Synapse SQL object to Fabric Warehouse-compatible T-SQL.

## Usage

```
/convert-sql <path/to/source.sql>
```

## What Happens

1. Reads the specified SQL file from `synapse/sql/`
2. Dispatches `tsql-converter` agent with the single file
3. Writes converted output to `fabric/warehouse/[object-type]/[filename].sql`
4. Appends a single-object entry to `migration/state/phase2_convert_sql.json`

## Examples

```
/convert-sql stored-procedures/sp_SalesReport.sql
/convert-sql views/vw_CustomerSummary.sql
/convert-sql functions/fn_GetFiscalYear.sql
```
