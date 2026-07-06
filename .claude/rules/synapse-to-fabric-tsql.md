# T-SQL Compatibility Rules: Synapse → Fabric Warehouse

This file is loaded by `tsql-converter` at the start of every conversion session.
Each rule includes the Synapse pattern, the Fabric replacement, and whether it is
automatic or requires manual review.

---

## IDENTITY Columns

**Synapse:** `column_name INT IDENTITY(1,1)`  
**Fabric:** `column_name INT GENERATED ALWAYS AS IDENTITY`  
**Status:** Automatic  
**Note:** Fabric Warehouse uses ANSI standard identity syntax. `DBCC CHECKIDENT` is not supported.

---

## Scalar User-Defined Functions

**Synapse:** `CREATE FUNCTION dbo.fn_GetTax(@amount DECIMAL) RETURNS DECIMAL AS BEGIN ... END`  
**Fabric:** Convert to inline table-valued function (TVF): `CREATE FUNCTION dbo.fn_GetTax(@amount DECIMAL) RETURNS TABLE AS RETURN (SELECT ...)`  
**Status:** Automatic where logic is a single expression; Manual review for multi-statement UDFs  
**Note:** Scalar UDFs with side effects or RAISEERROR are not supported.

---

## Cross-Database References

**Synapse:** `SELECT * FROM OtherDB.dbo.TableName`  
**Fabric:** Replace with OneLake shortcut or Lakehouse external table reference  
**Status:** Needs review — flag as blocker, document in arch_diffs_discovered  
**Note:** Fabric Warehouse does not support three-part cross-database references.

---

## Cursors

**Synapse:** `DECLARE cursor_name CURSOR FOR SELECT ...`  
**Fabric:** Convert to set-based operation using CTEs or WHILE loops  
**Status:** Manual review required  
**Note:** While cursors are syntactically allowed, performance is severely degraded. Always convert.

---

## Temporary Tables

**Synapse:** `CREATE TABLE #TempTable (...)` — session-scoped  
**Fabric:** Supported. No change required.  
**Status:** Automatic (no-op)  
**Note:** Global temp tables (`##TempTable`) are NOT supported — flag as blocker.

---

## sp_executesql and Dynamic SQL

**Synapse:** `EXEC sp_executesql @sql, @params, @val`  
**Fabric:** Supported with limitations — no DDL inside dynamic SQL  
**Status:** Needs review — check for DDL in dynamic SQL  

---

## OPENROWSET

**Synapse:** `SELECT * FROM OPENROWSET(BULK 'https://...', FORMAT='PARQUET') AS r`  
**Fabric:** Replace with Lakehouse table or OneLake shortcut  
**Status:** Needs manual rewrite  

---

## EXTERNAL TABLES

**Synapse:** `CREATE EXTERNAL TABLE dbo.ExternalSales (...) WITH (LOCATION='...', DATA_SOURCE=...)`  
**Fabric:** Replace with Lakehouse table with OneLake shortcut  
**Status:** Needs manual rewrite — document data source mapping  

---

## DISTRIBUTION Hints

**Synapse:** `CREATE TABLE dbo.Orders (...) WITH (DISTRIBUTION = HASH([OrderId]), CLUSTERED COLUMNSTORE INDEX)`  
**Fabric:** Remove all `WITH (DISTRIBUTION=...)` clauses. Fabric manages distribution automatically.  
**Status:** Automatic removal  

---

## STATISTICS

**Synapse:** `CREATE STATISTICS stat_Orders ON dbo.Orders(OrderId)`  
**Fabric:** Remove — Fabric manages statistics automatically  
**Status:** Automatic removal  

---

## WORKLOAD MANAGEMENT

**Synapse:** `CREATE WORKLOAD GROUP wg_Reporting ...`  
**Fabric:** Not applicable — remove all workload classifier/group DDL  
**Status:** Automatic removal  

---

## RESULT_SET_CACHING

**Synapse:** `ALTER DATABASE current SET RESULT_SET_CACHING ON`  
**Fabric:** Not supported — remove  
**Status:** Automatic removal  

---

## LINKED SERVER References

**Synapse:** `SELECT * FROM [LinkedServer].Database.dbo.Table`  
**Fabric:** Replace with Fabric pipeline Copy activity or Lakehouse shortcut  
**Status:** Blocker — requires architectural decision  

---

## TRY_CAST / TRY_CONVERT

**Status:** Fully supported. No change required.

---

## STRING_SPLIT with ordinal

**Synapse:** `SELECT * FROM STRING_SPLIT(@str, ',', 1)`  
**Fabric:** Supported in Fabric Warehouse GA.  
**Status:** No change required.

---

## Header Comment Template

Every converted file must start with:
```sql
/*
  Object    : <schema>.<object_name>
  Type      : <StoredProcedure|View|Function|Table>
  Source    : synapse/sql/<path>
  Converted : <YYYY-MM-DD>
  Status    : <converted|needs_review|blocked>
  Changes   : <comma-separated list of changes made>
*/
```
