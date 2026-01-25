"""
Bug Description: Event loop already running error
Category: async
Difficulty: hard
Expected Fix: Use asyncio.create_task or get_running_loop
"""

BUGGY_CODE = '''
import asyncio

async def inner_task():
    return "result"

async def outer_task():
    # Bug: Can't call run() inside running loop
    result = asyncio.run(inner_task())
    return result
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import outer_task

def test_nested():
    result = asyncio.run(outer_task())
    assert result == "result"

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_035")
    print(f"Description: Event loop already running error")
    print(f"Category: async")
    print(f"Difficulty: hard")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
