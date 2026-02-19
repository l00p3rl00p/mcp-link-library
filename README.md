# MCP Librarian: The Knowledge Indexer (mcp-link-library)

**The Universal Search & Retrieval Engine for the Workforce Nexus.**

The **Librarian** (`mcp.py`) is a specialized MCP server responsible for indexing, storing, and retrieving knowledge from heterogeneous sources. In v3.2.1, it includes the **ATP Sandbox** for secure execution of agent-driven logic.

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

## 🌟 Capabilities (v3.2.1)

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

---

## 🛠️ Global Command Reference

| Command | Action |
| :--- | :--- |
| `mcp-librarian --search X` | Search the knowledge base for X. |
| `mcp-librarian --add Y` | Index a new URL or local file. |
| `mcp-librarian --list` | List all indexed resources (summarized). |

---

## 📝 Metadata
* **Status**: Production Ready (v3.2.1)
* **Author**: l00p3rl00p
* **Part of**: The Workforce Nexus Suite
