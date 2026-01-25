"""
Bug Description: async with missing __aexit__
Category: async
Difficulty: hard
Expected Fix: Implement both __aenter__ and __aexit__
"""

BUGGY_CODE = '''
class AsyncResource:
    async def __aenter__(self):
        return self
    
    # Missing __aexit__

async def use_resource():
    async with AsyncResource() as r:
        return "used"
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import use_resource

def test_async_with():
    result = asyncio.run(use_resource())
    assert result == "used"

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_037")
    print(f"Description: async with missing __aexit__")
    print(f"Category: async")
    print(f"Difficulty: hard")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
