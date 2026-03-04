# MCP Librarian: The Knowledge Hub (mcp-link-library)

**The Universal Search & Retrieval Engine for the Workforce Nexus.**

The **Librarian** (`mcp.py`) is a specialized MCP server responsible for indexing, storing, and retrieving knowledge. It features an **ATP Sandbox** for secure execution and a **Named Stacks** context system for organizing knowledge by project or theme.

---

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

## 🌟 Capabilities

### 1. Universal Indexing & Parsing
Deep content parsing for Documents (`PDF`, `DOCX`, `XLSX`) and Images.
- **Optimization**: Server-side extraction returns only relevant JSON paths, reducing token bloat by 80%.

### 2. Named Stacks (Knowledge Contexts)
Organize your research into isolated, named contexts.
- **Project Isolation**: Group resources into "stacks" (e.g., 'physics-research', 'legal-docs').
- **Contextual Search**: Query specific stacks to prevent cross-contamination of results.

### 3. ATP Sandbox & Security
The `ATPSandbox` layer protects the host environment during agent-driven logic execution.
- **AST Guards**: Blocks `type()`, `getattr()`, and class-escape vectors.
- **Safety Protocol**: Mandates strictly deterministic processing of agent logic.

### 4. Zero-Token Filtering
- **Paginated Discovery**: Lists and categories are capped to prevent context saturation.
- **Deep Search**: Returns intelligent snippets instead of full documents.

---

## 🛠️ Global Command Reference

| Command | Action |
| :--- | :--- |
| `mcp-librarian --search X` | Search the knowledge base for X. |
| `mcp-librarian --add Y` | Index a new URL or local file. |
| `mcp-librarian --list` | List all indexed resources (summarized). |
| `mcp-librarian --stacks` | List all named knowledge contexts. |

---

## 🔄 Drift Lifecycle Integration

The Librarian integrates with the Drift Lifecycle system:
- **Persistence**: Maintains indexed resources (SQLite) across all suite deployments.
- **Auto-Watcher**: Real-time re-indexing of documents at server startup.
- **Version Awareness**: Unified health monitoring via the Nexus Dashboard.

---

## 📝 Metadata
* **Status**: 🟢 Production Ready (v3.4.2)
* **Part of**: The Workforce Nexus Suite
* **Mission Confidence**: 100% ✅
