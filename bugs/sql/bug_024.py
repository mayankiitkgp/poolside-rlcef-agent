"""
Bug Description: GROUP BY missing column
Category: sql
Difficulty: medium
Expected Fix: Include all non-aggregated columns in GROUP BY
"""

BUGGY_CODE = '''
import sqlite3

def get_stats_by_category(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: name not in GROUP BY but selected
    cursor.execute("SELECT category, name, SUM(amount) FROM sales GROUP BY category")
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
from temp_module import get_stats_by_category

def test_group_by():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE sales (category TEXT, name TEXT, amount REAL)')
    conn.execute('INSERT INTO sales VALUES ("A", "Item1", 100)')
    conn.execute('INSERT INTO sales VALUES ("A", "Item2", 150)')
    conn.execute('INSERT INTO sales VALUES ("B", "Item3", 200)')
    conn.commit()
    conn.close()
    
    try:
        results = get_stats_by_category(db_path)
        # Should have 2 categories with correct sums
        assert len(results) == 2
    finally:
        os.unlink(db_path)

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_024")
    print(f"Description: GROUP BY missing column")
    print(f"Category: sql")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
