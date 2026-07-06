# /assess-pipeline

Assess a single Synapse pipeline JSON file for Fabric migration readiness.

## Usage

```
/assess-pipeline <path/to/pipeline.json>
```

## What Happens

1. Reads the specified pipeline JSON from `synapse/pipelines/`
2. Dispatches `pipeline-assessor` agent with the single file
3. Appends assessment result to `migration/state/phase1_assess.json`
4. Prints a summary: activity count, blockers, estimated conversion effort

## Examples

```
/assess-pipeline pl_sales_ingest.json
/assess-pipeline pl_customer_etl.json
```
