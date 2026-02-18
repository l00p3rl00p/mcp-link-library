import requests
import json
import time
import logging
import os
from typing import Dict, Any, Optional, Union
from urllib.parse import urlparse

try:
    from nexus_session_logger import NexusSessionLogger
    session_logger = NexusSessionLogger()
except ImportError:
    session_logger = None

# Constants for defaults and safety
DEFAULT_TIMEOUT_MS = 30000
MAX_RESPONSE_SIZE_BYTES = 1024 * 1024 # 1MB Default
ALLOWED_SCHEMES = ("http", "https")

class MCPWrapper:
    """
    Deterministic MCP Wrapper (The Reliable Pipe)
    Implements the Canonical Wrapper Schema (v1).
    """

    def __init__(self, max_response_size: int = MAX_RESPONSE_SIZE_BYTES):
        self.max_response_size = max_response_size

    def _extract_path(self, data: Any, path: str) -> Any:
        """Helper to extract data via dot-path notation (projection)."""
        if not path or not isinstance(data, dict):
            return data
        
        keys = path.split('.')
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current

    def call(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes an HTTP call based on the canonical input schema.
        """
        req_id = request_data.get("id", "unknown")
        method = request_data.get("method", "GET").upper()
        url = request_data.get("url", "")
        headers = request_data.get("headers", {})
        body = request_data.get("body")
        timeout_ms = request_data.get("timeout_ms", DEFAULT_TIMEOUT_MS)
        response_mode = request_data.get("response_mode", "json")
        extract_config = request_data.get("extract", {})
        
        start_time = time.perf_counter()
        
        # 1. Security Check (Scheme Whitelist)
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ALLOWED_SCHEMES:
            return self._finalize_response(
                req_id, False, 0, start_time, 
                error_type="blocked", 
                message=f"Protocol {parsed_url.scheme} is NOT allowed. Only HTTP/S."
            )

        # 2. Logic Execution
        try:
            # Prepare Request
            timeout_sec = timeout_ms / 1000.0
            
            # Deterministic Retry logic (Retry once on network error, not HTTP error)
            response = None
            last_err = None
            
            for attempt in range(2): # 0 = primary, 1 = retry
                try:
                    response = requests.request(
                        method=method,
                        url=url,
                        headers=headers,
                        json=body if isinstance(body, (dict, list)) else None,
                        data=body if isinstance(body, (str, bytes)) else None,
                        timeout=timeout_sec,
                        stream=True # Use stream for size control
                    )
                    break # Success
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                    last_err = e
                    if attempt == 0:
                        time.sleep(0.5) # Minimal backoff for retry
                        continue
                    else:
                        raise e
            
            if response is None:
                raise last_err

            # 3. Payload Size Guard & Aggregation
            content = b""
            truncated = False
            try:
                for chunk in response.iter_content(chunk_size=8192):
                    if len(content) + len(chunk) > self.max_response_size:
                        # Capture partial if possible or just flag
                        truncated = True
                        break
                    content += chunk
            except Exception as e:
                # Handle streaming errors (e.g. connection lost mid-way)
                if not content:
                    raise e
                truncated = True # Treat as truncation/interruption
            
            elapsed_ms = int((time.perf_counter() - start_time) * 1000)
            
            # 4. Response Normalization
            res_data = None
            extracted = None
            err = None
            
            if response_mode == "json":
                try:
                    res_data = json.loads(content.decode('utf-8'))
                    # Projection Engine
                    if "path" in extract_config:
                        extracted = self._extract_path(res_data, extract_config["path"])
                except json.JSONDecodeError:
                    if not truncated:
                        err = {"type": "parse", "message": "Failed to parse JSON body"}
            
            return self._finalize_response(
                req_id, 
                response.ok, 
                response.status_code, 
                start_time,
                url=url,
                headers=dict(response.headers),
                data=res_data,
                extracted=extracted,
                error=err,
                truncated=truncated,
                bytes_in=len(content),
                content_type=response.headers.get("Content-Type")
            )

        except requests.exceptions.Timeout:
            return self._finalize_response(req_id, False, 0, start_time, url=url, error_type="timeout", message="Request timed out")
        except requests.exceptions.ConnectionError as e:
            return self._finalize_response(req_id, False, 0, start_time, url=url, error_type="connect", message=str(e))
        except Exception as e:
            return self._finalize_response(req_id, False, 0, start_time, url=url, error_type="http", message=str(e))

    def _finalize_response(self, req_id: str, ok: bool, status: int, start_time: float, 
                           url: str = "",
                           headers: Optional[Dict] = None, data: Any = None, 
                           extracted: Any = None, error_type: Optional[str] = None, 
                           message: Optional[str] = None, error: Optional[Dict] = None,
                           truncated: bool = False, bytes_in: int = 0,
                           content_type: Optional[str] = None) -> Dict[str, Any]:
        
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        
        # Build standard error object if needed
        final_error = error
        if not ok and not final_error:
            final_error = {
                "type": error_type or "http",
                "message": message or f"HTTP {status}",
                "details": {"status": status}
            }

        result = {
            "id": req_id,
            "ok": ok,
            "status": status,
            "elapsed_ms": elapsed_ms,
            "content_type": content_type,
            "data": data,
            "extracted": extracted,
            "error": final_error,
            "truncated": truncated,
            "bytes_in": bytes_in
        }
        
        # Performance/Tier Estimation (Decomposition 13)
        host = urlparse(url).hostname or ""
        result["tier"] = "local" if any(x in host for x in ["localhost", "127.0.0.1"]) else "external"

        # Token Auditing (Unit 23)
        tokens = {"input": 0, "output": 0, "total": 0}
        
        # 1. Try to extract real usage from response (LLM Standard)
        if isinstance(data, dict) and "usage" in data:
            u = data["usage"]
            tokens["input"] = u.get("prompt_tokens", u.get("input_tokens", 0))
            tokens["output"] = u.get("completion_tokens", u.get("output_tokens", 0))
            tokens["total"] = u.get("total_tokens", tokens["input"] + tokens["output"])
            
        # 2. Fallback to heuristic
        if tokens["total"] == 0:
            # Estimate input (Request Body)
            if headers:
                tokens["input"] += len(str(headers)) // 4
            # We don't have easy access to request body here without passing it down, 
            # so we focus on response for now.
            
            # Estimate output (Response Content)
            if bytes_in > 0:
                tokens["output"] = bytes_in // 4 # Rough char count proxy
            
            tokens["total"] = tokens["input"] + tokens["output"]

        result["usage"] = tokens

        # Observability Hook
        if session_logger:
            session_logger.log_command(f"mcp_wrapper {req_id}", "SUCCESS" if ok else "ERROR", 
                                      result=f"Status: {status}, Time: {elapsed_ms}ms, Size: {bytes_in}b",
                                      tokens=tokens)
            
        return result

# Singleton instance
wrapper = MCPWrapper()

if __name__ == "__main__":
    # Self-test demo
    test_req = {
        "id": "test-ollama",
        "method": "POST",
        "url": "http://localhost:11434/api/generate",
        "body": {"model": "qwen2.5-coder:7b", "prompt": "Hello", "stream": False},
        "extract": {"path": "response"}
    }
    print("Testing Wrapper (Ollama Mock-style)...")
    # Using a real public API for better testability if Ollama is down
    test_req_pub = {
        "id": "test-public",
        "method": "GET",
        "url": "https://jsonplaceholder.typicode.com/todos/1",
        "extract": {"path": "title"}
    }
    res = wrapper.call(test_req_pub)
    print(json.dumps(res, indent=2))
