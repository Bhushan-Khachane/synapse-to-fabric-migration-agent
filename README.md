# 🏗️ Synapse → Fabric Migration Agent

> **Enterprise-grade multi-agent system** for migrating Azure Synapse Analytics workspaces to Microsoft Fabric — orchestrated by Claude (Opus 4), human-gated at every phase, with typed handoffs, immutable audit trails, and mechanical security enforcement.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Opus_4-blueviolet)](https://claude.ai/code)
[![Agents: 8](https://img.shields.io/badge/Agents-8-blue)](#agent-reference)
[![Phases: 7](https://img.shields.io/badge/Migration_Phases-7-green)](#migration-phases)

---

## 🎯 What This Does

This system automates the migration of **Azure Synapse Analytics** workspaces to **Microsoft Fabric** using a fleet of specialist Claude subagents coordinated by a lead orchestrator. You approve each phase before it proceeds. Nothing gets committed without your sign-off.

**What gets migrated:**
- ✅ T-SQL stored procedures, views, functions, schemas
- ✅ Synapse Data Factory pipelines → Fabric Data Factory
- ✅ Spark notebooks
- ✅ Power BI semantic models / TMSL definitions
- ✅ Linked services → Fabric connections
- ✅ Triggers (migrated as DISABLED)

**What you get:**
- 🔐 Immutable audit trail of every file change (SHA-256 hashed)
- 🔒 Mechanical security enforcement via Claude Code hooks
- 📊 Typed JSON handoffs between agents (schema-validated)
- 🧪 Data validation comparing source vs target row counts & schema
- 🚨 Kill switch — one command halts all agents instantly
- 💰 Per-phase token budget enforcement

---

## 🏛️ Architecture

```
                     ┌───────────────────────────────┐
                     │     HUMAN OPERATOR (You)       │
                     │  • Launches /migrate-segment   │
                     │  • Approves/rejects at gates   │
                     │  • Can trigger kill switch     │
                     └──────────────┬────────────────┘
                                    │
                     ┌──────────────▼────────────────┐
                     │  migration-orchestrator (Opus) │
                     │  • Reads state file            │
                     │  • Dispatches subagents        │
                     │  • Validates JSON vs schema    │
                     │  • Enforces token budgets      │
                     │  • Pauses at each gate         │
                     └─┬───┬───┬───┬───┬───┬───┬─────┘
                       │   │   │   │   │   │   │
            ┌──────────▼┐┌▼──┐┌▼──┐┌▼──┐┌▼──┐┌▼──┐┌▼──────────┐
            │Phase 1    ││Ph2││Ph3││Ph4││Ph5││Ph6││Phase 7     │
            │assessor   ││sql││pl ││dep││val││rep││security    │
            │(RO,Sonnet)││(wt││(wt││   ││(RO││(wt││(RO,noWrite)│
            └───────────┘└───┘└───┘└───┘└───┘└───┘└────────────┘
                   │       │    │    │    │    │        │
                   ▼       ▼    ▼    ▼    ▼    ▼        ▼
            ┌─────────────────────────────────────────────────┐
            │       migration/state/ (typed JSON artifacts)    │
            │  phase1_assess.json → phase2_convert_sql.json   │
            │  → phase3_pipelines.json → phase4_deploy.json   │
            │  → phase5_validate.json → phase6_reports.json   │
            │  → phase7_security.json                          │
            └─────────────────────────────────────────────────┘
```

### Hook Enforcement Layer

Every tool call passes through mechanical enforcement hooks **before** execution:

| Hook | Event | Blocks |
|------|-------|--------|
| `bash_guard.py` | PreToolUse | `rm -rf`, `git push --force`, `sed -i`, `python -c .write()`, SQL DROP |
| `kill_switch.py` | PreToolUse | All tool calls when `.claude/KILL_SWITCH` exists |
| `secret_scanner.py` | PreToolUse (Write/Edit) | Passwords, Azure keys, AWS keys, JWTs, private keys |
| `audit_logger.py` | PostToolUse (Write/Edit) | Logs SHA-256 hash of every file write |
| `session_start.py` | SessionStart | Logs session init, warns if kill switch active |

---

## 🚀 Quick Start

### Prerequisites

- [Claude Code](https://claude.ai/code) (v2.1.154+, requires Opus 4 access)
- Azure CLI authenticated to your Synapse workspace
- Microsoft Fabric workspace (DEV) created
- Python 3.11+
- Git

### 1. Clone and configure

```bash
git clone https://github.com/Bhushan-Khachane/synapse-to-fabric-migration-agent
cd synapse-to-fabric-migration-agent
pip install -r requirements.txt
```

### 2. Export your Synapse artifacts

```bash
# Export pipelines, SQL scripts, notebooks, linked services from your Synapse workspace
# Place them in the synapse/ directory:
# synapse/pipelines/*.json
# synapse/sql/stored-procedures/*.sql
# synapse/sql/views/*.sql
# synapse/notebooks/*.ipynb
# synapse/semantic-models/*.json
```

### 3. Configure deployment

```bash
cp migration/config/deploy_config.example.json migration/config/deploy_config.json
# Edit deploy_config.json with your Fabric workspace details
```

### 4. Launch Claude Code

```bash
claude
```

### 5. Run the migration

```
/migrate-segment sales-data-etl-reports
```

The orchestrator will guide you through all 7 phases, pausing at each gate for your approval.

---

## 📋 Migration Phases

| Phase | Agent | Model | Tools | What It Does |
|-------|-------|-------|-------|--------------|
| 1. Assess | `pipeline-assessor` | Sonnet | Read, Grep, Glob | Analyzes source artifacts, produces compatibility report |
| 2. Convert SQL | `tsql-converter` | Sonnet | Read, Write, Grep, Glob | Converts stored procs, views, UDFs to Fabric T-SQL |
| 3. Convert Pipelines | `pipeline-converter` | Sonnet | Read, Write, Grep, Glob | Converts pipeline JSON to Fabric Data Factory |
| 4. Deploy | `fabric-deployer` | Sonnet | Read, Write, Bash | Deploys artifacts to Fabric DEV workspace |
| 5. Validate Data | `data-validator` | Sonnet | Read, Write, Bash | Compares row counts and schema between source and target |
| 6. Convert Reports | `report-migrator` | Sonnet | Read, Write, Grep | Recreates semantic models and Power BI reports |
| 7. Final Review | `security-auditor` | Sonnet | Read, Grep, Glob | Pre-commit scan for secrets, credentials, PII |

---

## 🛡️ Security & Compliance

- **SOC 2 alignment**: Immutable audit trail with SHA-256 content hashes
- **Least privilege**: Each agent has exactly the tools it needs — no more
- **No credential storage**: Secret scanner blocks any file write containing passwords, keys, or tokens
- **Read-only source**: `synapse/` directory is protected from all writes at both permission and hook level
- **Kill switch**: `touch .claude/KILL_SWITCH` halts all agents instantly
- **Human gates**: Every phase requires explicit human approval before proceeding

See [docs/security-compliance.md](docs/security-compliance.md) for full enterprise checklist.

---

## 📁 Repository Structure

```
synapse-to-fabric-migration-agent/
├── .claude/
│   ├── agents/          # 8 agent definitions (orchestrator + 7 specialists)
│   ├── commands/        # Slash commands (/migrate-segment, /convert-sql, ...)
│   ├── hooks/           # Mechanical security enforcement scripts
│   ├── rules/           # Stable migration rules (T-SQL, pipeline mapping)
│   ├── schemas/         # Typed JSON handoff schemas (4 schemas)
│   └── settings/        # Permissions + hook wiring
├── docs/                # Full documentation suite (10 docs)
├── examples/            # Sample Synapse → Fabric conversions
├── migration/
│   ├── audit/           # Immutable audit trail (append-only .jsonl)
│   ├── config/          # Deployment configuration
│   ├── evals/           # Evaluation test segments (known-good pairs)
│   ├── orchestration/   # Python scripts: CLI runner, validator, state manager
│   └── state/           # Per-phase typed JSON artifacts
├── synapse/             # READ-ONLY: place your exported Synapse artifacts here
├── fabric/              # TARGET: converted Fabric artifacts land here
├── CLAUDE.md            # Project context (loaded every Claude Code session)
└── README.md
```

---

## ⚡ Commands

| Command | Description |
|---------|-------------|
| `/migrate-segment <name>` | Launch full 7-phase migration for a segment |
| `/convert-sql <file>` | Convert a single SQL object |
| `/batch-convert <dir>` | Batch convert all SQL in a directory |
| `/assess-pipeline <file>` | Assess compatibility of a single pipeline |
| `/validate-migration <dir>` | Validate converted artifacts against source |

---

## 💰 Cost Management

Default per-phase token budgets (configurable in `migration/config/`):

| Phase | Budget |
|-------|--------|
| 1. Assess | 50,000 tokens |
| 2. Convert SQL | 200,000 tokens |
| 3. Convert Pipelines | 150,000 tokens |
| 4. Deploy | 75,000 tokens |
| 5. Validate Data | 100,000 tokens |
| 6. Convert Reports | 125,000 tokens |
| 7. Final Review | 50,000 tokens |
| **Total per segment** | **750,000 tokens** |

If any phase exceeds its budget, the orchestrator activates the kill switch and pauses for human intervention.

---

## 🧪 Evaluation Suite

The `migration/evals/test-segment-sales/` directory contains a small set of known-good Synapse → Fabric conversion pairs for testing agent quality before production use.

Run evals:
```bash
python migration/orchestration/run_evals.py --segment test-segment-sales
```

---

## 📚 Documentation

- [Getting Started](docs/getting-started.md)
- [Architecture Overview](docs/architecture-overview.md)
- [Agent Reference](docs/agent-reference.md)
- [Hook Reference](docs/hook-reference.md)
- [Schema Reference](docs/schema-reference.md)
- [Phase-by-Phase Guide](docs/phase-by-phase-guide.md)
- [Cost Management](docs/cost-management.md)
- [Security & Compliance](docs/security-compliance.md)
- [Architecture Differences: Synapse vs Fabric](docs/architecture-differences.md)
- [Troubleshooting](docs/troubleshooting.md)

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All PRs welcome — especially new T-SQL conversion rules and pipeline activity mappings.

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

## ⚠️ Disclaimer

This tool performs irreversible operations on your Fabric workspace when in deploy mode. Always test against a DEV workspace first. Review all agent outputs at each human gate before approving. The maintainers are not responsible for data loss caused by misconfiguration.
