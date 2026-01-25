"""
Bug Description: groupby with NaN handling
Category: etl
Difficulty: medium
Expected Fix: Use dropna=False in groupby to include NaN groups
"""

BUGGY_CODE = '''
import pandas as pd

def sum_by_category(df):
    return df.groupby('category')['value'].sum().to_dict()  # Drops NaN categories
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import pandas as pd
import numpy as np
from temp_module import sum_by_category

def test_normal():
    df = pd.DataFrame({'category': ['A', 'B', 'A'], 'value': [1, 2, 3]})
    result = sum_by_category(df)
    assert result == {'A': 4, 'B': 2}

def test_with_nan():
    df = pd.DataFrame({'category': ['A', None, 'A'], 'value': [1, 2, 3]})
    result = sum_by_category(df)
    assert 'A' in result and result['A'] == 4
    # NaN category should also be counted
    assert len(result) == 2

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_012")
    print(f"Description: groupby with NaN handling")
    print(f"Category: etl")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
