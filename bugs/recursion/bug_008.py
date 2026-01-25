"""
Bug Description: Count digits missing zero check
Category: recursion
Difficulty: easy
Expected Fix: Handle zero as a special case (1 digit)
"""

BUGGY_CODE = '''
def count_digits(n):
    if n < 10:
        return 1
    return 1 + count_digits(n // 10)

# Bug: doesn't handle 0 correctly - returns 1 but concept is ambiguous
# Actually the real bug: negative numbers cause infinite recursion
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import count_digits

def test_single_digit():
    assert count_digits(5) == 1

def test_two_digits():
    assert count_digits(42) == 2

def test_large_number():
    assert count_digits(12345) == 5

def test_zero():
    assert count_digits(0) == 1

def test_negative():
    assert count_digits(-123) == 3

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_008")
    print(f"Description: Count digits missing zero check")
    print(f"Category: recursion")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
