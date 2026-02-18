
import sys
import json
import subprocess
from pathlib import Path
import re

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 answer_query.py <query>")
        sys.exit(1)
        
    query = sys.argv[1]
    server_script = Path("mcp.py").resolve()
    
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

        # 2. Search
        print(f"🔍 Searching for: '{query}'")
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
        
        if "No results found" in content:
            print("❌ No results found.")
            return

        print("✅ Found matches. Retrieving content...")
        
        # 3. Extract URIs and Read Content
        # Regex to find URIs in the search result list: - [Title] (URI) or - Title (URI)
        uris = re.findall(r'\(([^)]+)\)', content)
        
        for uri in uris:
            # Skip if it's not a valid URI format we recognize (simple check)
            if not (uri.startswith("file://") or uri.startswith("http") or uri.startswith("mcp://")):
                continue
                
            print(f"\n📥 Reading: {uri}")
            read_req = {
                "jsonrpc": "2.0", 
                "id": 3, 
                "method": "resources/read",
                "params": {"uri": uri}
            }
            process.stdin.write(json.dumps(read_req) + "\n")
            process.stdin.flush()
            
            read_line = process.stdout.readline()
            read_resp = json.loads(read_line)
            
            file_content = read_resp.get("result", {}).get("contents", [{}])[0].get("text", "")
            
            # Simple snippet extraction (primitive "RAG")
            # Find the line with the query or just print first 500 chars
            print("-" * 20)
            if query.lower() in file_content.lower():
                # Print lines surrounding the match
                lines = file_content.split('\n')
                for i, line in enumerate(lines):
                    if query.lower() in line.lower():
                        print(f"MATCH (Line {i+1}): {line.strip()}")
            else:
                print("Content Preview:")
                print(file_content[:500])
            print("-" * 20)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        process.terminate()

if __name__ == "__main__":
    main()
