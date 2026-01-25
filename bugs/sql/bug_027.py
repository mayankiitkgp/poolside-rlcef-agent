"""
Bug Description: COUNT(*) with wrong filter
Category: sql
Difficulty: easy
Expected Fix: Fix WHERE clause condition
"""

BUGGY_CODE = '''
import sqlite3

def count_active_users(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: Using = instead of True/1 for boolean
    cursor.execute("SELECT COUNT(*) FROM users WHERE active = 'true'")
    result = cursor.fetchone()[0]
    conn.close()
    return result
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import sqlite3
import tempfile
import os
from temp_module import count_active_users

def test_count():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE users (id INTEGER, name TEXT, active INTEGER)')
    conn.execute('INSERT INTO users VALUES (1, "Alice", 1)')
    conn.execute('INSERT INTO users VALUES (2, "Bob", 0)')
    conn.execute('INSERT INTO users VALUES (3, "Charlie", 1)')
    conn.commit()
    conn.close()
    
    try:
        count = count_active_users(db_path)
        assert count == 2
    finally:
        os.unlink(db_path)

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_027")
    print(f"Description: COUNT(*) with wrong filter")
    print(f"Category: sql")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
