#!/bin/bash
# Double-click to sync data from Sibling tools (Observer/Injector)
echo "Pulling metadata from sibling tools..."
mcp-librarian --index-suite
read -p "Press any key to exit..."
