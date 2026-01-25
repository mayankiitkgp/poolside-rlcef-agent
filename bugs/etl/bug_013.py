"""
Bug Description: merge with missing key column
Category: etl
Difficulty: medium
Expected Fix: Add validation for key column existence before merge
"""

BUGGY_CODE = '''
import pandas as pd

def merge_dataframes(df1, df2, key):
    return pd.merge(df1, df2, on=key)  # No validation if key exists
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import pandas as pd
import pytest
from temp_module import merge_dataframes

def test_valid_merge():
    df1 = pd.DataFrame({'id': [1, 2], 'a': ['x', 'y']})
    df2 = pd.DataFrame({'id': [1, 2], 'b': ['p', 'q']})
    result = merge_dataframes(df1, df2, 'id')
    assert len(result) == 2

def test_missing_key():
    df1 = pd.DataFrame({'id': [1, 2], 'a': ['x', 'y']})
    df2 = pd.DataFrame({'other': [1, 2], 'b': ['p', 'q']})
    try:
        result = merge_dataframes(df1, df2, 'id')
        assert False, "Should raise error for missing key"
    except KeyError:
        pass

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_013")
    print(f"Description: merge with missing key column")
    print(f"Category: etl")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
