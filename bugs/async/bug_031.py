"""
Bug Description: Missing await keyword
Category: async
Difficulty: easy
Expected Fix: Add await before async function call
"""

BUGGY_CODE = '''
import asyncio

async def fetch_data():
    await asyncio.sleep(0.1)
    return {"data": "result"}

async def process():
    result = fetch_data()  # Missing await
    return result
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import process

def test_process():
    result = asyncio.run(process())
    assert isinstance(result, dict)
    assert result.get("data") == "result"

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_031")
    print(f"Description: Missing await keyword")
    print(f"Category: async")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
