import asyncio
import httpx
import subprocess
import time
import os
import sys

async def test_hive_mind():
    print("Starting Hive Mind Daemon...")
    # Generate a secure key for testing
    os.environ["HIVE_MIND_API_KEY"] = "test-secure-key"
    
    # Start the daemon
    daemon = subprocess.Popen([sys.executable, "friday_node.py", "--port", "8082"])
    
    # Wait for startup
    time.sleep(3)
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Test without API key (Should fail)
            print("\n[Test 1] Testing Hive Mind without API key...")
            res1 = await client.post("http://localhost:8082/execute", json={"command": "echo hello", "timeout": 5})
            if res1.status_code == 403:
                print("[PASSED] Hive Mind rejected unauthorized request (403 Forbidden).")
            else:
                print(f"[FAILED] Hive Mind returned {res1.status_code}: {res1.text}")
                
            # 2. Test with correct API key (Should pass)
            print("\n[Test 2] Testing Hive Mind WITH API key...")
            headers = {"X-API-Key": "test-secure-key"}
            res2 = await client.post("http://localhost:8082/execute", json={"command": "echo hello", "timeout": 5}, headers=headers)
            if res2.status_code == 200:
                print("[PASSED] Hive Mind accepted authorized request.")
                print(f"   Output: {res2.json().get('stdout', '').strip()}")
            else:
                print(f"[FAILED] Hive Mind returned {res2.status_code}: {res2.text}")
                
    finally:
        print("\nShutting down daemon...")
        daemon.terminate()
        daemon.wait()

if __name__ == "__main__":
    asyncio.run(test_hive_mind())
