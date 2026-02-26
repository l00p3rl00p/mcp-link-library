# Changelog - MCP Librarian (mcp-link-library)

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

