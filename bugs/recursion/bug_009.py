"""
Bug Description: Palindrome check stack overflow
Category: recursion
Difficulty: medium
Expected Fix: Fix the slicing to exclude both first and last characters
"""

BUGGY_CODE = '''
def is_palindrome(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:])  # Should be s[1:-1]
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import is_palindrome

def test_racecar():
    assert is_palindrome("racecar") == True

def test_hello():
    assert is_palindrome("hello") == False

def test_single():
    assert is_palindrome("a") == True

def test_empty():
    assert is_palindrome("") == True

def test_two_same():
    assert is_palindrome("aa") == True

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_009")
    print(f"Description: Palindrome check stack overflow")
    print(f"Category: recursion")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
