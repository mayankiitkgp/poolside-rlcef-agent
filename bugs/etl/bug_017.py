"""
Bug Description: wrong aggregation function
Category: etl
Difficulty: medium
Expected Fix: Use correct aggregation (sum vs mean vs count)
"""

BUGGY_CODE = '''
import pandas as pd

def calculate_totals(df, group_col, value_col):
    return df.groupby(group_col)[value_col].mean()  # Should be sum()
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import pandas as pd
from temp_module import calculate_totals

def test_totals():
    df = pd.DataFrame({
        'category': ['A', 'A', 'B'],
        'value': [10, 20, 15]
    })
    result = calculate_totals(df, 'category', 'value')
    assert result['A'] == 30
    assert result['B'] == 15

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_017")
    print(f"Description: wrong aggregation function")
    print(f"Category: etl")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
