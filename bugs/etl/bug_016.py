"""
Bug Description: incorrect column rename
Category: etl
Difficulty: easy
Expected Fix: Fix the rename dictionary or use correct method
"""

BUGGY_CODE = '''
import pandas as pd

def rename_columns(df, old_name, new_name):
    df.rename(columns={old_name: new_name})  # Missing inplace=True or assignment
    return df
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import pandas as pd
from temp_module import rename_columns

def test_rename():
    df = pd.DataFrame({'old': [1, 2, 3]})
    result = rename_columns(df, 'old', 'new')
    assert 'new' in result.columns
    assert 'old' not in result.columns

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_016")
    print(f"Description: incorrect column rename")
    print(f"Category: etl")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
