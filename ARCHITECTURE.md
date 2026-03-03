# Architecture - MCP Librarian (mcp-link-library)

**The technical blueprint for the Universal Knowledge Indexer.**

The **Librarian** is the knowledge persistence layer of the Workforce Nexus. It moves beyond simple file storage into **Data Projection** and **ATP-Hardened Search**, ensuring agents have access to verified truth without context bloat.

---

## 🔍 Core Philosophy: Zero-Token Data Processing

The Librarian is designed to protect the LLM's context window. Instead of returning full document contents, it projects only the requested fields or snippets, applying the **Zero-Token Filtering** principle.

---

## 🏗 Subsystem Breakdown

### 1. The Universal Parser (`mcp.py`)
Handles heterogeneous file formats using a modular plugin architecture.
* **PDF Engine**: `pypdf`-based text extraction.
* **Excel Engine**: `openpyxl`-based cell/sheet projection.
* **image Engine**: Metadata and EXIF extraction via `Pillow`.
* **Standard Doc Engine**: `python-docx` for structured text retrieval.

### 2. The Knowledge Base (SQLite)
A persistent, local-first database that catalogs resources, metadata, and full-text indexes.
* **Atomic Transactions**: Uses SQLite's ACID compliance to ensure data integrity during parallel indexing tasks.
* **Heuristic Indexing**: Automatically tags files with categories (api, docs, legal) based on path patterns.

### 3. The ATP Sandbox (`atp_sandbox.py`)
Provides a hardened execution environment for agent-driven data processing.
* **AST Inspection**: Blocks dunder-access (`__class__`), class-escape (`type()`), and attribute-escape (`getattr()`) vectors.
* **Deterministic Logic**: Ensures logic remains portable across different host environments.

### 4. Self-Healing Module (`check_health`)
A diagnostic subsystem that audits the environment's health:
* **Dependency Audit**: Checks if optional parsers are available.
* **Self-Request**: If a parser is missing, it provides a tool-call to install the required library.

### 5. GUI Bridge Daemon (`gui_bridge.py`)
Flask-based REST API for dashboard interaction and MCP server lifecycle management.
* **Foreground Mode** (default): `python3 gui_bridge.py` — traditional blocking HTTP server.
* **Daemon Mode** (v6.0): `python3 gui_bridge.py --daemon` — POSIX double-fork detachment with PID file (`~/.mcpinv/gui_bridge.pid`).
* **Status Command** (v6.0): `python3 gui_bridge.py --status` — exit code 0 (running) or 1 (stopped).
* **Stop Command** (v6.0): `python3 gui_bridge.py --stop` — graceful SIGTERM termination.
* **Version Health Endpoint** (v6.0): `/version-health` — monitors source vs installed version drift, returns `needs_repair` flag.
* **Security**: CORS limited to localhost only; all JSON parsing catches `JSONDecodeError`; subprocess calls use list-based argv (no shell injection).

### 6. Dashboard UI (`App.tsx`)
React + TypeScript SPA frontend for real-time Nexus observability.
* **Dashboard Tab**: Displays managed MCP server inventory with interactive "Start"/"Stop" buttons.
* **Librarian Tab**: "Artifact Explorer" table showing indexed files with disk paths and sizes.
* **Terminal Tab**: Master command log (JSONL from `~/.mcpinv/session.jsonl`) with live updates.
* **Version Health Badge** (v6.0): Rendered in header, shows "v3.4.0" (green) or "⚠️ Repair Needed" (red) with tooltip containing action command.
* **Polling Strategy**: Core data (logs, status) every 2s; version health every 30s (slow-changing).

---

## 🔐 Security & Safety

### 1. Path Guarding
The Librarian only indexes files within approved workspace boundaries. It rejects attempts to traverse into system-level directories.

### 2. Token Weight HUD
Exposes heuristic character counting to the Dashboard, allowing the user to see the "Token Weight" of any requested search result before it is sent to the LLM.

---

## 📝 Metadata
* **Status**: Production Ready (v6.0) — Mission Score 100% ✅
* **Latest Release**: 2026-03-03
* **Key Milestones**:
  - v3.3.5 (2026-02-25): Auto-watcher launch (GAP-R3 closed)
  - v3.4.0 (2026-02-26): Named stacks for knowledge organization
  - v6.0 (2026-03-03): GUI reliability (daemon mode) + operational awareness (version health)
* **Author**: l00p3rl00p
* **Part of**: The Workforce Nexus Suite
