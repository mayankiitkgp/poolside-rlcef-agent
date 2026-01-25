# Bug Dataset for RLCEF Training

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

### Recursion

| ID | Description | Difficulty |
|-----|-------------|------------|
| bug_001 | Factorial missing base case | easy |
| bug_002 | Fibonacci off-by-one error | easy |
| bug_003 | Tree traversal missing None check | medium |
| bug_004 | Sum list recursive without base case | easy |
| bug_005 | Power function infinite loop | easy |
| bug_006 | GCD recursive wrong condition | medium |
| bug_007 | Reverse string recursion error | easy |
| bug_008 | Count digits missing zero check | easy |
| bug_009 | Palindrome check stack overflow | medium |
| bug_010 | Merge sort missing base case | hard |

### Etl

| ID | Description | Difficulty |
|-----|-------------|------------|
| bug_011 | apply() on None values crashes | medium |
| bug_012 | groupby with NaN handling | medium |
| bug_013 | merge with missing key column | medium |
| bug_014 | dtype mismatch in concat | hard |
| bug_015 | fillna with wrong value type | easy |
| bug_016 | incorrect column rename | easy |
| bug_017 | wrong aggregation function | medium |
| bug_018 | index reset error | easy |
| bug_019 | duplicate column names | medium |
| bug_020 | missing encoding in read_csv | easy |

### Sql

| ID | Description | Difficulty |
|-----|-------------|------------|
| bug_021 | NULL vs None comparison in SQLite | medium |
| bug_022 | JOIN without ON clause causing cartesian product | medium |
| bug_023 | WHERE clause syntax error | easy |
| bug_024 | GROUP BY missing column | medium |
| bug_025 | HAVING without GROUP BY | medium |
| bug_026 | ORDER BY non-existent column | easy |
| bug_027 | COUNT(*) with wrong filter | easy |
| bug_028 | INNER JOIN instead of LEFT JOIN loses data | medium |
| bug_029 | String concatenation with NULL returns NULL | medium |
| bug_030 | Date comparison format error | medium |

### Async

| ID | Description | Difficulty |
|-----|-------------|------------|
| bug_031 | Missing await keyword | easy |
| bug_032 | Sync function blocking async context | medium |
| bug_033 | Race condition in async counter | hard |
| bug_034 | asyncio.gather wrong usage | medium |
| bug_035 | Event loop already running error | hard |
| bug_036 | Timeout not handled | medium |
| bug_037 | async with missing __aexit__ | hard |
| bug_038 | Concurrent modification error | hard |
| bug_039 | Deadlock in async lock | hard |
| bug_040 | Missing async context manager | medium |

### Edge_Cases

| ID | Description | Difficulty |
|-----|-------------|------------|
| bug_041 | Division by zero | easy |
| bug_042 | Empty list index error | easy |
| bug_043 | Negative array index unintended | medium |
| bug_044 | String index out of range | easy |
| bug_045 | Dict KeyError | easy |
| bug_046 | Integer overflow big factorial | medium |
| bug_047 | Float precision error | medium |
| bug_048 | None type operation | easy |
| bug_049 | Infinite while loop | easy |
| bug_050 | Wrong comparison operator | easy |

## Usage

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
