#!/usr/bin/env python3
"""
PostToolUse hook for Write and Edit tool calls.

Logs every file write to an append-only audit trail at:
  migration/audit/audit_trail.jsonl

Each entry contains:
  - timestamp (UTC ISO 8601)
  - event_type: FILE_WRITE
  - tool: Write or Edit
  - file_path: the file that was written
  - content_sha256: SHA-256 hash of the content (for tamper detection)
  - content_length: byte count
  - session_id: CLAUDE_SESSION_ID env var (if available)

The audit file is APPEND-ONLY. Never rewrite or delete it.
SOC 2 / GDPR compliance requires this trail to be preserved.
"""
import json
import sys
import os
import hashlib
from datetime import datetime, timezone
from pathlib import Path


AUDIT_FILE = Path("migration") / "audit" / "audit_trail.jsonl"


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool = data.get("tool_name", "unknown")
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "unknown")
    content = tool_input.get("content", "")

    content_hash = (
        hashlib.sha256(content.encode("utf-8", errors="replace")).hexdigest()
        if content
        else ""
    )

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "FILE_WRITE",
        "tool": tool,
        "file_path": file_path,
        "content_sha256": content_hash,
        "content_length": len(content.encode("utf-8", errors="replace")),
        "session_id": os.environ.get("CLAUDE_SESSION_ID", ""),
    }

    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Never block on audit logger failure
        sys.exit(0)
