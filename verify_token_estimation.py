import sys
# Need to import from current dir
sys.path.append('.')
from nexus_session_logger import NexusSessionLogger

print("📉 Verifying Unit 1: Token Estimation Logic...")

logger = NexusSessionLogger()

# Test 1: Heuristic Estimation
text = "Hello World"
estimated = logger.estimate_tokens(text)
expected = len(text) // 4
if estimated == expected:
    print(f"✅ Heuristic Accurate: '{text}' -> {estimated} tokens")
else:
    print(f"❌ Heuristic Failed: '{text}' -> {estimated} tokens (Expected {expected})")
    sys.exit(1)

# Test 2: Log with Auto-Estimation
logger.log_command("echo test", "SUCCESS", result="output")
print("✅ log_command() executed with auto-estimation.")

# Test 3: Log with Explicit Tokens
logger.log_command("llm prompt", "SUCCESS", result="response", tokens={"input": 10, "output": 20, "total": 30})
print("✅ log_command() executed with explicit tokens.")

print("🎉 Unit 1 Verified.")
