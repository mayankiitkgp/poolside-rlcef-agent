"""
Bug Description: INNER JOIN instead of LEFT JOIN loses data
Category: sql
Difficulty: medium
Expected Fix: Use LEFT JOIN to preserve all left table rows
"""

BUGGY_CODE = '''
import sqlite3

def get_all_customers_with_orders(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: INNER JOIN excludes customers without orders
    cursor.execute("""
        SELECT c.name, o.amount 
        FROM customers c 
        INNER JOIN orders o ON c.id = o.customer_id
    """)
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
from temp_module import get_all_customers_with_orders

def test_all_customers():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE customers (id INTEGER, name TEXT)')
    conn.execute('CREATE TABLE orders (id INTEGER, customer_id INTEGER, amount REAL)')
    conn.execute('INSERT INTO customers VALUES (1, "Alice")')
    conn.execute('INSERT INTO customers VALUES (2, "Bob")')
    conn.execute('INSERT INTO orders VALUES (1, 1, 100)')
    conn.commit()
    conn.close()
    
    try:
        results = get_all_customers_with_orders(db_path)
        # Should include Bob even without orders
        names = [r[0] for r in results]
        assert 'Alice' in names
        assert 'Bob' in names
        assert len(results) == 2
    finally:
        os.unlink(db_path)

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_028")
    print(f"Description: INNER JOIN instead of LEFT JOIN loses data")
    print(f"Category: sql")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
