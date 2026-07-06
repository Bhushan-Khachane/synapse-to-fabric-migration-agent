#!/usr/bin/env python3
"""
PreToolUse hook for Bash tool calls.

Blocks:
  - Destructive filesystem commands (rm -rf, dd)
  - Dangerous git operations (push --force, reset --hard)
  - Network exfiltration (curl | sh, wget | sh, scp, ssh)
  - Credential access (az keyvault secret, sqlcmd -P)
  - Write BYPASS vectors: patterns Claude uses when Write/Edit is denied
    (sed -i, echo >, python -c open().write(), tee /, cat >)
  - Synapse directory writes (source is read-only)

Exit codes:
  0 — allow
  2 — block (only code that mechanically stops the tool call)
"""
import json
import sys
import re


BLOCKED_PATTERNS = [
    # Destructive filesystem
    (r"rm\s+-rf\s+/", "destructive rm -rf /"),
    (r"rm\s+-r\s+/", "destructive rm -r /"),
    (r"rm\s+-rf\s+~", "destructive rm -rf ~"),
    (r"rm\s+-rf\s+\$HOME", "destructive rm -rf $HOME"),
    (r"\bdd\s+.*of=/", "destructive dd of=/"),
    # Dangerous git
    (r"git\s+push\s+--force", "git push --force"),
    (r"git\s+reset\s+--hard", "git reset --hard"),
    (r"git\s+clean\s+-f", "git clean -f"),
    (r"git\s+branch\s+-D\s+main", "git branch -D main"),
    (r"git\s+branch\s+-D\s+master", "git branch -D master"),
    # Network exfiltration
    (r"\bcurl\s+.*\|\s*sh", "curl | sh (remote exec)"),
    (r"\bwget\s+.*\|\s*sh", "wget | sh (remote exec)"),
    (r"\bscp\s+", "scp (file exfiltration)"),
    (r"\brsync\s+.*@", "rsync to remote"),
    (r"\bssh\s+", "ssh connection"),
    # Credential access
    (r"\baz\s+login", "az login (credential access)"),
    (r"\baz\s+account\s+set", "az account set"),
    (r"\baz\s+keyvault\s+secret\s+show", "az keyvault secret show"),
    (r"\baz\s+keyvault\s+secret\s+download", "az keyvault secret download"),
    # SQL destructive
    (r"\bDROP\s+DATABASE\b", "DROP DATABASE"),
    (r"\bDROP\s+TABLE\b", "DROP TABLE"),
    (r"\bTRUNCATE\s+TABLE\b", "TRUNCATE TABLE"),
    (r"\bDROP\s+SCHEMA\b", "DROP SCHEMA"),
    # Write bypass vectors (Claude uses these when Write/Edit is denied)
    (r"\bsed\s+-i", "sed -i (write bypass)"),
    (r"\becho\s+.*>\s*/", "echo > / (write bypass)"),
    (r"\bprintf\s+.*>\s*/", "printf > / (write bypass)"),
    (r"\btee\s+/", "tee / (write bypass)"),
    (r"\bpython3?\s+-c\s+.*open\(.*['\"]w", "python -c open().write (write bypass)"),
    (r"\bpython3?\s+-c\s+.*\.write\(", "python -c .write() (write bypass)"),
    (r"\bnode\s+-e\s+.*writeFile", "node -e writeFile (write bypass)"),
    (r"\bcat\s+.*>\s*/", "cat > / (write bypass)"),
]

SYNAPSE_WRITE_PATTERNS = [
    (r"echo\s+.*>\s*synapse/", "write to synapse/ (read-only)"),
    (r"tee\s+synapse/", "tee to synapse/ (read-only)"),
    (r"sed\s+-i.*synapse/", "sed to synapse/ (read-only)"),
    (r"python3?\s+-c\s+.*open\(['\"]synapse/", "python write to synapse/ (read-only)"),
    (r"cp\s+.*\s+synapse/", "cp to synapse/ (read-only)"),
    (r"mv\s+.*\s+synapse/", "mv to synapse/ (read-only)"),
]


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")
    if not command:
        sys.exit(0)

    for pattern, description in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            print(
                f"[BASH_GUARD BLOCKED] {description}\n"
                f"  Command: {command[:120]}{'...' if len(command) > 120 else ''}",
                file=sys.stderr,
            )
            sys.exit(2)

    for pattern, description in SYNAPSE_WRITE_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            print(
                f"[BASH_GUARD BLOCKED] {description} — synapse/ is the read-only source\n"
                f"  Command: {command[:120]}{'...' if len(command) > 120 else ''}",
                file=sys.stderr,
            )
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
