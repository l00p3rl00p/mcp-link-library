import sys
import json
import time
from pathlib import Path
import os

# Add current dir to path
sys.path.append(os.getcwd())
from mcp_wrapper import MCPWrapper

print("📉 Verifying Unit 2: Token Auditing in Protocol Wrapper...")

wrapper = MCPWrapper()
log_path = Path.home() / ".mcpinv" / "session.jsonl"

req = {
    "id": "audit-test-log",
    "method": "GET",
    "url": "https://jsonplaceholder.typicode.com/todos/1"
}

res = wrapper.call(req)

if not res.get("usage"):
    print("❌ Response missing 'usage' (Heuristic failed).")
    sys.exit(1)
else:
    print(f"✅ Response contained 'usage': {res['usage']}")

time.sleep(1)

with open(log_path, "r") as f:
    lines = f.readlines()
    last = json.loads(lines[-1])

meta = last.get("metadata", {})
if not meta.get("tokens"):
    print(f"❌ Log entry missing 'tokens' metadata: {meta}")
    sys.exit(1)

print(f"✅ Log Entry Verified: {meta['tokens']}")
print("🎉 Unit 2 Verified.")
