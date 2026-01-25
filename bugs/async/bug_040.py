"""
Bug Description: Missing async context manager
Category: async
Difficulty: medium
Expected Fix: Use contextlib.asynccontextmanager or implement __aenter__/__aexit__
"""

BUGGY_CODE = '''
import asyncio
from contextlib import contextmanager

@contextmanager  # Should be asynccontextmanager
def async_resource():
    yield "resource"

async def use_resource():
    async with async_resource() as r:
        return r
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import use_resource

def test_resource():
    result = asyncio.run(use_resource())
    assert result == "resource"

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_040")
    print(f"Description: Missing async context manager")
    print(f"Category: async")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
