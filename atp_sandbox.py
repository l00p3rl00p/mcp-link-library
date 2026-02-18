import json
import datetime
import math
import sys
import io

class ATPSandbox:
    """
    Restricted Python Sandbox for ATP (Agent Tool Protocol).
    Designed to process tool data (filter/map/reduce) without host access.
    """
    def __init__(self):
        # The ONLY things the agent's code can see
        self.safe_builtins = {
            'abs': abs, 'all': all, 'any': any, 'ascii': ascii, 'bin': bin, 'bool': bool,
            'bytearray': bytearray, 'bytes': bytes, 'callable': callable, 'chr': chr,
            'complex': complex, 'dict': dict, 'divmod': divmod, 'enumerate': enumerate,
            'filter': filter, 'float': float, 'format': format, 'frozenset': frozenset,
            'getattr': getattr, 'hasattr': hasattr, 'hash': hash, 'hex': hex, 'id': id,
            'int': int, 'isinstance': isinstance, 'issubclass': issubclass, 'iter': iter,
            'len': len, 'list': list, 'locals': locals, 'map': map, 'max': max, 'min': min,
            'next': next, 'object': object, 'oct': oct, 'ord': ord, 'pow': pow, 'print': print,
            'range': range, 'repr': repr, 'reversed': reversed, 'round': round, 'set': set,
            'setattr': setattr, 'slice': slice, 'sorted': sorted, 'str': str, 'sum': sum,
            'tuple': tuple, 'type': type, 'vars': vars, 'zip': zip,
            'Exception': Exception, 'ValueError': ValueError, 'TypeError': TypeError,
            '__name__': '__main__',
            '__doc__': None,
            '__package__': None,
        }
        
    def execute(self, code: str, context: dict = None):
        """
        Executes code and returns the 'result' variable or the local scope.
        """
        # Capture stdout to prevent protocol pollution
        stdout_capture = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = stdout_capture
        
        try:
            # Deny dangerous keyword strings and dunder access
            dangerous = ['import', 'eval', 'exec', 'open', 'globals', '__', '.__']
            for d in dangerous:
                if d in code:
                    return {"success": False, "error": f"Security Violation: '{d}' is forbidden in ATP sandbox."}

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
