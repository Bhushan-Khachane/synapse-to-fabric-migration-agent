#!/usr/bin/env python3
"""
SessionStart hook: logs every session initialization.

Writes to migration/audit/sessions.jsonl (append-only).
Warns loudly if the kill switch sentinel is active from a prior session.

This hook runs automatically at the start of every Claude Code session
in this project (configured in .claude/settings/settings.json).
"""
import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path


SESSION_LOG = Path("migration") / "audit" / "sessions.jsonl"
KILL_SWITCH = Path(os.getcwd()) / ".claude" / "KILL_SWITCH"


def main() -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "SESSION_START",
        "cwd": os.getcwd(),
        "session_id": os.environ.get("CLAUDE_SESSION_ID", ""),
        "kill_switch_active": KILL_SWITCH.exists(),
    }

    SESSION_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    if KILL_SWITCH.exists():
        print(
            "\n[SESSION_START WARNING] Kill switch is ACTIVE from a previous session.\n"
            "  All tool calls will be blocked until you run: rm .claude/KILL_SWITCH\n",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
