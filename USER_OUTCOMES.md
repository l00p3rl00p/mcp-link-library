# User Outcomes - Nexus Librarian (mcp-link-library)

This document defines success for the **Nexus Librarian**, the component responsible for knowledge persistence, RAG (Retrieval-Augmented Generation), and deep resource linking.

---

## 🔗 Canonical Outcomes & Mission (Project Scope)

This repo-level `USER_OUTCOMES.md` is subordinate to the canonical [Workforce Nexus Mission Statement](/Users/almowplay/Developer/Github/mcp-creater-manager/USER_OUTCOMES.md).

## Core Mission Statement - READ ONLY- NEVER EDIT

The mission is to empower users and agents with a persistent, searchable 'Source of Truth' for all project-related knowledge. By indexing files, URLs, and repositories into an ATP-hardened, token-optimized library, it enables industrial-speed retrieval and zero-friction resource linking, ensuring the ecosystem's memory is always accessible and secure.

### The Rule of Ones: The LIBRARIAN System Architecture
The Nexus Librarian serves as the central cognitive memory of the ecosystem, anchored in:
- **One Install Path:** Deployed as a core, high-availability service within the Unified Nexus.
- **One Entry Point:** Unified access via the `nexus-librarian` MCP server tools and the "Librarian" tab in the Nexus Commander GUI.
- **One Status:** Clear visibility into index health, watcher status, and resource counts.
- **One Log:** Comprehensive indexing logs and sub-agent execution trails (ATP logs).

---

## 📋 Table of Contents
1. [Successful Outcomes](#-successful-outcomes)
2. [High-Fidelity Signals](#-high-fidelity-signals)
3. [Design Guardrails](#-design-guardrails)

---

## 🔍 Successful Outcomes (Nexus Librarian)

As a user, I want:

### 1. Robust Knowledge Discovery
* **Deep Search**: Query indexed files and URLs using natural language or keywords to find relevant technical resources.
* **Universal Linker**: Automatically generate symbolic links or references to indexed materials so agents can "attach" knowledge to a conversation.
* **Web Integration**: Add web URLs or entire public repositories to the knowledge base with a single command or GUI action.

### 2. High-Fidelity Retrieval (ATP Hardening)
* **Zero-Token Filtering**: Process large datasets (filtering, mapping) within the Librarian's execution environment to avoid context bloat in the LLM.
* **AST-Based Security**: Execute code-based filtering queries only in a hardened sandbox that blocks malicious attribute access.
* **Fragment Retrieval**: Only return the most relevant chunks of a document to the agent, keeping raw high-volume data isolated.

### 3. Resource Resilience
* **Offline Access**: Persist indexed content so it remains accessible even if the source URL or file path becomes temporarily unavailable.
* **Automatic Watcher**: Detect changes in watched directories and re-index content in real-time to ensure the knowledge base never rots.

### 4. Standalone & Integrated Utility
* **Suite Sync**: Shares its index with the Observer dashboard for visual knowledge management.
* **Standalone Mode**: Can be deployed as a standard MCP server in any environment without requiring the full Nexus GUI.

### 2. Intelligent Discovery & Autonomy
* **Autonomous Bootstrap**: The Activator can fetch the entire Workforce Nexus suite from GitHub, allowing it to move from "standalone script" to "suite architect" without local source siblings.
* **Inventory Awareness**: The installer identifies all available components (Python, Node, Docker) and allows selective installation to prevent "package bloat."
* **Local Source Parity**: In developer mode, the tool installs the application *exactly as it exists* in the local root, respecting custom modifications.

### 3. Trust & Transparency
* **Surgical Integrity**: The `uninstall` command surgically reverses only the changes it made, ensuring the host is returned to its pre-installation state.
* **Before/After Verification**: Clear reports allow the operator (human or agent) to verify every change. No stealth modifications to PATH or Registry.

### 4. Universal Observability
* **Visual Status**: The user can see the health and connection status of all Nexus components (Observer, Librarian, Injector, Activator) in a single dashboard.
* **Graceful Degradation**: The system functions even if components are missing, clearly indicating what is available vs. what needs installation.
* **Standalone Resilience**: The library functions as a standard MCP server even when isolated from the Nexus suite and missing optional dependencies (PDF/Excel support degradation).

### 5. Resilient Lifecycle
* **Atomic Rollback**: If an installation fails at any step, the system automatically reverts to a clean state, leaving no partial artifacts.
* **Safe Upgrades**: The `mcp-activator --sync` command provides a unified update loop, ensuring all central tools stay synchronized with the latest security and feature patches.
* **Context-Locked Execution**: Entry points carry their own venv and PYTHONPATH, ensuring they work regardless of the user's active terminal environment.

---

## 🚀 Roadmap to 100% Compliance

To fully align with these outcomes, the following enhancements are planned:

*   **GUI Reliability (Target 95%+)**: Transition GUI from a blocking process to a background service with PID management.
*   **Librarian Synergy**: Implement a dynamic watcher so the Librarian indexes changes in real-time, not just on installation.
*   **Operational Awareness**: Add "version health" checks to the GUI dashboard to visually signal when a `--sync` is required.

### 2026-02-11 Alignment Update
* **Injector Startup Detect**: Added startup detection/prompt flow for common IDE clients, including `claude`, `codex`, and `aistudio` (plus `google-antigravity` alias).
* **Package-Created Component Injection Policy**: If full Nexus components are detected (`~/.mcp-tools/bin`), the injector prompts injection only for components that are **actual MCP servers over stdio** (currently `nexus-librarian`). Other Nexus binaries (e.g. `mcp-activator`, `mcp-observer`) are CLIs and should not be injected into MCP clients.
* **Tier-Aware GUI Control Surface**: GUI command widgets now map to command catalog behavior with visual unchecked state for unsupported tier actions.
* **Central-Only Uninstall Policy**: Full wipes only touch approved central locations (e.g. `~/.mcp-tools`, `~/.mcpinv`, and the Nexus PATH block). No disk scans or directory-tree climbing during uninstall.
* **Uninstall Safety + Diagnostics**: Uninstall now prints an explicit deletion plan and requires confirmation (unless `--yes`). Added `--verbose` and `--devlog` (JSONL) with 90-day retention for diagnostics.
* **Bootstrap Safety Policy**: Workspace detection avoids filesystem crawling (checks only `cwd` + script-sibling workspace). If a workspace `.env` is present, the installer warns about potential conflicts with the central install.

---

## 🚥 High-Fidelity Signals

* **Success**: `.librarian/manifest.json` correctly lists all artifacts, and `verify.py` reports `[VERIFIED]` for all items.
* **Failure**: Encountering an interactive prompt in `--headless` mode.
* **Success**: Running `uninstall.py` removes the `# Nexus Block` from `.zshrc` without deleting other aliases (legacy installs may still contain `# Shesha Block`).

---

## 🛡 Design Guardrails

* **No Sudo**: Reject any feature that requires global `sudo` permissions if a local `.venv` alternative exists.
* **No Unmanaged Overwrites**: Reject any "auto-update" feature that replaces local configuration without a manifest-backed snapshot.
* **Respect Local Code**: Treatment of the current repository state as the "source of truth." Never overwrite local changes with upstream templates.
