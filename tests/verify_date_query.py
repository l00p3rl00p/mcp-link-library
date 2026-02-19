
import sys
import json
import subprocess
from pathlib import Path

def main():
    server_script = Path("mcp.py").resolve()
    print(f"🚀 Spawning MCP Server for Universal PDF Search Verification...")
    
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

        # Search "Mar 6, 2025" (The user's specific complaint)
        query = "Mar 6, 2025"
        print(f"\n🔍 Searching for '{query}' inside PDFs...")
        req = {
            "jsonrpc": "2.0", 
            "id": 2, 
            "method": "tools/call",
            "params": {
                "name": "search_knowledge_base",
                "arguments": {"query": query}
            }
        }
        process.stdin.write(json.dumps(req) + "\n")
        process.stdin.flush()
        
        line = process.stdout.readline()
        resp = json.loads(line)
        content = resp.get("result", {}).get("content", [{}])[0].get("text", "")
        print(f"📄 Response:\n{content.strip()}")

        if "mdi-insurance.pdf" in content:
            print("✅ SUCCESS: Found 'mdi-insurance.pdf' via content search!")
        else:
             print("❌ FAIL: Did not find PDF content match.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        process.terminate()

if __name__ == "__main__":
    main()
