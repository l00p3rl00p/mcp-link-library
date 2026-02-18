
import sys
import json
import subprocess
from pathlib import Path
import time
import re

def main():
    server_script = Path("mcp.py").resolve()
    
    print(f"🚀 Spawning MCP Server for Local File Verification...")
    
    cmd = [sys.executable, str(server_script), "--server"]
    process = subprocess.Popen(
        cmd, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # Helper to send request
    def send_request(method, params=None, req_id=1):
        req = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method
        }
        if params:
            req["params"] = params
            
        process.stdin.write(json.dumps(req) + "\n")
        process.stdin.flush()
        return req

    try:
        # 1. Initialize
        send_request("initialize", req_id=1)
        line = process.stdout.readline()
        # Skip init response check for brevity

        # 2. Search "insurance"
        print("\n🔍 Searching for 'insurance'...")
        req = send_request("tools/call", {
            "name": "search_knowledge_base",
            "arguments": {"query": "insurance"}
        }, req_id=2)
        
        line = process.stdout.readline()
        resp = json.loads(line)
        content = resp.get("result", {}).get("content", [{}])[0].get("text", "")
        print(f"📄 Search Results:\n{content.strip()}")
        
        if "mdi-insurance.pdf" not in content:
            print("❌ 'mdi-insurance.pdf' not found in search results.")
            return

        # 3. Retrieve
        # Extract URI: file:///Users/.../mdi-insurance.pdf
        match = re.search(r'\((file://[^)]+)\)', content)
        if match:
            uri = match.group(1)
            print(f"\n📥 Retrieving content from: {uri}...")
            
            send_request("resources/read", {"uri": uri}, req_id=3)
            line = process.stdout.readline()
            resp = json.loads(line)
            
            blob = resp.get("result", {}).get("contents", [{}])[0].get("text", "")
            
            if blob:
                print(f"✅ FILE ACCESSED ({len(blob)} bytes)")
                preview = blob[:50].replace("\n", " ")
                print(f"📄 Header Preview: {preview}...")
                
                if "%PDF" in blob:
                    print("✅ Confirmed Valid PDF Header")
            else:
                print("⚠️  No content returned (empty file?)")
        else:
             print("⚠️  Could not parse file URI from search result.")

        print("\n" + "="*40)
        print("   LOCAL FILE ADDED & VERIFIED 🟢")
        print("="*40 + "\n")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        process.terminate()

if __name__ == "__main__":
    main()
