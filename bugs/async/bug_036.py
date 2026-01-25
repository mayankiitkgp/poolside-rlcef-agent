"""
Bug Description: Timeout not handled
Category: async
Difficulty: medium
Expected Fix: Use asyncio.wait_for with try/except
"""

BUGGY_CODE = '''
import asyncio

async def slow_task():
    await asyncio.sleep(10)
    return "done"

async def run_with_timeout(timeout):
    result = await asyncio.wait_for(slow_task(), timeout=timeout)
    return result  # TimeoutError not handled
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import run_with_timeout

def test_timeout():
    result = asyncio.run(run_with_timeout(0.1))
    # Should return None or handle timeout gracefully
    assert result is None

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_036")
    print(f"Description: Timeout not handled")
    print(f"Category: async")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
