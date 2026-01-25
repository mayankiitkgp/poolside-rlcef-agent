"""
Bug Description: Date comparison format error
Category: sql
Difficulty: medium
Expected Fix: Use consistent date format (YYYY-MM-DD) for comparison
"""

BUGGY_CODE = '''
import sqlite3

def get_recent_orders(db_path, date_str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: Date format mismatch
    cursor.execute(f"SELECT * FROM orders WHERE order_date > '{date_str}'")
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
from temp_module import get_recent_orders

def test_recent():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE orders (id INTEGER, order_date TEXT)')
    conn.execute('INSERT INTO orders VALUES (1, "2024-01-15")')
    conn.execute('INSERT INTO orders VALUES (2, "2024-02-20")')
    conn.execute('INSERT INTO orders VALUES (3, "2024-03-10")')
    conn.commit()
    conn.close()
    
    try:
        results = get_recent_orders(db_path, '2024-02-01')
        assert len(results) == 2
    finally:
        os.unlink(db_path)

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_030")
    print(f"Description: Date comparison format error")
    print(f"Category: sql")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
