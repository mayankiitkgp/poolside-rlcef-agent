"""
Bug Description: Race condition in async counter
Category: async
Difficulty: hard
Expected Fix: Use asyncio.Lock to protect shared state
"""

BUGGY_CODE = '''
import asyncio

counter = 0

async def increment():
    global counter
    current = counter
    await asyncio.sleep(0.001)  # Simulates async work
    counter = current + 1

async def run_increments(n):
    global counter
    counter = 0
    await asyncio.gather(*[increment() for _ in range(n)])
    return counter
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import run_increments

def test_race_condition():
    result = asyncio.run(run_increments(100))
    # Should be 100 if properly synchronized
    assert result == 100

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_033")
    print(f"Description: Race condition in async counter")
    print(f"Category: async")
    print(f"Difficulty: hard")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
