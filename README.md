# 🏗️ Synapse → Fabric Migration Agent

> Human-assisted AI agent system for migrating Azure Synapse Analytics to Microsoft Fabric — powered by Claude.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude](https://img.shields.io/badge/Powered%20by-Claude%20Opus%20%2B%20Sonnet-blueviolet)](https://claude.ai)
[![Platform](https://img.shields.io/badge/Platform-Microsoft%20Fabric-0078D4)](https://fabric.microsoft.com)

---

## Overview

This project provides a complete **orchestrator-worker multi-agent system** that automates the migration of Azure Synapse Analytics workspaces to Microsoft Fabric, with human approval gates at every phase.

A lead orchestrator agent (Claude Opus) decomposes the migration into 7 ordered phases, dispatches specialist subagents (Claude Sonnet) for each phase, validates their typed JSON output against schemas, and pauses for your approval before proceeding. Every tool call is mechanically enforced by security hooks. Every file write is logged to an immutable audit trail.

---

## Architecture

```
                     ┌────────────────────────────────┐
                     │     HUMAN OPERATOR (You)        │
                     │  /migrate-segment <name>        │
                     │  Approves/rejects at each gate  │
                     │  Can trigger kill switch         │
                     └──────────────┬─────────────────┘
                                    │
                     ┌──────────────▼─────────────────┐
                     │  migration-orchestrator (Opus)  │
                     │  • Reads & updates state file   │
                     │  • Dispatches subagents          │
                     │  • Validates JSON vs schema      │
                     │  • Enforces token budgets        │
                     │  • Pauses at every gate          │
                     └──┬──┬──┬──┬──┬──┬──┬───────────┘
                        │  │  │  │  │  │  │
           ┌────────────▼┐┌▼─┐┌▼─┐┌▼─┐┌▼─┐┌▼─┐┌▼────────────┐
           │Phase 1      ││P2││P3││P4││P5││P6││Phase 7       │
           │pipeline-    ││ts││pi││fa││da││re││security-     │
           │assessor     ││ql││pe││br││ta││po││auditor       │
           │(read-only)  ││co││co││de││va││rt││(read-only,   │
           │Sonnet       ││nv││nv││pl││li││mi││no Write)     │
           │             ││(w││(w││  ││d││gr││Sonnet        │
           │             ││t)││t)││  ││  ││(wt)│              │
           └─────────────┘└──┘└──┘└──┘└──┘└──┘└─────────────┘
                                    │
                     ┌──────────────▼─────────────────┐
                     │     migration/state/ (typed JSON)│
                     │  phase1_assess.json              │
                     │  phase2_convert_sql.json         │
                     │  phase3_convert_pipelines.json   │
                     │  phase4_deploy.json              │
                     │  phase5_validate.json            │
                     │  phase6_reports.json             │
                     │  phase7_security.json            │
                     └─────────────────────────────────┘
```

### Hook Enforcement Layer (every tool call)

| Hook | Trigger | What It Does |
|---|---|---|
| `bash_guard.py` | PreToolUse (Bash) | Blocks 30+ dangerous patterns + Write bypass vectors |
| `kill_switch.py` | PreToolUse (all) | Checks sentinel file; blocks everything if active |
| `secret_scanner.py` | PreToolUse (Write/Edit) | Scans file content for secrets before write |
| `audit_logger.py` | PostToolUse (Write/Edit) | Logs SHA256 hash of every file write |
| `session_start.py` | SessionStart | Logs session init, warns if kill switch active |

---

## Migration Phases

| Phase | Agent | Model | Isolation | What It Does |
|---|---|---|---|---|
| 1 · Assess | `pipeline-assessor` | Sonnet | Shared (RO) | Analyzes source Synapse artifacts, produces compatibility report |
| 2 · Convert SQL | `tsql-converter` | Sonnet | Worktree | Converts stored procs, views, UDFs to Fabric T-SQL |
| 3 · Convert Pipelines | `pipeline-converter` | Sonnet | Worktree | Converts pipeline JSON to Fabric Data Factory format |
| 4 · Deploy | `fabric-deployer` | Sonnet | Shared | Deploys artifacts to Fabric DEV workspace via REST API |
| 5 · Validate Data | `data-validator` | Sonnet | Shared (RO) | Compares row counts + schema between Synapse and Fabric |
| 6 · Convert Reports | `report-migrator` | Sonnet | Worktree | Recreates semantic models and Power BI report bindings |
| 7 · Final Review | `security-auditor` | Sonnet | Shared (RO) | Pre-commit scan for secrets, credentials, and PII |

---

## Quick Start

### Prerequisites

- [Claude Code](https://claude.ai/code) v2.1.154+
- Git
- Python 3.10+
- Azure CLI (for deployment phase)
- Access to both source Synapse workspace and target Fabric workspace

### 1 · Clone and configure

```bash
git clone https://github.com/Bhushan-Khachane/synapse-to-fabric-migration-agent.git
cd synapse-to-fabric-migration-agent
cp migration/config/deploy_config.example.json migration/config/deploy_config.json
# Edit deploy_config.json with your workspace details
```

### 2 · Export Synapse artifacts

```bash
# Place your exported Synapse artifacts into the synapse/ directory
mkdir -p synapse/{sql/{schemas,tables,views,stored-procedures,functions},pipelines,notebooks,semantic-models,linkedservices,triggers}
# Copy your exported JSON and SQL files here
```

### 3 · Launch Claude Code and run the migration

```bash
claude
# In Claude Code:
/migrate-segment sales-data-etl-reports
```

### 4 · Approve each phase gate

The orchestrator will pause after every phase and ask:
```
Phase complete: convert-sql
23 objects converted, 2 need review, 0 blocked.
Proceed to pipeline conversion? (yes / no / adjust)
```

Type **yes** to continue, **no** to stop, or **adjust** to give instructions.

---

## Kill Switch

To immediately halt all running agents:

```bash
touch .claude/KILL_SWITCH
```

Every agent hook checks for this file before executing any tool call. Remove it to resume:

```bash
rm .claude/KILL_SWITCH
```

---

## Cost Management

| Phase | Token Budget |
|---|---|
| Phase 1 — Assess | 50,000 |
| Phase 2 — Convert SQL | 200,000 |
| Phase 3 — Convert Pipelines | 150,000 |
| Phase 4 — Deploy | 75,000 |
| Phase 5 — Validate Data | 100,000 |
| Phase 6 — Convert Reports | 125,000 |
| Phase 7 — Final Review | 50,000 |
| **Total per segment** | **750,000** |

If a phase exceeds its budget, the orchestrator triggers the kill switch and pauses for human intervention.

---

## Project Structure

```
synapse-to-fabric-migration-agent/
├── CLAUDE.md                          # Claude Code project context
├── .claude/
│   ├── settings/settings.json         # Permissions + hook config
│   ├── hooks/                         # 5 mechanical enforcement scripts
│   ├── agents/                        # 8 agent definitions
│   ├── commands/                      # 5 slash commands
│   ├── schemas/                       # 4 typed JSON handoff schemas
│   └── rules/                         # T-SQL and pipeline migration rules
├── migration/
│   ├── orchestration/                 # Python orchestration scripts
│   ├── state/                         # Agent output JSON + state file
│   ├── audit/                         # Immutable audit trail
│   ├── config/                        # Deployment configuration
│   └── evals/                         # Evaluation test segments
├── docs/                              # Full documentation suite
├── examples/                          # Sample conversions
└── synapse/                           # (You add) Source Synapse artifacts
```

---

## Documentation

- [Getting Started](docs/getting-started.md)
- [Architecture Overview](docs/architecture-overview.md)
- [Agent Reference](docs/agent-reference.md)
- [Hook Reference](docs/hook-reference.md)
- [Schema Reference](docs/schema-reference.md)
- [Phase-by-Phase Guide](docs/phase-by-phase-guide.md)
- [Cost Management](docs/cost-management.md)
- [Security & Compliance](docs/security-compliance.md)
- [Architecture Differences](docs/architecture-differences.md)
- [Troubleshooting](docs/troubleshooting.md)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT — see [LICENSE](LICENSE).
