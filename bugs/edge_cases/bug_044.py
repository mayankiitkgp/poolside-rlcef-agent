"""
Bug Description: String index out of range
Category: edge_cases
Difficulty: easy
Expected Fix: Check string length before indexing
"""

BUGGY_CODE = '''
def get_char_at(s, index):
    return s[index]  # No bounds checking
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import get_char_at

def test_valid():
    assert get_char_at("hello", 0) == "h"

def test_out_of_range():
    result = get_char_at("hello", 10)
    assert result is None

def test_empty_string():
    result = get_char_at("", 0)
    assert result is None

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_044")
    print(f"Description: String index out of range")
    print(f"Category: edge_cases")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
