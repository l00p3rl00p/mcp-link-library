
import sys
import json
import subprocess
from pathlib import Path
try:
    import openpyxl
    import docx
    from PIL import Image
except ImportError:
    print("❌ Missing dependencies. Run pip install openpyxl python-docx Pillow")
    sys.exit(1)

def create_test_files():
    print("📂 Creating test files...")
    
    # 1. Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws['A1'] = "Project Code"
    ws['B1'] = "Status"
    ws['A2'] = "NEXUS-001"
    ws['B2'] = "Alpha Release"
    wb.save("test_excel.xlsx")
    print("   - test_excel.xlsx")

    # 2. Word
    doc = docx.Document()
    doc.add_heading('Nexus Report', 0)
    doc.add_paragraph('Confidential mission briefing for Agent 007.')
    doc.save("test_word.docx")
    print("   - test_word.docx")

    # 3. Image
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save("test_image.png")
    print("   - test_image.png")

def index_and_search():
    server_script = Path("mcp.py").resolve()
    files = [
        ("test_excel.xlsx", "NEXUS-001"),
        ("test_word.docx", "mission briefing"),
        ("test_image.png", "Format: PNG") 
    ]
    
    for filename, query in files:
        file_path = Path(filename).resolve()
        uri = f"file://{file_path}"
        
        print(f"\n🔗 Indexing {filename}...")
        subprocess.run([sys.executable, str(server_script), "--add", uri, "--categories", "test"], check=True)
        
        print(f"🔍 Searching for '{query}'...")
        # Spawn server to search
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
            # Initialize
            process.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"}) + "\n")
            process.stdin.flush()
            process.stdout.readline()

            # Search
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
            
            if filename in content:
                print(f"✅ SUCCESS: Found {filename} via query '{query}'")
            else:
                print(f"❌ FAIL: Did not find {filename}")
                print(f"   Response: {content[:200]}...")

        finally:
            process.terminate()

if __name__ == "__main__":
    create_test_files()
    index_and_search()
