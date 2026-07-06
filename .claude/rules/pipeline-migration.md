# Pipeline Migration Rules: Synapse → Fabric Data Factory

Loaded by `pipeline-converter` at the start of every session.

---

## Activity Type Mapping

| Synapse Activity Type | Fabric Equivalent | Status |
|---|---|---|
| Copy | Copy | Automatic |
| ExecutePipeline | ExecutePipeline | Automatic |
| ForEach | ForEach | Automatic |
| IfCondition | IfCondition | Automatic |
| Wait | Wait | Automatic |
| SetVariable | SetVariable | Automatic |
| AppendVariable | AppendVariable | Automatic |
| Lookup | Lookup | Automatic |
| GetMetadata | GetMetadata | Automatic |
| Filter | Filter | Automatic |
| Until | Until | Automatic |
| Switch | Switch | Automatic |
| Fail | Fail | Automatic |
| SqlServerStoredProcedure | StoredProcedure | Rename type only |
| ExecuteDataFlow (Gen1) | Notebook (Spark) | **Manual rewrite required** |
| HDInsightSpark | Notebook (Spark) | Needs review |
| DatabricksNotebook | Notebook | Needs review |
| AzureFunctionActivity | WebActivity | Needs review |
| WebHook | WebActivity | Needs review |
| SynapseNotebook | Notebook | Automatic |
| SparkJobDefinition | SparkJobDefinition | Automatic |
| ExecuteSSISPackage | **UNSUPPORTED** | Blocker |
| AzureMLBatchExecution | **UNSUPPORTED** | Blocker |

---

## Linked Service → Fabric Connection Mapping

| Synapse Linked Service | Fabric Connection Type |
|---|---|
| AzureSqlDatabase | Azure SQL Database |
| AzureSqlDW (Synapse) | Fabric Warehouse |
| AzureBlobStorage | Azure Blob Storage |
| AzureDataLakeStorageGen2 | Azure Data Lake Gen2 |
| AzureKeyVault | Azure Key Vault |
| AzureDatabricks | Azure Databricks |
| RestService | REST |
| HttpServer | HTTP |
| AzureTableStorage | Azure Table Storage |
| CosmosDb | Azure Cosmos DB |
| Salesforce | Salesforce |

**Rule:** Replace all `typeProperties.connectVia` with Fabric workspace connection reference.
Never hardcode connection strings. Use Fabric connection names from `migration/config/deploy_config.json`.

---

## Trigger Migration Rules

1. All triggers must be deployed as **DISABLED** (`"runtimeState": "Stopped"`)
2. ScheduleTrigger: map cron expression directly — supported
3. TumblingWindowTrigger: supported — map windowSize directly
4. BlobEventsTrigger: map to Storage Event trigger in Fabric
4. CustomEventsTrigger: supported
5. **RerunTumblingWindowTrigger: NOT supported in Fabric — flag as needs_review**

---

## Integration Runtime Rules

- `AutoResolveIntegrationRuntime` → Fabric default runtime (automatic)
- Self-hosted IR → must be registered in Fabric workspace manually — flag as blocker
- Azure IR with specific region → Fabric uses workspace region — flag as needs_review if region-specific

---

## Data Flow Gen1 (ExecuteDataFlow)

This is the most complex migration scenario:
1. Flag as `needs_manual_rewrite`
2. Document all source/sink datasets
3. Document transformation logic (derived columns, aggregates, joins, filters)
4. Recommend Fabric Notebook (PySpark) as replacement
5. Never auto-convert — always escalate to human

---

## Parameters and Variables

- All pipeline parameters must be preserved exactly
- All pipeline variables must be preserved exactly
- Default values must be preserved
- Parameter types: String, Int, Float, Bool, Array, Object — all supported

---

## Error Handling

- `onFailure` edges: preserved
- `onSkip` edges: preserved  
- `onSuccess` edges: preserved
- Retry policy on activities: preserved
- Timeout values: preserved

---

## Output File Structure

Every converted pipeline JSON must:
1. Be placed in `fabric/pipelines/<pipeline_name>.json`
2. Have a header comment block:
```json
"_migration": {
  "source": "synapse/pipelines/<name>.json",
  "converted": "<YYYY-MM-DD>",
  "status": "converted|needs_review|blocked",
  "changes": ["<list of changes made>"]
}
```
3. Triggers deployed as separate files in `fabric/pipelines/triggers/`
