#!/usr/bin/env python3
"""
PreToolUse hook: kill switch.

Checks for the existence of .claude/KILL_SWITCH sentinel file.
If found, blocks ALL tool calls with exit code 2.

Activate:  touch .claude/KILL_SWITCH
Deactivate: rm .claude/KILL_SWITCH

This hook runs on EVERY tool call (Bash and Write/Edit) so it is
checked twice per action — once before the action type-specific check
and once as the second hook in the chain.
"""
import sys
import os
from pathlib import Path


def main() -> None:
    sentinel = Path(os.getcwd()) / ".claude" / "KILL_SWITCH"
    if sentinel.exists():
        print(
            "[KILL_SWITCH] ACTIVE — all tool calls blocked.\n"
            "  To resume: rm .claude/KILL_SWITCH",
            file=sys.stderr,
        )
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
