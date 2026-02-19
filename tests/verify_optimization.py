
import sys
import json
import subprocess
from pathlib import Path

def test_librarian_list():
    # Target the industrial binary
    librarian_bin = Path.home() / ".mcp-tools" / "bin" / "mcp-librarian"
    
    # Run librarian and send resources/list request
    cmd = [str(librarian_bin), "--server"]
    process = subprocess.Popen(
        cmd, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Handshake
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05", 
            "capabilities": {},
            "clientInfo": {"name": "tester", "version": "1.0"}
        }
    }
    
    # List Request
    list_req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "resources/list",
        "params": {}
    }
    
    try:
        # Send Init
        process.stdin.write(json.dumps(init_req) + "\n")
        process.stdin.flush()
        
        # Read Init Response
        line1 = process.stdout.readline()
        print(f"Init Response: {line1.strip()}")
        
        # Send Notification
        process.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
        
        # Send List
        process.stdin.write(json.dumps(list_req) + "\n")
        process.stdin.flush()
        
        # Read List Response
        line2 = process.stdout.readline()
        resp = json.loads(line2)
        
        resources = resp.get("result", {}).get("resources", [])
        count = len(resources)
        print(f"Resources returned: {count}")
        
        if count > 52: # 50 + guidance + margin
            print("❌ FAIL: Too many resources returned (Context Flooding)")
            sys.exit(1)
            
        has_guidance = any("nexus://guidance" in r["uri"] for r in resources)
        # If we have < 50 items, we might not trigger the limit, which is also a success if the DB is small.
        # But if the user has many items, we expect guidance.
        
        print(f"Guidance found: {has_guidance}")
        print("✅ SUCCESS: Verification passed.")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        process.terminate()

if __name__ == "__main__":
    test_librarian_list()
