"""
Bug Description: Dict KeyError
Category: edge_cases
Difficulty: easy
Expected Fix: Use .get() or check key existence
"""

BUGGY_CODE = '''
def get_value(d, key):
    return d[key]  # KeyError if missing
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import get_value

def test_exists():
    assert get_value({'a': 1}, 'a') == 1

def test_missing():
    result = get_value({'a': 1}, 'b')
    assert result is None

def test_default():
    result = get_value({}, 'any')
    assert result is None

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_045")
    print(f"Description: Dict KeyError")
    print(f"Category: edge_cases")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
