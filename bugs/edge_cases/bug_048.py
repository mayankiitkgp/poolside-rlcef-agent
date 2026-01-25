"""
Bug Description: None type operation
Category: edge_cases
Difficulty: easy
Expected Fix: Check for None before operation
"""

BUGGY_CODE = '''
def double_value(x):
    return x * 2  # TypeError if x is None
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import double_value

def test_number():
    assert double_value(5) == 10

def test_none():
    result = double_value(None)
    assert result is None

def test_string():
    assert double_value("ab") == "abab"

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_048")
    print(f"Description: None type operation")
    print(f"Category: edge_cases")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
