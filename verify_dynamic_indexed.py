
import sys
import json
import subprocess
import time
from pathlib import Path

def main():
    venv_python = Path.home() / ".mcp-tools" / ".venv" / "bin" / "python"
    server_script = Path("mcp.py").resolve()
    test_dir = Path("test_watch_dir").resolve()
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "dynamic_test.txt"
    if test_file.exists():
        test_file.unlink()

    print(f"🏥 Spawning MCP Server for Dynamic Indexing Check...")
    
    cmd = [str(venv_python), str(server_script), "--server"]
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

        # 2. Start Watcher
        print(f"👁️  Starting watcher on {test_dir}...")
        req = {
            "jsonrpc": "2.0", 
            "id": 2, 
            "method": "tools/call",
            "params": {
                "name": "start_watcher",
                "arguments": {
                    "paths": [str(test_dir)]
                } 
            }
        }
        process.stdin.write(json.dumps(req) + "\n")
        process.stdin.flush()
        process.stdout.readline()
        
        print("⏳ Waiting for watcher to initialize (2 sec)...")
        time.sleep(2)

        # 3. Create a file
        print(f"📝 Creating file {test_file.name}...")
        test_file.write_text("This is a dynamic test for the Librarian watcher. SecretKey: NEXUS-DYNAMIC-999")
        
        # 4. Wait for indexing
        print("⏳ Waiting for auto-indexing (3 sec)...")
        time.sleep(3)

        # 5. Search for the content
        print("🔍 Searching for SecretKey...")
        req = {
            "jsonrpc": "2.0", 
            "id": 3, 
            "method": "tools/call",
            "params": {
                "name": "search_knowledge_base",
                "arguments": {
                    "query": "NEXUS-DYNAMIC-999"
                } 
            }
        }
        process.stdin.write(json.dumps(req) + "\n")
        process.stdin.flush()
        
        # Drain lines until we find the search result
        search_result = ""
        while True:
            line = process.stdout.readline()
            if not line: break
            try:
                resp = json.loads(line)
                if resp.get("id") == 3:
                    search_result = resp.get("result", {}).get("content", [{}])[0].get("text", "")
                    break
            except:
                continue
        
        print("\n🔍 Search Result:")
        print(search_result)
        
        if "dynamic_test.txt" in search_result:
            print("\n✅ Verification SUCCESS: Dynamic Indexing is WORKING.")
        else:
             print("\n❌ Verification FAIL: File not found in search.")
             print("\n📝 Inspecting Watcher Logs...")
             req = {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_watcher_logs", "arguments": {}}}
             process.stdin.write(json.dumps(req) + "\n")
             process.stdin.flush()
             line = process.stdout.readline()
             if line:
                 print(json.loads(line).get("result", {}).get("content", [{}])[0].get("text", ""))

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        process.terminate()
        stdout, stderr = process.communicate(timeout=2)
        if stderr:
            print("\n🖥️  Server Stderr:")
            print(stderr)
        
        if test_file.exists():
            test_file.unlink()
        if test_dir.exists():
            test_dir.rmdir()

if __name__ == "__main__":
    main()
