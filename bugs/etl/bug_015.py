"""
Bug Description: fillna with wrong value type
Category: etl
Difficulty: easy
Expected Fix: Use appropriate fill value for the column dtype
"""

BUGGY_CODE = '''
import pandas as pd

def fill_missing(df, column, value):
    df[column] = df[column].fillna(value)
    return df  # No type checking
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import pandas as pd
import numpy as np
from temp_module import fill_missing

def test_fill_numeric():
    df = pd.DataFrame({'a': [1.0, np.nan, 3.0]})
    result = fill_missing(df, 'a', 0)
    assert result['a'].tolist() == [1.0, 0.0, 3.0]

def test_fill_string():
    df = pd.DataFrame({'a': ['x', None, 'z']})
    result = fill_missing(df, 'a', 'missing')
    assert result['a'].tolist() == ['x', 'missing', 'z']

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_015")
    print(f"Description: fillna with wrong value type")
    print(f"Category: etl")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
