"""
Bug Description: NULL vs None comparison in SQLite
Category: sql
Difficulty: medium
Expected Fix: Use IS NULL instead of = NULL
"""

BUGGY_CODE = '''
import sqlite3

def find_null_values(db_path, table, column):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: = NULL doesn't work in SQL, need IS NULL
    cursor.execute(f"SELECT * FROM {table} WHERE {column} = NULL")
    results = cursor.fetchall()
    conn.close()
    return results
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import sqlite3
import tempfile
import os
from temp_module import find_null_values

def test_find_nulls():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE test (id INTEGER, name TEXT)')
    conn.execute('INSERT INTO test VALUES (1, "Alice")')
    conn.execute('INSERT INTO test VALUES (2, NULL)')
    conn.execute('INSERT INTO test VALUES (3, NULL)')
    conn.commit()
    conn.close()
    
    try:
        results = find_null_values(db_path, 'test', 'name')
        assert len(results) == 2
    finally:
        os.unlink(db_path)

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_021")
    print(f"Description: NULL vs None comparison in SQLite")
    print(f"Category: sql")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
