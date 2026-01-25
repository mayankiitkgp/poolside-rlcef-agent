"""
Bug Description: Reverse string recursion error
Category: recursion
Difficulty: easy
Expected Fix: Fix the string slicing for recursion
"""

BUGGY_CODE = '''
def reverse_string(s):
    if len(s) <= 1:
        return s
    return s[0] + reverse_string(s[1:])  # Should be reverse_string(s[1:]) + s[0]
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import reverse_string

def test_hello():
    assert reverse_string("hello") == "olleh"

def test_single_char():
    assert reverse_string("a") == "a"

def test_empty():
    assert reverse_string("") == ""

def test_palindrome():
    assert reverse_string("racecar") == "racecar"

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_007")
    print(f"Description: Reverse string recursion error")
    print(f"Category: recursion")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
