"""
Bug Description: Integer overflow big factorial
Category: edge_cases
Difficulty: medium
Expected Fix: Return error for large inputs or use arbitrary precision
"""

BUGGY_CODE = '''
def big_factorial(n):
    if n <= 1:
        return 1
    return n * big_factorial(n - 1)  # Stack overflow for large n
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import big_factorial

def test_small():
    assert big_factorial(5) == 120

def test_large():
    # Should handle large numbers without stack overflow
    result = big_factorial(500)
    assert result > 0

def test_negative():
    result = big_factorial(-5)
    assert result is None or result == 1

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_046")
    print(f"Description: Integer overflow big factorial")
    print(f"Category: edge_cases")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
