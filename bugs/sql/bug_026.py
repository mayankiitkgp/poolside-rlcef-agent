"""
Bug Description: ORDER BY non-existent column
Category: sql
Difficulty: easy
Expected Fix: Use correct column name in ORDER BY
"""

BUGGY_CODE = '''
import sqlite3

def get_sorted_users(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: column 'username' doesn't exist, should be 'name'
    cursor.execute("SELECT * FROM users ORDER BY username")
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
from temp_module import get_sorted_users

def test_sorted():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE users (id INTEGER, name TEXT)')
    conn.execute('INSERT INTO users VALUES (1, "Charlie")')
    conn.execute('INSERT INTO users VALUES (2, "Alice")')
    conn.execute('INSERT INTO users VALUES (3, "Bob")')
    conn.commit()
    conn.close()
    
    try:
        results = get_sorted_users(db_path)
        names = [r[1] for r in results]
        assert names == ['Alice', 'Bob', 'Charlie']
    finally:
        os.unlink(db_path)

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_026")
    print(f"Description: ORDER BY non-existent column")
    print(f"Category: sql")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
