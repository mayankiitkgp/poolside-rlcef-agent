"""
Bug Description: Power function infinite loop
Category: recursion
Difficulty: easy
Expected Fix: Handle negative exponents and add base case
"""

BUGGY_CODE = '''
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp)  # Should be exp - 1
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import power

def test_power_2_3():
    assert power(2, 3) == 8

def test_power_5_0():
    assert power(5, 0) == 1

def test_power_3_2():
    assert power(3, 2) == 9

def test_power_10_1():
    assert power(10, 1) == 10

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_005")
    print(f"Description: Power function infinite loop")
    print(f"Category: recursion")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
