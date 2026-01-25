"""
Bug Description: duplicate column names
Category: etl
Difficulty: medium
Expected Fix: Handle or rename duplicate columns
"""

BUGGY_CODE = '''
import pandas as pd

def add_column(df, name, values):
    df[name] = values  # Silently overwrites if exists
    return df
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import pandas as pd
from temp_module import add_column

def test_add_new():
    df = pd.DataFrame({'a': [1, 2]})
    result = add_column(df, 'b', [3, 4])
    assert 'b' in result.columns

def test_add_existing():
    df = pd.DataFrame({'a': [1, 2]})
    try:
        result = add_column(df, 'a', [3, 4])
        # Should raise error or rename, not silently overwrite
        assert result['a'].tolist() != [3, 4], "Should not silently overwrite"
    except ValueError:
        pass

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_019")
    print(f"Description: duplicate column names")
    print(f"Category: etl")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
