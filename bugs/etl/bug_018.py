"""
Bug Description: index reset error
Category: etl
Difficulty: easy
Expected Fix: Use reset_index properly with drop parameter
"""

BUGGY_CODE = '''
import pandas as pd

def reset_df_index(df):
    df.reset_index()  # Missing inplace or assignment
    return df
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import pandas as pd
from temp_module import reset_df_index

def test_reset():
    df = pd.DataFrame({'a': [1, 2, 3]}, index=[10, 20, 30])
    result = reset_df_index(df)
    assert list(result.index) == [0, 1, 2]

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_018")
    print(f"Description: index reset error")
    print(f"Category: etl")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
