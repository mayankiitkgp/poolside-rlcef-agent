"""
Bug Description: WHERE clause syntax error
Category: sql
Difficulty: easy
Expected Fix: Use proper SQL string comparison syntax
"""

BUGGY_CODE = '''
import sqlite3

def find_by_name(db_path, table, name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: Missing quotes around string value
    cursor.execute(f"SELECT * FROM {table} WHERE name = {name}")
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
from temp_module import find_by_name

def test_find_name():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE users (id INTEGER, name TEXT)')
    conn.execute('INSERT INTO users VALUES (1, "Alice")')
    conn.execute('INSERT INTO users VALUES (2, "Bob")')
    conn.commit()
    conn.close()
    
    try:
        results = find_by_name(db_path, 'users', 'Alice')
        assert len(results) == 1
        assert results[0][1] == 'Alice'
    finally:
        os.unlink(db_path)

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_023")
    print(f"Description: WHERE clause syntax error")
    print(f"Category: sql")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
