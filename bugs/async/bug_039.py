"""
Bug Description: Deadlock in async lock
Category: async
Difficulty: hard
Expected Fix: Use timeout or avoid nested lock acquisition
"""

BUGGY_CODE = '''
import asyncio

lock = asyncio.Lock()

async def task_a():
    async with lock:
        await asyncio.sleep(0.01)
        async with lock:  # Deadlock - already holding lock
            return "done"

async def run():
    return await task_a()
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import run

def test_no_deadlock():
    result = asyncio.run(asyncio.wait_for(run(), timeout=1))
    assert result == "done"

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_039")
    print(f"Description: Deadlock in async lock")
    print(f"Category: async")
    print(f"Difficulty: hard")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
