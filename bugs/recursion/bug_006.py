"""
Bug Description: GCD recursive wrong condition
Category: recursion
Difficulty: medium
Expected Fix: Fix the recursive call order (b, a % b)
"""

BUGGY_CODE = '''
def gcd(a, b):
    if b == 0:
        return a
    return gcd(a, a % b)  # Should be gcd(b, a % b)
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import gcd

def test_gcd_12_8():
    assert gcd(12, 8) == 4

def test_gcd_17_5():
    assert gcd(17, 5) == 1

def test_gcd_100_25():
    assert gcd(100, 25) == 25

def test_gcd_same():
    assert gcd(7, 7) == 7

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_006")
    print(f"Description: GCD recursive wrong condition")
    print(f"Category: recursion")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
