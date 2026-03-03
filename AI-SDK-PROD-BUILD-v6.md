# AI-SDK-PROD-BUILD-v6: GUI Reliability + Operational Awareness

**Version**: 6.0
**Date**: 2026-03-02
**Status**: ACTIVE
**Mission Score Target**: 87% → 100%
**Closes Roadmap**: GUI Reliability (95%+) · Operational Awareness (version health)

---

## L3 — Contract

This contract covers two tightly-coupled shippable units that together close the
remaining 13% gap in `USER_OUTCOMES.md`:

| Unit | Name | Files Touched |
|---|---|---|
| Unit 2 | GUI Background Service + PID Management | `gui_bridge.py`, `tests/` |
| Unit 3 | Version Health Endpoint + Dashboard Indicator | `gui_bridge.py`, `App.tsx`, `tests/` |

**Human Promise** (one sentence each):

- Unit 2: "I run `mcp-nexus-gui --daemon` and the GUI bridge starts silently in the
  background; I can check its status with `--status` and stop it with `--stop` — no
  terminal stays blocked."

- Unit 3: "The Nexus dashboard shows a clear warning badge whenever the installed
  Librarian version is out of sync with the source, and tells me exactly which command
  to run to fix it."

---

## Q1 — Trigger (Front Door)

### Unit 2 Trigger
```bash
python3 gui_bridge.py --daemon    # starts as background process, exits terminal immediately
python3 gui_bridge.py --status    # prints: Running (PID 12345) or Stopped
python3 gui_bridge.py --stop      # sends SIGTERM to daemonized process
python3 gui_bridge.py             # still works as blocking foreground server (unchanged)
```

**Acceptance**: `--daemon` exits with code 0 and writes `~/.mcpinv/gui_bridge.pid`.
Terminal is NOT blocked. A follow-up `--status` call returns `Running`.

### Unit 3 Trigger
```bash
curl -s http://127.0.0.1:5001/version-health | python3 -m json.tool
```

Expected response shape:
```json
{
  "source_version": "3.4.0",
  "installed_version": "3.4.0",
  "needs_repair": false,
  "reason": null,
  "action": null
}
```

When versions differ:
```json
{
  "source_version": "3.5.0",
  "installed_version": "3.4.0",
  "needs_repair": true,
  "reason": "Source version (3.5.0) is ahead of installed (3.4.0).",
  "action": "Run 'mcp-activator --repair' to sync the installed runtime."
}
```

Dashboard shows a `⚠️ Repair Needed` badge next to the version pill when
`needs_repair: true`, with the exact `action` command surfaced as tooltip/text.

---

## Q2 — Evidence (Doctor)

### Unit 2 Evidence
```bash
# 1. Start daemon
python3 /Users/almowplay/Developer/Github/mcp-creater-manager/mcp-link-library/gui_bridge.py --daemon
# Expected: prints "GUI Bridge daemon started (PID <N>)" then exits immediately

# 2. Verify PID file written
cat ~/.mcpinv/gui_bridge.pid
# Expected: integer PID

# 3. Confirm process alive
python3 gui_bridge.py --status
# Expected: "Running (PID <N>)"

# 4. Confirm bridge responding
curl -s http://127.0.0.1:5001/health
# Expected: {"status": "ok"}

# 5. Stop daemon
python3 gui_bridge.py --stop
# Expected: "GUI Bridge stopped."

# 6. Confirm stopped
python3 gui_bridge.py --status
# Expected: "Stopped"

# 7. PID file cleaned up
test ! -f ~/.mcpinv/gui_bridge.pid && echo "PID file removed" || echo "FAIL: stale PID"
```

