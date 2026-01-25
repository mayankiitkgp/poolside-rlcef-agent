"""
Bug Description: dtype mismatch in concat
Category: etl
Difficulty: hard
Expected Fix: Ensure consistent dtypes before concatenation
"""

BUGGY_CODE = '''
import pandas as pd

def concat_dataframes(dfs):
    return pd.concat(dfs, ignore_index=True)  # May cause dtype issues
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import pandas as pd
from temp_module import concat_dataframes

def test_same_types():
    df1 = pd.DataFrame({'a': [1, 2]})
    df2 = pd.DataFrame({'a': [3, 4]})
    result = concat_dataframes([df1, df2])
    assert result['a'].dtype == 'int64'

def test_mixed_types():
    df1 = pd.DataFrame({'a': [1, 2]})
    df2 = pd.DataFrame({'a': ['3', '4']})
    result = concat_dataframes([df1, df2])
    # After concat, all should be same type
    assert len(result) == 4

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_014")
    print(f"Description: dtype mismatch in concat")
    print(f"Category: etl")
    print(f"Difficulty: hard")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
