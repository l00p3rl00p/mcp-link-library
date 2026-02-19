
import subprocess
import sys
import json
import time
from pathlib import Path

# Create a dummy file with 2025 info
test_file = Path("2025_Projection.txt")
test_file.write_text("Projected revenue for 2025: $50M from AI integration.")

# Find mcp.py
mcp_py = Path("mcp.py").resolve()
if not mcp_py.exists():
    print("❌ mcp.py not found in current directory.")
    sys.exit(1)

# Start Librarian as a subprocess
try:
    print("🚀 Starting Librarian (mcp.py --server)...")
    process = subprocess.Popen(
        [sys.executable, str(mcp_py), "--server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0 # Unbuffered for real-time interaction
    )
    
    # helper for sending requests
    def send_request(method, params, req_id):
        req = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/call",
            "params": {
                "name": method,
                "arguments": params
            }
        }
        process.stdin.write(json.dumps(req) + "\n")
        process.stdin.flush()
        return process.stdout.readline()

    # 1. Add Resource
    print(f"📝 Adding resource: {test_file.resolve()}...")
    resp = send_request("add_resource", {"url": str(test_file.resolve()), "categories": "finance"}, 1)
    print(f"   Response: {resp.strip()}")

    # 2. Search
    print("🔍 Searching for '2025'...")
    resp = send_request("search_knowledge_base", {"query": "2025"}, 2)
    print(f"   Response: {resp.strip()}")
    
    # 3. Verify Log
    print("✅ Verify Log Entry in ~/.mcpinv/session.jsonl...")
    log_path = Path.home() / ".mcpinv" / "session.jsonl"
    found_command = False
    if log_path.exists():
        lines = log_path.read_text().splitlines()
        for line in lines[-20:]: # Check last 20 lines
            try:
                entry = json.loads(line)
                if entry.get("level") == "COMMAND" and "search_knowledge_base" in entry.get("message", ""):
                     print(f"   Found Log from Librarian: {line}")
                     found_command = True
            except:
                pass
    
    if found_command:
        print("✅ SUCCESS: Librarian tool call was logged to session registry.")
    else:
        print("❌ FAILURE: Librarian tool call NOT found in session logs.")
        
except Exception as e:
    print(f"❌ Error: {e}")
    if process:
        stdout, stderr = process.communicate()
        if stderr:
            print(f"Server STDERR:\n{stderr}")
finally:
    if process:
        process.terminate()
    if test_file.exists():
        test_file.unlink()