### Unit 3 Evidence
```bash
# 1. Health endpoint returns version data
curl -s http://127.0.0.1:5001/version-health | python3 -m json.tool
# Expected: JSON with source_version, installed_version, needs_repair keys

# 2. ATP sandbox verification (zero-LLM)
python3 -c "
import json, subprocess, sys
r = subprocess.run(['curl','-s','http://127.0.0.1:5001/version-health'], capture_output=True, text=True)
d = json.loads(r.stdout)
assert 'needs_repair' in d, 'missing needs_repair'
assert 'source_version' in d, 'missing source_version'
assert 'installed_version' in d, 'missing installed_version'
print('[VERIFIED] /version-health returns required keys')
"

# 3. Unit tests pass
python3 -m pytest tests/test_version_health.py -v
python3 -m pytest tests/test_daemon.py -v
```

**Doctor command** (existing, unchanged):
```bash
python3 /Users/almowplay/Developer/Github/mcp-creater-manager/mcp-link-library/verify.py
```

---

## L4 — Pre-Flight (Four-Team Review)

### 🔴 Risk Team
- **Race condition**: `--daemon` forks; parent must wait for child to bind port before
  exiting or `--status` immediately after `--daemon` would report "Stopped." Fix: child
  signals readiness via PID file write; parent polls PID file (max 3s, 100ms interval).
- **Stale PID file**: If process dies unexpectedly, `~/.mcpinv/gui_bridge.pid` remains.
  `--status` must validate the PID is actually alive (`os.kill(pid, 0)`) before reporting
  "Running." If stale, auto-clean file and report "Stopped (stale PID cleaned)."
- **`needs_repair` false positive**: If `~/.mcp-tools/mcp-link-library/mcp.py` does not
  exist (fresh install, no mirror yet), do NOT flag repair-needed. Return `installed_version: null`
  and `needs_repair: false` with `reason: "Not installed centrally yet"`.
- **`needs_repair` missing binary**: If `~/.mcp-tools/bin/mcp-librarian` is absent but
  installed version matches, still flag repair (binary missing = broken state).

### 🟡 Delivery Team
- `--daemon` uses `os.fork()` + double-fork (POSIX daemon idiom) to fully detach from
  the terminal, prevent zombie processes, and release the controlling terminal.
- PID file path: `~/.mcpinv/gui_bridge.pid`. Directory auto-created if absent.
- Version read: extract `__version__ = "X.Y.Z"` via regex from source `mcp.py` and
  installed `~/.mcp-tools/mcp-link-library/mcp.py`. No `import` needed (avoids side effects).
- `App.tsx`: add `versionHealth` state, fetched from `/version-health` every 30s.
  Render a `badge-danger` badge ("⚠️ Repair Needed") in the header when `needs_repair: true`.

### 🔵 Framework Team
- `--daemon` must NOT break the existing `if __name__ == '__main__': app.run(...)` path.
  Guard with argparse. Foreground mode is the default.
- No new Python dependencies. Uses only stdlib: `os`, `signal`, `sys`, `re`, `argparse`.
- GUI Call-Chain Standard (2026-02-23): the new version health badge is purely read-only
  (no button). No `fireEvent` test required. However a render test IS required confirming
  the badge renders when `needs_repair: true`.
- GUI Starts Last Standard (2026-02-25): `--daemon` must check `ready.lock` or bin dir
  exists before starting. If binaries missing, start in degraded mode with log entry +
  suggestion (not a hard failure).
- Dual-State Capability Check (2026-02-21): version comparison must check BOTH workspace
  and installed mirror; display whichever is actually running.

### 🟣 Coherence Team
- The Dashboard header currently shows: `[Posture badge] [Online badge]`. After Unit 3,
  it becomes: `[Posture badge] [Version Health badge] [Online badge]`.
- "Repair Needed" message must include the exact command string `mcp-activator --repair`
  so the user never has to guess.
- `--status` output must be machine-readable for scripting:
  `Running (PID 12345)` → exit code 0, `Stopped` → exit code 1.
- No silent failures: every error path in `--daemon`/`--stop`/`--status` must print a
  human-readable message and exit with a non-zero code on failure.

---

## L5 — Implementation Matrix

### Unit 2: `gui_bridge.py` daemon mode

