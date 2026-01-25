"""
Bug Description: Infinite while loop
Category: edge_cases
Difficulty: easy
Expected Fix: Add proper loop termination condition
"""

BUGGY_CODE = '''
def countdown(n):
    result = []
    while n > 0:
        result.append(n)
        # Missing n -= 1
    return result
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import countdown

def test_countdown():
    result = countdown(5)
    assert result == [5, 4, 3, 2, 1]

def test_zero():
    result = countdown(0)
    assert result == []

def test_one():
    result = countdown(1)
    assert result == [1]

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_049")
    print(f"Description: Infinite while loop")
    print(f"Category: edge_cases")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
