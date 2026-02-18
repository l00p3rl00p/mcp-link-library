# MCP Librarian: The Knowledge Indexer (mcp-link-library)

**The Universal Search & Retrieval Engine for the Workforce Nexus.**

The **Librarian** (`mcp.py`) is a specialized MCP server responsible for indexing, storing, and retrieving knowledge from heterogeneous sources. It provides agents with "Deep Search" capabilities, allowing them to find needles in haystacks across file formats.

---

## 🌟 Core Capabilities

### 1. Universal File Support (v2.0)
The Librarian can natively parse and index content from:
- **PDF** (`.pdf`): Full text extraction via `pypdf`.
- **Excel** (`.xlsx`): Cell-by-cell data extraction via `openpyxl`.
- **Word** (`.docx`): Paragraph text extraction via `python-docx`.
- **Images** (`.png`, `.jpg`): Metadata and EXIF extraction via `Pillow`.

### 2. Deep Content Search
Unlike simple file finders, the Librarian indexes the **contents** of files.
- Query: "Mar 6, 2025"
- Result: Finds `invoice.pdf` because the date is inside the text, not the filename.

### 3. Self-Healing Architecture
The Librarian includes a built-in doctor (`check_health`) that:
- Audits its own Python environment.
- Detects missing optional dependencies (e.g., if `openpyxl` is missing).
- Can self-request updates via `update_dependencies` (Agent-driven `pip install`).

### 4. Standalone Resilience
- **Modular**: Works independently of the full Nexus suite.
- **Graceful Degradation**: If optional parsers are missing, it falls back to basic metadata indexing without crashing.

---

## 🛠️ Usage

### CLI Mode (Human)
```bash
# Add a file/url
python3 mcp.py --add "file:///path/to/doc.pdf" --categories "financial"

# Search
python3 mcp.py --search "invoice"

# List all
python3 mcp.py --list
```

### MCP Server Mode (Agent)
```bash
python3 mcp.py --server
```
*Exposes `search_knowledge_base`, `add_resource`, `check_health`, etc. over JSON-RPC stdio.*

---

## 📚 API (MCP Tools)

| Tool | Description | Optimization |
| :--- | :--- | :--- |
| `search_knowledge_base` | Filter results by query string | **Server-Side Filtering** (Zero-Token) |
| `add_resource` | Download, extract, and index content | **One-Shot Logic** (Chatty Reduction) |
| `check_health` | detailed status of dependencies | **Self-Diagnosis** |
| `update_dependencies` | Install missing Python packages | **Self-Healing** |

---

## 📝 Metadata
* **Status**: Production Ready (Verified v2.0)
* **Author**: l00p3rl00p
* **Part of**: The Nexus Workforce Suite
