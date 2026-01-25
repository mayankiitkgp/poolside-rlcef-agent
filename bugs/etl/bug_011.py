"""
Bug Description: apply() on None values crashes
Category: etl
Difficulty: medium
Expected Fix: Handle None/NaN values before applying function
"""

BUGGY_CODE = '''
import pandas as pd

def clean_names(df):
    df['name'] = df['name'].apply(lambda x: x.upper())  # Crashes on None
    return df
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import pandas as pd
from temp_module import clean_names

def test_normal_names():
    df = pd.DataFrame({'name': ['alice', 'bob']})
    result = clean_names(df)
    assert result['name'].tolist() == ['ALICE', 'BOB']

def test_with_none():
    df = pd.DataFrame({'name': ['alice', None, 'bob']})
    result = clean_names(df)
    assert result['name'].tolist() == ['ALICE', None, 'BOB']

def test_empty():
    df = pd.DataFrame({'name': []})
    result = clean_names(df)
    assert len(result) == 0

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_011")
    print(f"Description: apply() on None values crashes")
    print(f"Category: etl")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
