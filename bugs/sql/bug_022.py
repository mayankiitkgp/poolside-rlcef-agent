"""
Bug Description: JOIN without ON clause causing cartesian product
Category: sql
Difficulty: medium
Expected Fix: Add proper ON clause to JOIN
"""

BUGGY_CODE = '''
import sqlite3

def join_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: Missing ON clause creates cartesian product
    cursor.execute("SELECT * FROM orders, customers")
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
from temp_module import join_tables

def test_proper_join():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE customers (id INTEGER, name TEXT)')
    conn.execute('CREATE TABLE orders (id INTEGER, customer_id INTEGER, amount REAL)')
    conn.execute('INSERT INTO customers VALUES (1, "Alice")')
    conn.execute('INSERT INTO customers VALUES (2, "Bob")')
    conn.execute('INSERT INTO orders VALUES (1, 1, 100)')
    conn.execute('INSERT INTO orders VALUES (2, 2, 200)')
    conn.commit()
    conn.close()
    
    try:
        results = join_tables(db_path)
        # Should return 2 rows (one per order), not 4 (cartesian)
        assert len(results) == 2
    finally:
        os.unlink(db_path)

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_022")
    print(f"Description: JOIN without ON clause causing cartesian product")
    print(f"Category: sql")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
