"""
Bug Dataset Generator for RLCEF Training.

Generates 50 diverse buggy Python code examples across 5 categories:
- Recursion bugs
- ETL/Pandas bugs  
- SQL bugs
- Async bugs
- Edge case bugs

Each bug file contains BUGGY_CODE and TEST_CODE that can be used
with the RLCEF agent for training data collection.
"""

import os
from pathlib import Path

# Base directory for bugs
BUGS_DIR = Path("bugs")

# Bug definitions organized by category
BUGS = {
    "recursion": [
        {
            "id": "bug_001",
            "description": "Factorial missing base case",
            "difficulty": "easy",
            "expected_fix": "Add base case for n == 0 or n == 1",
            "buggy_code": '''def factorial(n):
    return n * factorial(n - 1)  # Missing base case - infinite recursion''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import factorial

def test_factorial_5():
    assert factorial(5) == 120

def test_factorial_0():
    assert factorial(0) == 1

def test_factorial_1():
    assert factorial(1) == 1
'''
        },
        {
            "id": "bug_002",
            "description": "Fibonacci off-by-one error",
            "difficulty": "easy",
            "expected_fix": "Fix the base cases and index alignment",
            "buggy_code": '''def fibonacci(n):
    if n == 0:
        return 1  # Should return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import fibonacci

def test_fib_0():
    assert fibonacci(0) == 0

def test_fib_1():
    assert fibonacci(1) == 1

def test_fib_5():
    assert fibonacci(5) == 5

def test_fib_10():
    assert fibonacci(10) == 55
'''
        },
        {
            "id": "bug_003",
            "description": "Tree traversal missing None check",
            "difficulty": "medium",
            "expected_fix": "Add check for None node before accessing attributes",
            "buggy_code": '''class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root):
    result = []
    result.extend(inorder_traversal(root.left))  # Missing None check
    result.append(root.val)
    result.extend(inorder_traversal(root.right))
    return result''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import TreeNode, inorder_traversal

def test_single_node():
    root = TreeNode(1)
    assert inorder_traversal(root) == [1]

def test_left_child():
    root = TreeNode(2, TreeNode(1))
    assert inorder_traversal(root) == [1, 2]

def test_full_tree():
    root = TreeNode(2, TreeNode(1), TreeNode(3))
    assert inorder_traversal(root) == [1, 2, 3]

def test_empty_tree():
    assert inorder_traversal(None) == []
'''
        },
        {
            "id": "bug_004",
            "description": "Sum list recursive without base case",
            "difficulty": "easy",
            "expected_fix": "Add base case for empty list",
            "buggy_code": '''def sum_list(lst):
    return lst[0] + sum_list(lst[1:])  # Missing base case for empty list''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import sum_list

def test_normal_list():
    assert sum_list([1, 2, 3, 4, 5]) == 15

def test_single_element():
    assert sum_list([10]) == 10

def test_empty_list():
    assert sum_list([]) == 0

def test_negative_numbers():
    assert sum_list([-1, -2, 3]) == 0
'''
        },
        {
            "id": "bug_005",
            "description": "Power function infinite loop",
            "difficulty": "easy",
            "expected_fix": "Handle negative exponents and add base case",
            "buggy_code": '''def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp)  # Should be exp - 1''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import power

def test_power_2_3():
    assert power(2, 3) == 8

def test_power_5_0():
    assert power(5, 0) == 1

def test_power_3_2():
    assert power(3, 2) == 9

def test_power_10_1():
    assert power(10, 1) == 10
'''
        },
        {
            "id": "bug_006",
            "description": "GCD recursive wrong condition",
            "difficulty": "medium",
            "expected_fix": "Fix the recursive call order (b, a % b)",
            "buggy_code": '''def gcd(a, b):
    if b == 0:
        return a
    return gcd(a, a % b)  # Should be gcd(b, a % b)''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import gcd

def test_gcd_12_8():
    assert gcd(12, 8) == 4

def test_gcd_17_5():
    assert gcd(17, 5) == 1

def test_gcd_100_25():
    assert gcd(100, 25) == 25

def test_gcd_same():
    assert gcd(7, 7) == 7
'''
        },
        {
            "id": "bug_007",
            "description": "Reverse string recursion error",
            "difficulty": "easy",
            "expected_fix": "Fix the string slicing for recursion",
            "buggy_code": '''def reverse_string(s):
    if len(s) <= 1:
        return s
    return s[0] + reverse_string(s[1:])  # Should be reverse_string(s[1:]) + s[0]''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import reverse_string

def test_hello():
    assert reverse_string("hello") == "olleh"

def test_single_char():
    assert reverse_string("a") == "a"

def test_empty():
    assert reverse_string("") == ""

def test_palindrome():
    assert reverse_string("racecar") == "racecar"
'''
        },
        {
            "id": "bug_008",
            "description": "Count digits missing zero check",
            "difficulty": "easy",
            "expected_fix": "Handle zero as a special case (1 digit)",
            "buggy_code": '''def count_digits(n):
    if n < 10:
        return 1
    return 1 + count_digits(n // 10)

# Bug: doesn't handle 0 correctly - returns 1 but concept is ambiguous
# Actually the real bug: negative numbers cause infinite recursion''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import count_digits

def test_single_digit():
    assert count_digits(5) == 1

def test_two_digits():
    assert count_digits(42) == 2

def test_large_number():
    assert count_digits(12345) == 5

def test_zero():
    assert count_digits(0) == 1

def test_negative():
    assert count_digits(-123) == 3
'''
        },
        {
            "id": "bug_009",
            "description": "Palindrome check stack overflow",
            "difficulty": "medium",
            "expected_fix": "Fix the slicing to exclude both first and last characters",
            "buggy_code": '''def is_palindrome(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:])  # Should be s[1:-1]''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import is_palindrome

def test_racecar():
    assert is_palindrome("racecar") == True

def test_hello():
    assert is_palindrome("hello") == False

def test_single():
    assert is_palindrome("a") == True

def test_empty():
    assert is_palindrome("") == True

def test_two_same():
    assert is_palindrome("aa") == True
'''
        },
        {
            "id": "bug_010",
            "description": "Merge sort missing base case",
            "difficulty": "hard",
            "expected_fix": "Add proper base case check and fix merge logic",
            "buggy_code": '''def merge_sort(arr):
    if len(arr) == 0:  # Should be <= 1
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import merge_sort

def test_normal():
    assert merge_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]

def test_empty():
    assert merge_sort([]) == []

def test_single():
    assert merge_sort([1]) == [1]

def test_sorted():
    assert merge_sort([1, 2, 3]) == [1, 2, 3]

def test_reverse():
    assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
'''
        },
    ],
    "etl": [
        {
            "id": "bug_011",
            "description": "apply() on None values crashes",
            "difficulty": "medium",
            "expected_fix": "Handle None/NaN values before applying function",
            "buggy_code": '''import pandas as pd

def clean_names(df):
    df['name'] = df['name'].apply(lambda x: x.upper())  # Crashes on None
    return df''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import pandas as pd
from temp_module import clean_names

def test_normal_names():
    df = pd.DataFrame({'name': ['alice', 'bob']})
    result = clean_names(df)
    assert result['name'].tolist() == ['ALICE', 'BOB']

def test_with_none():
    df = pd.DataFrame({'name': ['alice', None, 'bob']})
    result = clean_names(df)
    assert result['name'].tolist() == ['ALICE', None, 'BOB']

def test_empty():
    df = pd.DataFrame({'name': []})
    result = clean_names(df)
    assert len(result) == 0
'''
        },
        {
            "id": "bug_012",
            "description": "groupby with NaN handling",
            "difficulty": "medium",
            "expected_fix": "Use dropna=False in groupby to include NaN groups",
            "buggy_code": '''import pandas as pd

def sum_by_category(df):
    return df.groupby('category')['value'].sum().to_dict()  # Drops NaN categories''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import pandas as pd
import numpy as np
from temp_module import sum_by_category

def test_normal():
    df = pd.DataFrame({'category': ['A', 'B', 'A'], 'value': [1, 2, 3]})
    result = sum_by_category(df)
    assert result == {'A': 4, 'B': 2}

def test_with_nan():
    df = pd.DataFrame({'category': ['A', None, 'A'], 'value': [1, 2, 3]})
    result = sum_by_category(df)
    assert 'A' in result and result['A'] == 4
    # NaN category should also be counted
    assert len(result) == 2
'''
        },
        {
            "id": "bug_013",
            "description": "merge with missing key column",
            "difficulty": "medium",
            "expected_fix": "Add validation for key column existence before merge",
            "buggy_code": '''import pandas as pd

def merge_dataframes(df1, df2, key):
    return pd.merge(df1, df2, on=key)  # No validation if key exists''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import pandas as pd
import pytest
from temp_module import merge_dataframes

def test_valid_merge():
    df1 = pd.DataFrame({'id': [1, 2], 'a': ['x', 'y']})
    df2 = pd.DataFrame({'id': [1, 2], 'b': ['p', 'q']})
    result = merge_dataframes(df1, df2, 'id')
    assert len(result) == 2

def test_missing_key():
    df1 = pd.DataFrame({'id': [1, 2], 'a': ['x', 'y']})
    df2 = pd.DataFrame({'other': [1, 2], 'b': ['p', 'q']})
    try:
        result = merge_dataframes(df1, df2, 'id')
        assert False, "Should raise error for missing key"
    except KeyError:
        pass
'''
        },
        {
            "id": "bug_014",
            "description": "dtype mismatch in concat",
            "difficulty": "hard",
            "expected_fix": "Ensure consistent dtypes before concatenation",
            "buggy_code": '''import pandas as pd

def concat_dataframes(dfs):
    return pd.concat(dfs, ignore_index=True)  # May cause dtype issues''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import pandas as pd
from temp_module import concat_dataframes

def test_same_types():
    df1 = pd.DataFrame({'a': [1, 2]})
    df2 = pd.DataFrame({'a': [3, 4]})
    result = concat_dataframes([df1, df2])
    assert result['a'].dtype == 'int64'

def test_mixed_types():
    df1 = pd.DataFrame({'a': [1, 2]})
    df2 = pd.DataFrame({'a': ['3', '4']})
    result = concat_dataframes([df1, df2])
    # After concat, all should be same type
    assert len(result) == 4
'''
        },
        {
            "id": "bug_015",
            "description": "fillna with wrong value type",
            "difficulty": "easy",
            "expected_fix": "Use appropriate fill value for the column dtype",
            "buggy_code": '''import pandas as pd

def fill_missing(df, column, value):
    df[column] = df[column].fillna(value)
    return df  # No type checking''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import pandas as pd
import numpy as np
from temp_module import fill_missing

def test_fill_numeric():
    df = pd.DataFrame({'a': [1.0, np.nan, 3.0]})
    result = fill_missing(df, 'a', 0)
    assert result['a'].tolist() == [1.0, 0.0, 3.0]

def test_fill_string():
    df = pd.DataFrame({'a': ['x', None, 'z']})
    result = fill_missing(df, 'a', 'missing')
    assert result['a'].tolist() == ['x', 'missing', 'z']
'''
        },
        {
            "id": "bug_016",
            "description": "incorrect column rename",
            "difficulty": "easy",
            "expected_fix": "Fix the rename dictionary or use correct method",
            "buggy_code": '''import pandas as pd

def rename_columns(df, old_name, new_name):
    df.rename(columns={old_name: new_name})  # Missing inplace=True or assignment
    return df''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import pandas as pd
from temp_module import rename_columns

def test_rename():
    df = pd.DataFrame({'old': [1, 2, 3]})
    result = rename_columns(df, 'old', 'new')
    assert 'new' in result.columns
    assert 'old' not in result.columns
'''
        },
        {
            "id": "bug_017",
            "description": "wrong aggregation function",
            "difficulty": "medium",
            "expected_fix": "Use correct aggregation (sum vs mean vs count)",
            "buggy_code": '''import pandas as pd

def calculate_totals(df, group_col, value_col):
    return df.groupby(group_col)[value_col].mean()  # Should be sum()''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import pandas as pd
from temp_module import calculate_totals

def test_totals():
    df = pd.DataFrame({
        'category': ['A', 'A', 'B'],
        'value': [10, 20, 15]
    })
    result = calculate_totals(df, 'category', 'value')
    assert result['A'] == 30
    assert result['B'] == 15
'''
        },
        {
            "id": "bug_018",
            "description": "index reset error",
            "difficulty": "easy",
            "expected_fix": "Use reset_index properly with drop parameter",
            "buggy_code": '''import pandas as pd

def reset_df_index(df):
    df.reset_index()  # Missing inplace or assignment
    return df''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import pandas as pd
from temp_module import reset_df_index

def test_reset():
    df = pd.DataFrame({'a': [1, 2, 3]}, index=[10, 20, 30])
    result = reset_df_index(df)
    assert list(result.index) == [0, 1, 2]
'''
        },
        {
            "id": "bug_019",
            "description": "duplicate column names",
            "difficulty": "medium",
            "expected_fix": "Handle or rename duplicate columns",
            "buggy_code": '''import pandas as pd

def add_column(df, name, values):
    df[name] = values  # Silently overwrites if exists
    return df''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import pandas as pd
from temp_module import add_column

def test_add_new():
    df = pd.DataFrame({'a': [1, 2]})
    result = add_column(df, 'b', [3, 4])
    assert 'b' in result.columns

def test_add_existing():
    df = pd.DataFrame({'a': [1, 2]})
    try:
        result = add_column(df, 'a', [3, 4])
        # Should raise error or rename, not silently overwrite
        assert result['a'].tolist() != [3, 4], "Should not silently overwrite"
    except ValueError:
        pass
'''
        },
        {
            "id": "bug_020",
            "description": "missing encoding in read_csv",
            "difficulty": "easy",
            "expected_fix": "Specify encoding parameter for non-ASCII data",
            "buggy_code": '''import pandas as pd

def read_csv_file(filepath):
    return pd.read_csv(filepath)  # Missing encoding for special characters''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import pandas as pd
import tempfile
import os
from temp_module import read_csv_file

def test_utf8():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write('name,city\\n')
        f.write('José,São Paulo\\n')
        filepath = f.name
    try:
        result = read_csv_file(filepath)
        assert result['name'][0] == 'José'
        assert result['city'][0] == 'São Paulo'
    finally:
        os.unlink(filepath)
'''
        },
    ],
    "sql": [
        {
            "id": "bug_021",
            "description": "NULL vs None comparison in SQLite",
            "difficulty": "medium",
            "expected_fix": "Use IS NULL instead of = NULL",
            "buggy_code": '''import sqlite3

def find_null_values(db_path, table, column):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: = NULL doesn't work in SQL, need IS NULL
    cursor.execute(f"SELECT * FROM {table} WHERE {column} = NULL")
    results = cursor.fetchall()
    conn.close()
    return results''',
            "test_code": '''import sys
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
        },
        {
            "id": "bug_022",
            "description": "JOIN without ON clause causing cartesian product",
            "difficulty": "medium",
            "expected_fix": "Add proper ON clause to JOIN",
            "buggy_code": '''import sqlite3

def join_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: Missing ON clause creates cartesian product
    cursor.execute("SELECT * FROM orders, customers")
    results = cursor.fetchall()
    conn.close()
    return results''',
            "test_code": '''import sys
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
        },
        {
            "id": "bug_023",
            "description": "WHERE clause syntax error",
            "difficulty": "easy",
            "expected_fix": "Use proper SQL string comparison syntax",
            "buggy_code": '''import sqlite3

def find_by_name(db_path, table, name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: Missing quotes around string value
    cursor.execute(f"SELECT * FROM {table} WHERE name = {name}")
    results = cursor.fetchall()
    conn.close()
    return results''',
            "test_code": '''import sys
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
        },
        {
            "id": "bug_024",
            "description": "GROUP BY missing column",
            "difficulty": "medium",
            "expected_fix": "Include all non-aggregated columns in GROUP BY",
            "buggy_code": '''import sqlite3

def get_stats_by_category(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: name not in GROUP BY but selected
    cursor.execute("SELECT category, name, SUM(amount) FROM sales GROUP BY category")
    results = cursor.fetchall()
    conn.close()
    return results''',
            "test_code": '''import sys
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
        },
        {
            "id": "bug_025",
            "description": "HAVING without GROUP BY",
            "difficulty": "medium",
            "expected_fix": "Add GROUP BY clause before HAVING",
            "buggy_code": '''import sqlite3

def filter_high_totals(db_path, min_total):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: HAVING without GROUP BY
    cursor.execute(f"SELECT category, SUM(amount) as total FROM sales HAVING total > {min_total}")
    results = cursor.fetchall()
    conn.close()
    return results''',
            "test_code": '''import sys
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
        },
        {
            "id": "bug_026",
            "description": "ORDER BY non-existent column",
            "difficulty": "easy",
            "expected_fix": "Use correct column name in ORDER BY",
            "buggy_code": '''import sqlite3

def get_sorted_users(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: column 'username' doesn't exist, should be 'name'
    cursor.execute("SELECT * FROM users ORDER BY username")
    results = cursor.fetchall()
    conn.close()
    return results''',
            "test_code": '''import sys
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
        },
        {
            "id": "bug_027",
            "description": "COUNT(*) with wrong filter",
            "difficulty": "easy",
            "expected_fix": "Fix WHERE clause condition",
            "buggy_code": '''import sqlite3

def count_active_users(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: Using = instead of True/1 for boolean
    cursor.execute("SELECT COUNT(*) FROM users WHERE active = 'true'")
    result = cursor.fetchone()[0]
    conn.close()
    return result''',
            "test_code": '''import sys
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
        },
        {
            "id": "bug_028",
            "description": "INNER JOIN instead of LEFT JOIN loses data",
            "difficulty": "medium",
            "expected_fix": "Use LEFT JOIN to preserve all left table rows",
            "buggy_code": '''import sqlite3

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
    return results''',
            "test_code": '''import sys
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
        },
        {
            "id": "bug_029",
            "description": "String concatenation with NULL returns NULL",
            "difficulty": "medium",
            "expected_fix": "Use COALESCE or IFNULL to handle NULL in concatenation",
            "buggy_code": '''import sqlite3

def get_full_names(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: NULL + string = NULL in SQL
    cursor.execute("SELECT first_name || ' ' || last_name as full_name FROM users")
    results = cursor.fetchall()
    conn.close()
    return [r[0] for r in results]''',
            "test_code": '''import sys
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
        },
        {
            "id": "bug_030",
            "description": "Date comparison format error",
            "difficulty": "medium",
            "expected_fix": "Use consistent date format (YYYY-MM-DD) for comparison",
            "buggy_code": '''import sqlite3

def get_recent_orders(db_path, date_str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Bug: Date format mismatch
    cursor.execute(f"SELECT * FROM orders WHERE order_date > '{date_str}'")
    results = cursor.fetchall()
    conn.close()
    return results''',
            "test_code": '''import sys
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
        },
    ],
    "async": [
        {
            "id": "bug_031",
            "description": "Missing await keyword",
            "difficulty": "easy",
            "expected_fix": "Add await before async function call",
            "buggy_code": '''import asyncio

async def fetch_data():
    await asyncio.sleep(0.1)
    return {"data": "result"}

async def process():
    result = fetch_data()  # Missing await
    return result''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import process

def test_process():
    result = asyncio.run(process())
    assert isinstance(result, dict)
    assert result.get("data") == "result"
'''
        },
        {
            "id": "bug_032",
            "description": "Sync function blocking async context",
            "difficulty": "medium",
            "expected_fix": "Use asyncio.to_thread or async version",
            "buggy_code": '''import asyncio
import time

def slow_sync():
    time.sleep(1)  # Blocks the event loop
    return "done"

async def main():
    result = slow_sync()
    return result''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import asyncio
import time
from temp_module import main

def test_main():
    start = time.time()
    result = asyncio.run(main())
    elapsed = time.time() - start
    assert result == "done"
    # Should complete quickly if properly async
    assert elapsed < 0.5
'''
        },
        {
            "id": "bug_033",
            "description": "Race condition in async counter",
            "difficulty": "hard",
            "expected_fix": "Use asyncio.Lock to protect shared state",
            "buggy_code": '''import asyncio

counter = 0

async def increment():
    global counter
    current = counter
    await asyncio.sleep(0.001)  # Simulates async work
    counter = current + 1

async def run_increments(n):
    global counter
    counter = 0
    await asyncio.gather(*[increment() for _ in range(n)])
    return counter''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import run_increments

def test_race_condition():
    result = asyncio.run(run_increments(100))
    # Should be 100 if properly synchronized
    assert result == 100
'''
        },
        {
            "id": "bug_034",
            "description": "asyncio.gather wrong usage",
            "difficulty": "medium",
            "expected_fix": "Pass coroutines, not coroutine functions",
            "buggy_code": '''import asyncio

async def task(n):
    await asyncio.sleep(0.01)
    return n * 2

async def run_tasks():
    # Bug: passing function, not coroutine
    results = await asyncio.gather(task, task, task)
    return results''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import run_tasks

def test_gather():
    results = asyncio.run(run_tasks())
    assert isinstance(results, (list, tuple))
    assert len(results) == 3
'''
        },
        {
            "id": "bug_035",
            "description": "Event loop already running error",
            "difficulty": "hard",
            "expected_fix": "Use asyncio.create_task or get_running_loop",
            "buggy_code": '''import asyncio

async def inner_task():
    return "result"

async def outer_task():
    # Bug: Can't call run() inside running loop
    result = asyncio.run(inner_task())
    return result''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import outer_task

def test_nested():
    result = asyncio.run(outer_task())
    assert result == "result"
'''
        },
        {
            "id": "bug_036",
            "description": "Timeout not handled",
            "difficulty": "medium",
            "expected_fix": "Use asyncio.wait_for with try/except",
            "buggy_code": '''import asyncio

async def slow_task():
    await asyncio.sleep(10)
    return "done"

async def run_with_timeout(timeout):
    result = await asyncio.wait_for(slow_task(), timeout=timeout)
    return result  # TimeoutError not handled''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import run_with_timeout

def test_timeout():
    result = asyncio.run(run_with_timeout(0.1))
    # Should return None or handle timeout gracefully
    assert result is None
'''
        },
        {
            "id": "bug_037",
            "description": "async with missing __aexit__",
            "difficulty": "hard",
            "expected_fix": "Implement both __aenter__ and __aexit__",
            "buggy_code": '''class AsyncResource:
    async def __aenter__(self):
        return self
    
    # Missing __aexit__

async def use_resource():
    async with AsyncResource() as r:
        return "used"''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import use_resource

def test_async_with():
    result = asyncio.run(use_resource())
    assert result == "used"
'''
        },
        {
            "id": "bug_038",
            "description": "Concurrent modification error",
            "difficulty": "hard",
            "expected_fix": "Avoid modifying collection during iteration",
            "buggy_code": '''import asyncio

async def process_items(items):
    results = []
    for item in items:
        await asyncio.sleep(0.001)
        results.append(item * 2)
        items.append(item)  # Modifying during iteration
    return results''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import process_items

def test_process():
    result = asyncio.run(process_items([1, 2, 3]))
    assert result == [2, 4, 6]
'''
        },
        {
            "id": "bug_039",
            "description": "Deadlock in async lock",
            "difficulty": "hard",
            "expected_fix": "Use timeout or avoid nested lock acquisition",
            "buggy_code": '''import asyncio

lock = asyncio.Lock()

async def task_a():
    async with lock:
        await asyncio.sleep(0.01)
        async with lock:  # Deadlock - already holding lock
            return "done"

async def run():
    return await task_a()''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import run

def test_no_deadlock():
    result = asyncio.run(asyncio.wait_for(run(), timeout=1))
    assert result == "done"
'''
        },
        {
            "id": "bug_040",
            "description": "Missing async context manager",
            "difficulty": "medium",
            "expected_fix": "Use contextlib.asynccontextmanager or implement __aenter__/__aexit__",
            "buggy_code": '''import asyncio
from contextlib import contextmanager

@contextmanager  # Should be asynccontextmanager
def async_resource():
    yield "resource"

async def use_resource():
    async with async_resource() as r:
        return r''',
            "test_code": '''import sys
sys.path.insert(0, '.')
import asyncio
from temp_module import use_resource

def test_resource():
    result = asyncio.run(use_resource())
    assert result == "resource"
'''
        },
    ],
    "edge_cases": [
        {
            "id": "bug_041",
            "description": "Division by zero",
            "difficulty": "easy",
            "expected_fix": "Check for zero divisor before division",
            "buggy_code": '''def safe_divide(a, b):
    return a / b  # No zero check''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import safe_divide

def test_normal():
    assert safe_divide(10, 2) == 5.0

def test_zero():
    result = safe_divide(10, 0)
    assert result is None or result == float('inf')

def test_negative():
    assert safe_divide(-10, 2) == -5.0
'''
        },
        {
            "id": "bug_042",
            "description": "Empty list index error",
            "difficulty": "easy",
            "expected_fix": "Check if list is empty before accessing",
            "buggy_code": '''def get_first(lst):
    return lst[0]  # Crashes on empty list''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import get_first

def test_normal():
    assert get_first([1, 2, 3]) == 1

def test_empty():
    result = get_first([])
    assert result is None

def test_single():
    assert get_first([42]) == 42
'''
        },
        {
            "id": "bug_043",
            "description": "Negative array index unintended",
            "difficulty": "medium",
            "expected_fix": "Validate index is non-negative",
            "buggy_code": '''def get_element(arr, index):
    return arr[index]  # Negative index wraps around''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import get_element

def test_positive():
    assert get_element([1, 2, 3], 0) == 1

def test_negative():
    # Negative index should raise error or return None, not wrap
    try:
        result = get_element([1, 2, 3], -1)
        assert result is None, "Should not return wrapped element"
    except IndexError:
        pass

def test_out_of_range():
    try:
        get_element([1, 2, 3], 10)
        assert False
    except IndexError:
        pass
'''
        },
        {
            "id": "bug_044",
            "description": "String index out of range",
            "difficulty": "easy",
            "expected_fix": "Check string length before indexing",
            "buggy_code": '''def get_char_at(s, index):
    return s[index]  # No bounds checking''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import get_char_at

def test_valid():
    assert get_char_at("hello", 0) == "h"

def test_out_of_range():
    result = get_char_at("hello", 10)
    assert result is None

def test_empty_string():
    result = get_char_at("", 0)
    assert result is None
'''
        },
        {
            "id": "bug_045",
            "description": "Dict KeyError",
            "difficulty": "easy",
            "expected_fix": "Use .get() or check key existence",
            "buggy_code": '''def get_value(d, key):
    return d[key]  # KeyError if missing''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import get_value

def test_exists():
    assert get_value({'a': 1}, 'a') == 1

def test_missing():
    result = get_value({'a': 1}, 'b')
    assert result is None

def test_default():
    result = get_value({}, 'any')
    assert result is None
'''
        },
        {
            "id": "bug_046",
            "description": "Integer overflow big factorial",
            "difficulty": "medium",
            "expected_fix": "Return error for large inputs or use arbitrary precision",
            "buggy_code": '''def big_factorial(n):
    if n <= 1:
        return 1
    return n * big_factorial(n - 1)  # Stack overflow for large n''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import big_factorial

def test_small():
    assert big_factorial(5) == 120

def test_large():
    # Should handle large numbers without stack overflow
    result = big_factorial(500)
    assert result > 0

def test_negative():
    result = big_factorial(-5)
    assert result is None or result == 1
'''
        },
        {
            "id": "bug_047",
            "description": "Float precision error",
            "difficulty": "medium",
            "expected_fix": "Use decimal module or approximate comparison",
            "buggy_code": '''def sum_floats(numbers):
    return sum(numbers)  # Float precision issues

def check_equal(a, b):
    return a == b  # Direct comparison fails for floats''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import sum_floats, check_equal

def test_sum():
    result = sum_floats([0.1, 0.2])
    assert check_equal(result, 0.3)

def test_precision():
    result = sum_floats([0.1] * 10)
    assert check_equal(result, 1.0)
'''
        },
        {
            "id": "bug_048",
            "description": "None type operation",
            "difficulty": "easy",
            "expected_fix": "Check for None before operation",
            "buggy_code": '''def double_value(x):
    return x * 2  # TypeError if x is None''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import double_value

def test_number():
    assert double_value(5) == 10

def test_none():
    result = double_value(None)
    assert result is None

def test_string():
    assert double_value("ab") == "abab"
'''
        },
        {
            "id": "bug_049",
            "description": "Infinite while loop",
            "difficulty": "easy",
            "expected_fix": "Add proper loop termination condition",
            "buggy_code": '''def countdown(n):
    result = []
    while n > 0:
        result.append(n)
        # Missing n -= 1
    return result''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import countdown

def test_countdown():
    result = countdown(5)
    assert result == [5, 4, 3, 2, 1]

def test_zero():
    result = countdown(0)
    assert result == []

def test_one():
    result = countdown(1)
    assert result == [1]
'''
        },
        {
            "id": "bug_050",
            "description": "Wrong comparison operator",
            "difficulty": "easy",
            "expected_fix": "Use correct comparison operator (< vs <=, == vs =)",
            "buggy_code": '''def find_max(lst):
    if not lst:
        return None
    max_val = lst[0]
    for val in lst:
        if val < max_val:  # Should be >
            max_val = val
    return max_val''',
            "test_code": '''import sys
sys.path.insert(0, '.')
from temp_module import find_max

def test_normal():
    assert find_max([1, 5, 3, 9, 2]) == 9

def test_single():
    assert find_max([42]) == 42

def test_empty():
    assert find_max([]) is None

def test_negative():
    assert find_max([-1, -5, -3]) == -1
'''
        },
    ],
}


def generate_bug_file(bug: dict, category: str) -> str:
    """Generate the content for a bug file."""
    return f'''"""
Bug Description: {bug['description']}
Category: {category}
Difficulty: {bug['difficulty']}
Expected Fix: {bug['expected_fix']}
"""

BUGGY_CODE = \'\'\'
{bug['buggy_code']}
\'\'\'

TEST_CODE = \'\'\'
{bug['test_code']}
\'\'\'

if __name__ == "__main__":
    print(f"Bug ID: {bug['id']}")
    print(f"Description: {bug['description']}")
    print(f"Category: {category}")
    print(f"Difficulty: {bug['difficulty']}")
    print("\\nBuggy Code:")
    print(BUGGY_CODE)
    print("\\nTest Code:")
    print(TEST_CODE)
'''


def generate_readme() -> str:
    """Generate README.md for the bugs directory."""
    readme = """# Bug Dataset for RLCEF Training

This directory contains 50 diverse buggy Python code examples across 5 categories,
designed for training and evaluating the RLCEF (Reinforcement Learning from Code Execution Feedback) agent.

## Categories

| Category | Count | Description |
|----------|-------|-------------|
| recursion | 10 | Recursive function bugs (base cases, termination) |
| etl | 10 | Pandas/data processing bugs |
| sql | 10 | SQLite query bugs |
| async | 10 | Asyncio/concurrency bugs |
| edge_cases | 10 | Common edge case handling bugs |

## Bug List

"""
    
    for category, bugs in BUGS.items():
        readme += f"### {category.title()}\n\n"
        readme += "| ID | Description | Difficulty |\n"
        readme += "|-----|-------------|------------|\n"
        for bug in bugs:
            readme += f"| {bug['id']} | {bug['description']} | {bug['difficulty']} |\n"
        readme += "\n"
    
    readme += """## Usage

Each bug file contains:
- `BUGGY_CODE`: The buggy Python code to fix
- `TEST_CODE`: Test code that the fixed function must pass

### Example

```python
from bugs.recursion.bug_001 import BUGGY_CODE, TEST_CODE
from src.agent.rlcef_loop import fix_code_with_rlcef

result = fix_code_with_rlcef(BUGGY_CODE, TEST_CODE)
print(f"Fixed: {result['success']}")
```

## Running All Bugs

```bash
python src/tools/run_all_bugs.py
```

This will run the RLCEF agent on all 50 bugs and generate training traces.
"""
    return readme


def main():
    """Generate all bug files and README."""
    print("Generating bug dataset...")
    
    # Create base bugs directory
    BUGS_DIR.mkdir(exist_ok=True)
    
    total_bugs = 0
    
    for category, bugs in BUGS.items():
        # Create category directory
        category_dir = BUGS_DIR / category
        category_dir.mkdir(exist_ok=True)
        
        # Create __init__.py for the category
        init_file = category_dir / "__init__.py"
        init_file.write_text(f'"""Bug category: {category}"""\n')
        
        for bug in bugs:
            # Generate and write bug file
            bug_file = category_dir / f"{bug['id']}.py"
            content = generate_bug_file(bug, category)
            bug_file.write_text(content)
            total_bugs += 1
            print(f"  Created: {bug_file}")
    
    # Create main __init__.py
    main_init = BUGS_DIR / "__init__.py"
    main_init.write_text('"""RLCEF Bug Dataset"""\n')
    
    # Generate README
    readme_file = BUGS_DIR / "README.md"
    readme_file.write_text(generate_readme())
    print(f"  Created: {readme_file}")
    
    print(f"\n✅ Generated {total_bugs} bug files across {len(BUGS)} categories")
    print(f"📁 Output directory: {BUGS_DIR.absolute()}")


if __name__ == "__main__":
    main()
