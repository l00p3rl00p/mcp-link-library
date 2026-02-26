# Changelog - MCP Librarian (mcp-link-library)

## [3.4.0] - 2026-02-26

### Added
- **Named Stacks**: Resources can now be organized into isolated named knowledge contexts ("stacks") — like NotebookLM projects. Use `stack='gravity-research'` when adding resources to keep them grouped.
- **`list_stacks` tool**: Returns all stacks that have at least one active resource. Call this first when browsing without a specific stack in mind.
- **`get_categories` tool**: Browses first and second-order categories within a stack (or across all stacks), with counts.
- **`stack` param on `add_resource`**: Resources are filed into a named stack (defaults to `'default'`).
- **`stack` param on `search_knowledge_base`**: Scope searches to a single stack or search all stacks by omitting the param.
- **DB migration**: Existing `knowledge.db` databases gain a `stack` column automatically on first launch (non-destructive `ALTER TABLE`).
- **CLI**: `--stack` flag for `--add`, `--list-stacks` flag to enumerate stacks from the command line.

### Changed
- `list_links()` now returns a 7-tuple `(id, url, title, domain, categories, is_active, stack)`.
- Version bumped `3.3.1 → 3.4.0`.

## [3.3.4] - 2026-02-25

### Fixed
- **Auto-Create Documents Directory**: `verify.py` now auto-creates the `documents/` directory on first health check so users never see a false-negative ❌ on a fresh install.
- **Non-Fatal Downgrade**: Missing `documents_dir` is now a `warning` (not `error`) — the DB scan roots are the real index; a missing static folder is cosmetic.



### Changed
- **Suite Version Sync**: Aligned component and docs to Nexus `v3.3.1`.

## [3.2.1] - 2026-02-19

### Improvements
- **Suite Sync**: Version alignment with Nexus v3.2.1.

### Security
- `ATPSandbox`: Blocked `type()` and `getattr()` class-escape vectors at AST level. Regression baseline: 9 attack vectors confirmed blocked.

### Fixes
- `verify_universal_files.py`: Added `--skip-live` flag + `communicate(timeout=5)` — prevents indefinite hang in CI.

---

## [2.0.0] - 2026-02-18

### 🚨 Major Security & Logic (ATP)
- **ATPSandbox**: Implemented a hardened Python sandbox for secure, isolated agent logic execution.
- **Deterministic Wrapper**: New `mcp_wrapper` with standardized input/output schemas to eliminate infrastructure hallucinations.
- **Data Projection**: Added server-side extraction (JSON path) to reduce token bloat by returning only requested fields.
- **Token Estimation**: Built-in heuristic character counting (`len/4`) for real-time cost transparency.

### 📚 Knowledge Management
- **Universal File Support**: Deep content indexing for PDF, Excel, Word, and Images (EXIF metadata).
- **Zero-Token Filtering**: Paginated resource lists (capped at 50) and server-side search to prevent context saturation.
- **Self-Healing**: `check_health` tool for automated dependency audit and recovery.

---

## [1.0.0] - 2026-02-09
- Initial release of core MCP shared library.
- Basic knowledge base indexing.
- Cross-repo utility foundation.

---

## [3.3.5] - 2026-02-25

### Added
- **Auto-Watcher on Launch (GAP-R3)**: `MCPServer._auto_start_watcher()` now fires at server startup, watching `documents/` via `NexusWatcher` (`PollingObserver`). If `watchdog` is not installed, the server starts normally with a clear stderr hint. Closes the core mission gap: "memory always accessible, not just after manual Quick Index".

### Fixed
- No breaking changes. Existing `start_watcher` MCP tool still available for manual watch-path additions.

---
*Status: Production Ready (v3.3.5)*

