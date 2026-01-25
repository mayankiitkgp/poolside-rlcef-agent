"""
Bug Description: Factorial missing base case
Category: recursion
Difficulty: easy
Expected Fix: Add base case for n == 0 or n == 1
"""

BUGGY_CODE = '''
def factorial(n):
    return n * factorial(n - 1)  # Missing base case - infinite recursion
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import factorial

def test_factorial_5():
    assert factorial(5) == 120

def test_factorial_0():
    assert factorial(0) == 1

def test_factorial_1():
    assert factorial(1) == 1

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_001")
    print(f"Description: Factorial missing base case")
    print(f"Category: recursion")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
