"""
Bug Description: asyncio.gather wrong usage
Category: async
Difficulty: medium
Expected Fix: Pass coroutines, not coroutine functions
"""

BUGGY_CODE = '''
import asyncio

async def task(n):
    await asyncio.sleep(0.01)
    return n * 2

async def run_tasks():
    # Bug: passing function, not coroutine
    results = await asyncio.gather(task, task, task)
    return results
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import run_tasks

def test_gather():
    results = asyncio.run(run_tasks())
    assert isinstance(results, (list, tuple))
    assert len(results) == 3

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_034")
    print(f"Description: asyncio.gather wrong usage")
    print(f"Category: async")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