| File | Change | Exact Logic |
|---|---|---|
| `gui_bridge.py` | Add `import argparse, signal, time` at top | stdlib only |
| `gui_bridge.py` | Add `PID_FILE = Path.home() / ".mcpinv" / "gui_bridge.pid"` constant | Fixed path |
| `gui_bridge.py` | Add `def _write_pid(pid)` | Creates `~/.mcpinv/`, writes str(pid) to PID_FILE |
| `gui_bridge.py` | Add `def _read_pid()` | Returns int(PID_FILE.read_text()) or None if file absent |
| `gui_bridge.py` | Add `def _pid_alive(pid)` | `os.kill(pid, 0)` → True; `ProcessLookupError` → False |
| `gui_bridge.py` | Add `def _daemonize()` | Double-fork POSIX idiom; child calls `_write_pid(os.getpid())` then returns to run Flask |
| `gui_bridge.py` | Add `def cmd_start_daemon()` | Calls `_daemonize()`, then `app.run(...)` in child |
| `gui_bridge.py` | Add `def cmd_stop()` | Reads PID, sends SIGTERM, removes PID_FILE |
| `gui_bridge.py` | Add `def cmd_status()` | Reads PID, checks alive, prints + exits 0/1 |
| `gui_bridge.py` | Replace `if __name__` block | argparse: `--daemon`, `--stop`, `--status`; default = foreground |

### Unit 3: `/version-health` endpoint + dashboard badge

| File | Change | Exact Logic |
|---|---|---|
| `gui_bridge.py` | Add `def _read_version(path)` | `re.search(r'__version__\s*=\s*["\']([^"\']+)', text)` on file content |
| `gui_bridge.py` | Add `@app.route('/version-health')` | Reads source + installed versions; compares; returns JSON with 5 keys |
| `App.tsx` | Add `versionHealth` state (`useState<any>(null)`) | Initialized null |
| `App.tsx` | Add fetch to `/version-health` in `useEffect` every 30s | Separate `setInterval` with 30000ms |
| `App.tsx` | Add `VersionHealthBadge` inline component | Renders nothing if `null`; renders `badge-warning` "Up to Date" or `badge-danger` "⚠ Repair Needed" with `title={action}` tooltip |
| `App.tsx` | Insert badge in header between posture and online badges | Preserves existing layout |

### Tests

| File | What it proves |
|---|---|
| `tests/test_daemon.py` | `--status` returns "Stopped" when no PID file; `_pid_alive` returns False for fake PID |
| `tests/test_version_health.py` | `_read_version` extracts correct version from mock file content; endpoint returns all 5 keys; `needs_repair=True` when versions differ |

---

## Guardrails

- GR-DAEMON-NO-ZOMBIE: Use double-fork POSIX idiom to prevent zombie processes. First fork exits immediately; second fork detaches from session.
- GR-PID-STALE-CLEAN: `--status` and `--stop` must handle stale PID file gracefully. Stale = file exists but `os.kill(pid, 0)` raises `ProcessLookupError`. Auto-remove stale file.
- GR-NO-REPAIR-FALSE-POSITIVE: If installed mirror does not exist, `needs_repair` MUST be `false`. Only flag repair when installed version is behind source version OR when bin is missing despite version match.
- GR-GUI-STARTS-LAST: Apply `gui-starts-last` standard. `--daemon` checks bin directory before starting Flask. If missing, start in degraded mode with actionable suggestion logged.
- GR-NO-SHELL-INJECTION: All subprocess calls use list-based argv. `shlex.split()` already applied to `start_cmd`.
- GR-VERSION-READ-NO-IMPORT: Extract version via `re.search` on file text. Never `import` target files (avoids side-effects and circular imports).
- GR-BADGE-TOOLTIP: When `needs_repair: true`, dashboard badge MUST display exact `action` string as accessible `title` attribute so user can copy it.
- GR-EVIDENCE-FIRST: No unit is marked complete until `EVIDENCE.md` has the CLI output proving the feature transformed real data.
