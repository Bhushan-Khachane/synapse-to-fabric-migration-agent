# Contributing

Thank you for considering contributing to the Synapse → Fabric Migration Agent.

## How to Contribute

### Reporting Issues
- Use GitHub Issues
- Include your Claude Code version (`claude --version`)
- Describe the phase that failed
- Attach the relevant `migration/state/phaseN_*.json` file (redact any credentials)

### Adding Architecture Differences
The most valuable contribution is adding to `docs/architecture-differences.md` — Synapse vs Fabric quirks discovered during real migrations.

Format:
```markdown
### [Category]
- **Source (Synapse):** description
- **Target (Fabric):** description  
- **Migration approach:** what to do
- **Discovered on:** YYYY-MM-DD
```

### Adding Migration Rules
Rules in `.claude/rules/` are used by subagents for conversion decisions. Add a rule if you find a conversion pattern that isn't already covered.

### Pull Request Process
1. Fork the repo
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Test against the eval segment: `python migration/orchestration/migrate_segment.py --dry-run --segment evals/test-segment-sales`
5. Submit a PR with a clear description of what changed and why

## Code Style
- Python: PEP 8
- JSON schemas: JSON Schema Draft 2020-12
- Agent markdown: follow existing frontmatter format
- Commit messages: `type: short description` (init/feat/fix/docs/refactor)

## Security
- Never commit credentials, connection strings, or sample data
- Never commit the `synapse/` or `fabric/` directories
- If you find a security issue, open a private GitHub Security Advisory
