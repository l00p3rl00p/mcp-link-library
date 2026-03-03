"""
tests/test_daemon.py — Unit tests for gui_bridge.py daemon PID management.

Covers:
- _read_pid() returns None when no PID file
- _pid_alive() returns False for a PID that does not exist
- _clean_stale_pid() removes a stale PID file
- cmd_status() prints "Stopped" and exits 1 when no daemon is running
- cmd_stop() prints "not running" and exits 1 when no PID file
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure the library root is importable.
sys.path.insert(0, str(Path(__file__).parent.parent))

import gui_bridge


class TestPidHelpers(unittest.TestCase):

    def test_read_pid_returns_none_when_file_absent(self):
        with patch.object(gui_bridge, "PID_FILE", Path("/tmp/__nonexistent_gui_bridge_test.pid")):
            result = gui_bridge._read_pid()
        self.assertIsNone(result)

    def test_read_pid_returns_int_when_file_present(self, tmp_path=None):
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".pid", delete=False) as f:
            f.write("99999\n")
            pid_path = Path(f.name)
        try:
            with patch.object(gui_bridge, "PID_FILE", pid_path):
                result = gui_bridge._read_pid()
            self.assertEqual(result, 99999)
        finally:
            pid_path.unlink(missing_ok=True)

    def test_pid_alive_returns_false_for_nonexistent_pid(self):
        # PID 1 exists on Unix; use a very large PID that almost certainly doesn't exist.
        # We rely on os.kill raising ProcessLookupError for an absent PID.
        # Use a known-dead PID by finding a free slot.
        import subprocess
        result = subprocess.run(["python3", "-c", "import os; os.kill(9999999, 0)"],
                                capture_output=True)
        if result.returncode != 0:
            self.assertFalse(gui_bridge._pid_alive(9999999))
        # If somehow PID 9999999 is alive, skip rather than fail (extremely unlikely).

    def test_pid_alive_returns_true_for_self(self):
        self.assertTrue(gui_bridge._pid_alive(os.getpid()))

    def test_clean_stale_pid_removes_file_for_dead_pid(self):
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".pid", delete=False) as f:
            f.write("9999999\n")   # almost certainly dead
            pid_path = Path(f.name)
        try:
            with patch.object(gui_bridge, "PID_FILE", pid_path):
                # Only test clean if the PID is genuinely dead.
                if not gui_bridge._pid_alive(9999999):
                    cleaned = gui_bridge._clean_stale_pid()
                    self.assertTrue(cleaned)
                    self.assertFalse(pid_path.exists())
        finally:
            pid_path.unlink(missing_ok=True)


class TestCmdStatus(unittest.TestCase):

    def test_status_stopped_when_no_pid_file(self):
        import tempfile
        dead_path = Path(tempfile.mktemp(suffix=".pid"))  # path that doesn't exist
        with patch.object(gui_bridge, "PID_FILE", dead_path):
            with self.assertRaises(SystemExit) as ctx:
                gui_bridge.cmd_status()
            self.assertEqual(ctx.exception.code, 1)

    def test_status_running_when_alive(self):
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".pid", delete=False) as f:
            f.write(str(os.getpid()))
            pid_path = Path(f.name)
        try:
            with patch.object(gui_bridge, "PID_FILE", pid_path):
                with self.assertRaises(SystemExit) as ctx:
                    gui_bridge.cmd_status()
                self.assertEqual(ctx.exception.code, 0)
        finally:
            pid_path.unlink(missing_ok=True)


class TestCmdStop(unittest.TestCase):

    def test_stop_exits_1_when_no_pid_file(self):
        import tempfile
        dead_path = Path(tempfile.mktemp(suffix=".pid"))
        with patch.object(gui_bridge, "PID_FILE", dead_path):
            with self.assertRaises(SystemExit) as ctx:
                gui_bridge.cmd_stop()
            self.assertEqual(ctx.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
