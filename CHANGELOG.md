# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-06

### Added
- Initial release of the Synapse → Fabric Migration Agent
- 8-agent system: orchestrator + 7 specialist subagents
- 5 Claude Code hooks: bash_guard, kill_switch, secret_scanner, audit_logger, session_start
- 4 typed JSON handoff schemas with JSON Schema validation
- 7-phase migration workflow: assess → convert SQL → convert pipelines → deploy → validate → reports → security audit
- Mechanical kill switch via sentinel file
- Immutable audit trail (SHA-256 hashed, append-only JSONL)
- Per-phase token budget enforcement (750K total per segment)
- Worktree isolation for write-capable agents
- Pre-seeded architecture differences knowledge base (10+ known issues)
- Evaluation suite scaffold for test segments
- Full documentation suite (10 docs)
- 5 slash commands for granular operations
