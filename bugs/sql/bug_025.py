"""
Bug Description: HAVING without GROUP BY
Category: sql
Difficulty: medium
Expected Fix: Add GROUP BY clause before HAVING
"""

BUGGY_CODE = '''
import sqlite3

def filter_high_totals(db_path, min_total):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: HAVING without GROUP BY
    cursor.execute(f"SELECT category, SUM(amount) as total FROM sales HAVING total > {min_total}")
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
from temp_module import filter_high_totals

def test_having():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE sales (category TEXT, amount REAL)')
    conn.execute('INSERT INTO sales VALUES ("A", 100)')
    conn.execute('INSERT INTO sales VALUES ("A", 150)')
    conn.execute('INSERT INTO sales VALUES ("B", 50)')
    conn.commit()
    conn.close()
    
    try:
        results = filter_high_totals(db_path, 100)
        assert len(results) == 1
        assert results[0][0] == 'A'
    finally:
        os.unlink(db_path)

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_025")
    print(f"Description: HAVING without GROUP BY")
    print(f"Category: sql")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
