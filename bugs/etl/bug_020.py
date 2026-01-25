"""
Bug Description: missing encoding in read_csv
Category: etl
Difficulty: easy
Expected Fix: Specify encoding parameter for non-ASCII data
"""

BUGGY_CODE = '''
import pandas as pd

def read_csv_file(filepath):
    return pd.read_csv(filepath)  # Missing encoding for special characters
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import pandas as pd
import tempfile
import os
from temp_module import read_csv_file

def test_utf8():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write('name,city\n')
        f.write('José,São Paulo\n')
        filepath = f.name
    try:
        result = read_csv_file(filepath)
        assert result['name'][0] == 'José'
        assert result['city'][0] == 'São Paulo'
    finally:
        os.unlink(filepath)

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_020")
    print(f"Description: missing encoding in read_csv")
    print(f"Category: etl")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
