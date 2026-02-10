# The Librarian: Features & Commands

## Overview
**The Librarian (`mcp-link-library`)** is the knowledge engine of the Workforce Nexus. It turns any folder into a searchable, queryable database that AI agents can read.

## Features

### 1. 📂 Local File Indexing
*   **Recursive Scan**: Indexes `.txt`, `.md`, `.py`, `.js`, `.pdf` (text-based) files.
*   **Smart Ignoring**: Respects `.gitignore` to avoid indexing secrets or dependencies (`node_modules`).
*   **Metadata Extraction**: Captures file paths, content hashes, and timestamps.

### 2. 🗣️ Included MCP Server
*   **Standard Protocol**: Implements the Model Context Protocol (JSON-RPC over stdio).
*   **Resources**: Exposes indexed files as `file://` resources.
*   **Tools**: Provides `search_knowledge_base` tool for semantic or keyword search.

### 3. 🔐 Secure Storage
*   **Centralized DB**: Stores all index data in `~/.mcp-tools/mcp-server-manager/knowledge.db` (The Nexus).
*   **No Pollution**: Doesn't create `.db` files in your project folders.

## Command Reference

### Indexing
```bash
# Index the current directory
python mcp.py --index .

# Index a specific folder
python mcp.py --index /path/to/docs
```

### Management
```bash
# List all indexed files
python mcp.py --list

# Filter by category
python mcp.py --list --category code

# Search for a file or link
python mcp.py --search "api"
```

### Server Mode
```bash
# Start the MCP JSON-RPC server (used by Claude/Cursor)
python mcp.py --server
```

### Diagnostics
```bash
# Check connection to the Nexus suite
python mcp.py --check

# Bootstrap the entire suite
python mcp.py --bootstrap
```

---
**Part of the Workforce Nexus**
*   **The Surgeon**: `mcp-injector` (Configuration)
*   **The Observer**: `mcp-server-manager` (Dashboard)
*   **The Activator**: `repo-mcp-packager` (Automation)
*   **The Librarian**: `mcp-link-library` (Knowledge)
