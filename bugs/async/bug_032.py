"""
Bug Description: Sync function blocking async context
Category: async
Difficulty: medium
Expected Fix: Use asyncio.to_thread or async version
"""

BUGGY_CODE = '''
import asyncio
import time

def slow_sync():
    time.sleep(1)  # Blocks the event loop
    return "done"

async def main():
    result = slow_sync()
    return result
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import asyncio
import time
from temp_module import main

def test_main():
    start = time.time()
    result = asyncio.run(main())
    elapsed = time.time() - start
    assert result == "done"
    # Should complete quickly if properly async
    assert elapsed < 0.5

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_032")
    print(f"Description: Sync function blocking async context")
    print(f"Category: async")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
