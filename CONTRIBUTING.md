# Contributing to Synapse → Fabric Migration Agent

Thank you for contributing! This guide explains how to add new migration rules, fix bugs, and submit PRs.

## Areas Most Needing Contributions

1. **T-SQL conversion rules** — new Synapse → Fabric incompatibilities in `.claude/rules/synapse-to-fabric-tsql.md`
2. **Pipeline activity mappings** — new activity types in `.claude/rules/pipeline-migration.md`
3. **Architecture differences** — newly discovered differences in `docs/architecture-differences.md`
4. **Eval pairs** — add known-good source/target pairs in `migration/evals/`
5. **Hook improvements** — new secret patterns in `.claude/hooks/secret_scanner.py`

## How to Submit a PR

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/new-tsql-rule`
3. Make your changes
4. Test against the eval suite: `python migration/orchestration/run_evals.py`
5. Submit a PR with a clear description of what was changed and why

## Adding a New T-SQL Conversion Rule

Edit `.claude/rules/synapse-to-fabric-tsql.md`:

```markdown
### [Rule Name]
- **Synapse**: `<synapse pattern>`
- **Fabric**: `<fabric equivalent>`
- **Notes**: Any caveats or manual steps
- **Example**:
  ```sql
  -- Synapse
  <example synapse code>
  
  -- Fabric
  <example fabric code>
  ```
```

## Adding an Eval Pair

1. Create a directory: `migration/evals/<segment-name>/`
2. Add source artifacts in `migration/evals/<segment-name>/synapse/`
3. Add hand-verified expected output in `migration/evals/<segment-name>/expected-fabric/`
4. Add `migration/evals/<segment-name>/README.md` explaining what is tested

## Code Style

- Python: PEP 8, type hints on all functions
- SQL: PascalCase object names, schema-qualified, one object per file
- Markdown: ATX headers, 80-char line limit where possible
