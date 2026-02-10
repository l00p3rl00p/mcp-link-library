import json
import sys
import subprocess
import os
from pathlib import Path

def verify_library():
    """
    Diagnostic script for the Librarian (mcp-link-library).
    Checks for document integrity, index existence, and version consistency.
    """
    results = {
        "status": "ok",
        "checks": [],
        "metrics": {}
    }
    
    lib_root = Path(__file__).parent
    docs_dir = lib_root / "documents"
    
    # Check 1: Documents Directory
    if docs_dir.exists() and docs_dir.is_dir():
        doc_files = list(docs_dir.glob("**/*.md"))
        results["checks"].append({
            "name": "documents_dir",
            "status": "ok",
            "message": f"Found {len(doc_files)} knowledge documents"
        })
        results["metrics"]["doc_count"] = len(doc_files)
    else:
        results["checks"].append({
            "name": "documents_dir",
            "status": "error",
            "message": "Documents directory missing"
        })
        results["status"] = "error"

    # Check 2: Core Library Files
    core_files = ["mcp-link-library.md", "mcp.py"]
    for cf in core_files:
        if (lib_root / cf).exists():
             results["checks"].append({
                "name": f"file:{cf}",
                "status": "ok",
                "message": f"Core file {cf} present"
            })
        else:
            results["checks"].append({
                "name": f"file:{cf}",
                "status": "warning",
                "message": f"Core file {cf} missing"
            })

    # Check 3: Database Integrity
    if sys.platform == "win32":
        db_path = Path(os.environ['USERPROFILE']) / ".mcp-tools" / "mcp-server-manager" / "knowledge.db"
    else:
        db_path = Path.home() / ".mcp-tools" / "mcp-server-manager" / "knowledge.db"

    if db_path.exists():
         results["checks"].append({
            "name": "database",
            "status": "ok",
            "message": f"Database file exists at {db_path}"
        })
    else:
        results["checks"].append({
            "name": "database",
            "status": "warning",
            "message": "Database not initialized"
        })


    # Check 4: MCP Protocol Liveness
    mcp_script = lib_root / "mcp.py"
    if mcp_script.exists():
        try:
            # Spawn server process
            process = subprocess.Popen(
                [sys.executable, str(mcp_script), "--server"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send initialize request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "verifier", "version": "0.1.0"}
                }
            }
            
            stdout, stderr = process.communicate(input=json.dumps(request) + "\n", timeout=5)
            
            if stdout:
                response = json.loads(stdout)
                if "result" in response and "capabilities" in response["result"]:
                     results["checks"].append({
                        "name": "mcp_protocol",
                        "status": "ok",
                        "message": "Server speaks MCP protocol (Voice Active)"
                    })
                else:
                    results["checks"].append({
                        "name": "mcp_protocol",
                        "status": "error",
                        "message": f"Invalid protocol response: {stdout[:100]}"
                    })
            else:
                 results["checks"].append({
                    "name": "mcp_protocol",
                    "status": "error",
                    "message": f"No response from server. Stderr: {stderr}"
                })
                
        except Exception as e:
            results["checks"].append({
                "name": "mcp_protocol",
                "status": "error",
                "message": f"Connection failed: {e}"
            })
    else:
        results["checks"].append({
            "name": "mcp_protocol",
            "status": "warning",
            "message": "mcp.py not found, skipping protocol check"
        })
    # Output machine-readable results if requested
    if "--json" in sys.argv:
        print(json.dumps(results, indent=2))
        return

    # Visual human-readable output
    print(f"Librarian Health: {results['status'].upper()}")
    for check in results["checks"]:
        icon = "✅" if check["status"] == "ok" else "❌" if check["status"] == "error" else "⚠️"
        print(f"{icon} {check['name']:15} : {check['message']}")

if __name__ == "__main__":
    verify_library()
