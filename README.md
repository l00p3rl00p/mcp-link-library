# MCP Link Library

A quick, flexible link library with CLI management.

## Features

- Add links with automatic metadata extraction
- Categorize links
- Search and filter links
- Activate/Deactivate links
- Simple CLI interface

## Installation

```bash
pip install .
```

## Usage

### 🚀 Workforce Integration
The Librarian is part of the Git-Packager suite.
```bash
# Bootstrap the entire workforce suite
mcp --bootstrap

# Check presence of sibling tools (Surgeon, Observer, Activator)
mcp --check
```

### Add a Link
```bash
mcp --add https://docs.claude.com --categories development ai
```

### List Links
```bash
# List all active links
mcp --list

# List links in a specific category
mcp --list --category development

# Search links
mcp --list --search claude
```

### Manage Links
```bash
# Delete a link by ID
mcp --delete 3

# Update a link
mcp --update 4 --url https://newurl.com --categories tech

# Deactivate/Activate a link
mcp --deactivate 5
mcp --activate 5
```

## 🤝 Git-Packager Workforce Suite

This tool is the **Librarian (Knowledge)** for the complete four-component workforce ecosystem:

| Tool | Persona | Purpose |
| --- | --- | --- |
| **mcp-injector** | The Surgeon | Safely manage MCP server configs in IDE JSON files |
| **mcp-server-manager** | The Observer | Discover, track, and monitor health of all MCP servers |
| **repo-mcp-packager** | The Activator | Install, package, and update MCP servers with automation |
| **mcp-link-library** | The Librarian | Curated knowledge base and document engine for AI tools |

### Integrated Benefits
* **Lifecycle Awareness**: Lifecycle updates in the Activator automatically refresh Librarian documents.
* **Health Diagnostics**: The `verify.py` script allows the Observer to monitor document index health.
* **Universal Search**: The Librarian provides the knowledge "fuel" for AI tools configured by the Surgeon.

## License

MIT License
