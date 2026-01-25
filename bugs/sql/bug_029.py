"""
Bug Description: String concatenation with NULL returns NULL
Category: sql
Difficulty: medium
Expected Fix: Use COALESCE or IFNULL to handle NULL in concatenation
"""

BUGGY_CODE = '''
import sqlite3

def get_full_names(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: NULL + string = NULL in SQL
    cursor.execute("SELECT first_name || ' ' || last_name as full_name FROM users")
    results = cursor.fetchall()
    conn.close()
    return [r[0] for r in results]
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
import sqlite3
import tempfile
import os
from temp_module import get_full_names

def test_full_names():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE users (first_name TEXT, last_name TEXT)')
    conn.execute('INSERT INTO users VALUES ("Alice", "Smith")')
    conn.execute('INSERT INTO users VALUES ("Bob", NULL)')
    conn.commit()
    conn.close()
    
    try:
        results = get_full_names(db_path)
        assert results[0] == 'Alice Smith'
        # Bob should still appear, not as None
        assert results[1] is not None
        assert 'Bob' in results[1]
    finally:
        os.unlink(db_path)

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_029")
    print(f"Description: String concatenation with NULL returns NULL")
    print(f"Category: sql")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
