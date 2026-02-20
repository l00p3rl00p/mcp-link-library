# Changelog - MCP Librarian (mcp-link-library)

## [3.3.1] - 2026-02-20

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
*Status: Production Ready (v3.3.1)*
