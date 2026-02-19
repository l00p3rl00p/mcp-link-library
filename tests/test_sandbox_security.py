from atp_sandbox import ATPSandbox
import json

def run_jailbreak_audit():
    sb = ATPSandbox()
    tests = [
        ("Import Attempt", "import os; result = os.getcwd()"),
        ("System Call", "import subprocess; result = subprocess.run(['ls'])"),
        ("File Access", "result = open('/etc/passwd').read()"),
        ("Builtin Hack", "result = __builtins__['open']('/etc/passwd').read()"),
        ("Dunder Hack", "result = context.__class__.__base__"),
    ]
    
    print(f"--- ATP Sandbox Security Audit ---")
    all_passed = True
    for name, code in tests:
        response = sb.execute(code)
        if response.get("success") == False or "Security Violation" in str(response.get("error")):
            print(f"✅ {name:15}: BLOCKED (Correct)")
        else:
            print(f"❌ {name:15}: ESCAPED! Result: {response.get('result')}")
            all_passed = False
            
    # Test valid logic
    valid_code = "result = sum(context['data'])"
    valid_resp = sb.execute(valid_code, {"data": [10, 20, 30]})
    if valid_resp.get("result") == 60:
        print(f"✅ Valid Logic   : EXECUTED (Correct)")
    else:
        print(f"❌ Valid Logic   : FAILED")
        all_passed = False

    return all_passed

if __name__ == "__main__":
    if run_jailbreak_audit():
        print("\n🛡️  ATP Sandbox Security: [VERIFIED HARDENED]")
    else:
        print("\n🚨 ATP Sandbox Security: [VULNERABLE]")
        exit(1)
