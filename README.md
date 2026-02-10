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

## Requirements

- Python 3.7+
- requests
- beautifulsoup4

## License

MIT License
