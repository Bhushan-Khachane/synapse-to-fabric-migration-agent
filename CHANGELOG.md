# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — 2026-07-06

### Added
- Full orchestrator-worker multi-agent architecture
- `migration-orchestrator` lead agent (Claude Opus) with 7-phase dispatch
- 7 specialist subagents: `pipeline-assessor`, `tsql-converter`, `pipeline-converter`, `fabric-deployer`, `data-validator`, `report-migrator`, `security-auditor`
- 5 security hooks: `bash_guard`, `kill_switch`, `secret_scanner`, `audit_logger`, `session_start`
- 4 typed JSON handoff schemas with JSON Schema Draft 2020-12
- `migrate_segment.py` CLI orchestration script with terminal-based human gates
- `schema_validator.py` for validating agent output against schemas
- `state_manager.py` for resumable migration state
- `cost_tracker.py` for per-phase token budget enforcement
- `kill_switch_manager.py` for kill switch activate/deactivate
- Complete documentation suite (10 docs)
- Example conversions for stored procedures, pipelines, and semantic models
- Eval test segment with known-good Synapse → Fabric conversion pairs
- Architecture differences knowledge base pre-seeded with 20+ known differences
