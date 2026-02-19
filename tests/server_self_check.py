
import sys
import json
import subprocess
from pathlib import Path

def main():
    server_script = Path("mcp.py").resolve()
    print(f"🏥 Spawning MCP Server for Health Check...")
    
    cmd = [sys.executable, str(server_script), "--server"]
    process = subprocess.Popen(
        cmd, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    try:
        # 1. Initialize
        process.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"}) + "\n")
        process.stdin.flush()
        process.stdout.readline() 

        # 2. Call check_health
        req = {
            "jsonrpc": "2.0", 
            "id": 2, 
            "method": "tools/call",
            "params": {
                "name": "check_health",
                "arguments": {} 
            }
        }
        process.stdin.write(json.dumps(req) + "\n")
        process.stdin.flush()
        
        line = process.stdout.readline()
        if not line:
            print("❌ No response from server")
            return

        resp = json.loads(line)
        content = resp.get("result", {}).get("content", [{}])[0].get("text", "")
        
        print("\n📊 Health Report:")
        print(content)
        
        if "✅" in content:
            print("\n✅ Verification SUCCESS: Server is reporting health correctly.")
        else:
             print("\n❌ Verification FAIL: Report seems empty or invalid.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        process.terminate()

if __name__ == "__main__":
    main()
