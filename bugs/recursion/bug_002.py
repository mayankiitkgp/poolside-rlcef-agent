"""
Bug Description: Fibonacci off-by-one error
Category: recursion
Difficulty: easy
Expected Fix: Fix the base cases and index alignment
"""

BUGGY_CODE = '''
def fibonacci(n):
    if n == 0:
        return 1  # Should return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import fibonacci

def test_fib_0():
    assert fibonacci(0) == 0

def test_fib_1():
    assert fibonacci(1) == 1

def test_fib_5():
    assert fibonacci(5) == 5

def test_fib_10():
    assert fibonacci(10) == 55

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_002")
    print(f"Description: Fibonacci off-by-one error")
    print(f"Category: recursion")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
