"""
Bug Description: Concurrent modification error
Category: async
Difficulty: hard
Expected Fix: Avoid modifying collection during iteration
"""

BUGGY_CODE = '''
import asyncio

async def process_items(items):
    results = []
    for item in items:
        await asyncio.sleep(0.001)
        results.append(item * 2)
        items.append(item)  # Modifying during iteration
    return results
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import process_items

def test_process():
    result = asyncio.run(process_items([1, 2, 3]))
    assert result == [2, 4, 6]

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_038")
    print(f"Description: Concurrent modification error")
    print(f"Category: async")
    print(f"Difficulty: hard")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
