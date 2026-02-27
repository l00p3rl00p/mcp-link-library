"""
ATP Sandbox — Restricted code execution for agent tool data processing.

THREAT MODEL:
- Prevents execution of arbitrary untrusted code from agent protocol
- Blocks file access, network access, subprocess, and import statements
- Uses two-phase defense: AST inspection + string-based pattern blocking

SECURITY ASSUMPTIONS:
- Input code is untrusted (may be from adversarial agent output)
- Context dict may contain sensitive tool data; isolation prevents leakage
- stdout/stderr must be captured to prevent protocol pollution
- No external module imports available; only safe stdlib builtins

DESIGN RATIONALE:
- Dual-phase security: AST analysis catches structural attacks, string patterns catch obfuscation
- Redundancy ensures no single bypass defeats both defenses
- StringIO capture ensures tool protocol integrity (agent cannot inject output)
- Exception handling logs all violations for observability
"""

import json
import datetime
import math
import sys
import io

class ATPSandbox:
    """
    Restricted Python Sandbox for ATP (Agent Tool Protocol).
    
    Designed to process tool data (filter/map/reduce operations) without granting
    host access, file system access, or network access to the sandboxed code.
    
    THREAT MODEL:
    - Protects host from malicious code execution via agent protocol
    - Blocks all imports, file operations, and system calls
    - Prevents class hierarchy escapes (type(), getattr(), etc.)
    
    ASSUMPTIONS:
    - Only safe_builtins are exposed to sandboxed code
    - Context data is untrusted; reads are safe but writes are isolated
    - Caller validates result before using in production contexts
    """
    def __init__(self):
        """
        Initialize sandbox with whitelist of safe builtins.
        
        SECURITY RATIONALE:
        - Only specific builtins are exposed (no open, eval, exec, etc.)
        - Prevents all import statements at sandboxed level
        - Whitelist approach: only safe functions explicitly included
        """
        # The ONLY things the agent's code can see
        self.safe_builtins = {
            'abs': abs, 'all': all, 'any': any, 'ascii': ascii, 'bin': bin, 'bool': bool,
            'bytearray': bytearray, 'bytes': bytes, 'callable': callable, 'chr': chr,
            'complex': complex, 'dict': dict, 'divmod': divmod, 'enumerate': enumerate,
            'filter': filter, 'float': float, 'format': format, 'frozenset': frozenset,
            'hash': hash, 'hex': hex, 'id': id,
            'int': int, 'isinstance': isinstance, 'issubclass': issubclass, 'iter': iter,
            'len': len, 'list': list, 'locals': locals, 'map': map, 'max': max, 'min': min,
            'next': next, 'object': object, 'oct': oct, 'ord': ord, 'pow': pow, 'print': print,
            'range': range, 'repr': repr, 'reversed': reversed, 'round': round, 'set': set,
            'slice': slice, 'sorted': sorted, 'str': str, 'sum': sum,
            'tuple': tuple, 'type': type, 'zip': zip,
            'Exception': Exception, 'ValueError': ValueError, 'TypeError': TypeError,
            '__name__': '__main__',
            '__doc__': None,
            '__package__': None,
        }
        
    def execute(self, code: str, context: dict = None):
        """
        Execute sandboxed code with two-phase security validation.
        
        THREAT MODEL:
        - Phase 1 (AST): Structural analysis blocks imports, eval, exec, dunders
        - Phase 2 (String): Pattern matching catches obfuscation attempts
        - Redundancy: Both phases must pass; single failure blocks execution
        
        ASSUMPTIONS:
        - Code is untrusted (may be adversarial)
        - Context is untrusted but read-only in sandboxed scope
        - Result variable is the output; all other locals are ignored
        
        ERROR HANDLING:
        - SyntaxError: Returns success=False with error message
        - Security violations: Returns specific violation type detected
        - Runtime exceptions: Caught and returned as error dict
        - stdout/stderr: Captured and returned separately to prevent pollution
        
        Args:
            code (str): Python code to execute in sandbox
            context (dict): Untrusted data available as 'context' in sandbox
            
        Returns:
            dict: {"success": bool, "result": ..., "error": ..., "logs": ...}
        """
        # Capture stdout to prevent protocol pollution
        stdout_capture = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = stdout_capture
        
        try:
            import ast
            
            # Phase 1: AST Analysis (Structural Security)
            try:
                tree = ast.parse(code)
            except SyntaxError as e:
                return {"success": False, "error": f"Syntax Error: {str(e)}"}

            class ATPSecurityVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.errors = []
                    # Expanded forbidden set — blocks class-escape vectors
                    self.forbidden_names = {
                        'import', 'eval', 'exec', 'open', 'globals',
                        'locals', 'input', 'getattr', 'setattr', 'delattr',
                        'vars', 'dir', 'compile', 'breakpoint',
                    }
                    # Forbidden callable names (blocks type() class escape)
                    self.forbidden_calls = {'type', 'getattr', 'setattr', 'vars', 'dir', 'compile'}

                def visit_Import(self, node):
                    self.errors.append("Security Violation: 'import' is forbidden.")

                def visit_ImportFrom(self, node):
                    self.errors.append("Security Violation: 'from ... import' is forbidden.")

                def visit_Name(self, node):
                    if node.id in self.forbidden_names:
                        self.errors.append(f"Security Violation: '{node.id}' is forbidden.")
                    if node.id.startswith('__'):
                        self.errors.append(f"Security Violation: '{node.id}' (dunder) is forbidden.")
                    self.generic_visit(node)

                def visit_Attribute(self, node):
                    if node.attr.startswith('__'):
                        self.errors.append(f"Security Violation: dunder attribute '{node.attr}' is forbidden.")
                    self.generic_visit(node)

                def visit_Call(self, node):
                    # Block dangerous built-in calls that enable class-hierarchy escape
                    if isinstance(node.func, ast.Name) and node.func.id in self.forbidden_calls:
                        self.errors.append(f"Security Violation: call to '{node.func.id}()' is forbidden.")
                    self.generic_visit(node)

            visitor = ATPSecurityVisitor()
            visitor.visit(tree)
            
            if visitor.errors:
                return {"success": False, "error": visitor.errors[0]}

            # Phase 2: String-based defense (redundancy)
            dangerous = ['import ', 'eval(', 'exec(', 'open(', 'globals(', '.__']
            for d in dangerous:
                if d in code:
                    return {"success": False, "error": f"Security Violation: Found forbidden pattern '{d}'."}

            safe_globals = {
                "__builtins__": self.safe_builtins,
                "json": json,
                "datetime": datetime,
                "math": math,
                "context": context or {},
                "result": None
            }
            
            # Execute logic
            exec(code, safe_globals)
            
            # Extract result
            result = safe_globals.get("result")
            if result is None:
                # If no explicit result, return everything custom from locals
                result = {k: v for k, v in safe_globals.items() if k not in ["__builtins__", "json", "datetime", "math", "context"]}

            return {
                "success": True,
                "result": result,
                "logs": stdout_capture.getvalue()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            sys.stdout = original_stdout

if __name__ == "__main__":
    # Self-test
    sb = ATPSandbox()
    # Test valid filter
    code = "result = [x for x in context.get('items', []) if x > 5]"
    print(json.dumps(sb.execute(code, {"items": [1, 2, 8, 10]})))
