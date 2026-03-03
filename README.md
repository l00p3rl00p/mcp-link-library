# MCP Librarian: The Knowledge Indexer (mcp-link-library)

**The Universal Search & Retrieval Engine for the Workforce Nexus.**

The **Librarian** (`mcp.py`) is a specialized MCP server responsible for indexing, storing, and retrieving knowledge from heterogeneous sources. In v3.5.0, it includes the **ATP Sandbox** for secure execution of agent-driven logic, **GUI Daemon Mode** for background service operation, and **Version Health Monitoring** for operational awareness.

## 🚀 Quick Start (Suite Mode)

The Librarian is automatically registered and monitored by the Dashboard:
```bash
../nexus.sh
```

**Standalone Start:**
```bash
python3 mcp.py --server
```

---

## 🌟 Capabilities (v3.5.0)

### 1. Universal Indexing (v3.0)
Deep content parsing for Documents (`PDF`, `DOCX`, `XLSX`) and Images (`EXIF`).
- **Optimization**: Server-side extraction returns only relevant JSON paths, reducing token bloat by 80%.

### 2. ATP Sandbox & Security
Includes the `ATPSandbox` layer to protect the host environment:
- **AST Guards**: Blocks `type()`, `getattr()`, and class-escape vectors.
- **Portability**: Uses deterministic wrappers to prevent infrastructure hallucinations.

### 3. Self-Healing & Diagnosis
- **`check_health`**: Audits Python dependencies and database integrity.
- **`update_dependencies`**: One-click recovery via the Nexus Dashboard.

### 4. Zero-Token Filtering
- **Paginated Lists**: capped at 50 results to prevent context saturation.
- **Deep Search**: Returns snippets instead of full documents for efficiency.

### 5. GUI Daemon Mode (v3.5.0+)
- **Background Service**: Flask bridge supports `--daemon` for unattended operation.
- **Process Management**: PID tracking and `--status` / `--stop` commands for lifecycle control.
- **Default Foreground**: No args = blocking server (backward compatible).

### 6. Version Health Monitoring (v3.5.0+)
- **Drift Detection**: `/version-health` endpoint compares source vs installed versions.
- **Dashboard Integration**: React UI displays version status badge with repair recommendations.
- **Dual-Interval Polling**: Optimized refresh rates for responsive UI without network overhead.

---

## 🛠️ Global Command Reference

| Command | Action |
| :--- | :--- |
| `mcp-librarian --search X` | Search the knowledge base for X. |
| `mcp-librarian --add Y` | Index a new URL or local file. |
| `mcp-librarian --list` | List all indexed resources (summarized). |

---

## 🔄 Drift Lifecycle Integration (v3.5.0+)

The Librarian integrates with the Drift Lifecycle system:
- **Knowledge Persistence**: Maintains indexed resources across deployments
- **Safe Indexing**: Real-time watcher prevents knowledge loss during drift
- **Multi-Deployment**: Supports indexing across core and forged servers
- **Version Awareness**: Automatic drift detection and repair recommendations via health monitoring

See main repo: [Drift Lifecycle System](../DRIFT_LIFECYCLE_OUTCOMES.md)

---

## 📝 Metadata
* **Status**: Production Ready (v3.5.0)
* **Released**: 2026-03-03
* **Author**: l00p3rl00p
* **Part of**: The Workforce Nexus Suite
* **Mission Score**: 100% ✅ (GUI Reliability + Operational Awareness complete)
