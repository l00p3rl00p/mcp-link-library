# ENVIRONMENT.md — Workforce Nexus Suite (mcp-link-library)

Host environment requirements, safety rules, and OS-specific paths for the **Link Library** repo.

---

## 🔍 Core Dependency Rules

### Python
* **Minimum**: Python **3.9+**
* **Recommended**: Python **3.11+**
* **Isolation**: When installed as part of the suite, runs from the **central** Nexus environment under `~/.mcp-tools` (no workspace venv required).

---

## 🛠 Central Paths (Suite Home)

The suite uses predictable, user-owned paths:
* Nexus home: `~/.mcp-tools`
* Tools bin: `~/.mcp-tools/bin`
* Shared venv (optional): `~/.mcp-tools/.venv`
* Shared state + devlogs: `~/.mcp-tools/mcpinv/`

---

## ⚙️ Safety Rules (No Disk Scans)

To reduce risk and surprise:
* Tools do **not** crawl your filesystem or walk up directory trees to “find” workspaces.
* Uninstall operations only touch **approved central locations** (e.g. `~/.mcp-tools`, `~/.mcp-tools/mcpinv`, and the Nexus PATH block).
* If you need to clean a git workspace, the tools print manual cleanup commands instead of deleting workspace files.

---

## 🧾 Devlogs (Shared Diagnostics)

Shared JSONL devlogs live under:
* `~/.mcp-tools/mcpinv/devlogs/nexus-YYYY-MM-DD.jsonl`

Behavior:
* Entries are appended as actions run.
* Old devlog files are pruned on use (90-day retention).

---

## 📝 Metadata
* **Status**: Hardened
* **Reference**: [ARCHITECTURE.md](./ARCHITECTURE.md) | [USER_OUTCOMES.md](./USER_OUTCOMES.md)

