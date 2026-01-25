"""
RLCEF Failure Analysis Tool

Analyzes failed bug-fixing attempts from the RLCEF agent.
Generates a detailed markdown report with:
- Root cause analysis for each failure
- Pattern detection across iterations
- Categorization of failure types
- Actionable recommendations

Usage:
    python src/tools/analyze_failures.py
"""

import json
import sys
import re
import difflib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class FailureCategory(Enum):
    """Categories of failure types for classification."""
    LOGIC_ERROR = "Logic Error"
    TEST_DESIGN_ISSUE = "Test Design Issue"
    EDGE_CASE_BLINDNESS = "Edge Case Blindness"
    SYNTAX_ERROR = "Syntax Error"
    DEPENDENCY_ISSUE = "Dependency Issue"
    IMPOSSIBLE_REQUIREMENT = "Impossible Requirement"


@dataclass
class BugAnalysis:
    """Analysis result for a single bug."""
    bug_id: str
    category: str
    iterations: int
    success: bool
    buggy_code: str
    test_code: str
    attempts: List[Dict[str, Any]]
    final_error: str
    failure_category: Optional[FailureCategory]
    root_cause: str
    recommended_fix: str
    loop_detected: bool
    similarity_scores: List[float]
    installed_packages: List[str]


# Mapping of trace files to bug info
FAILURE_TRACES = {
    "trace_20260125_205303.json": {"bug_id": "bug_003", "category": "recursion"},
    "trace_20260125_205352.json": {"bug_id": "bug_011", "category": "etl"},
    "trace_20260125_205508.json": {"bug_id": "bug_020", "category": "etl"},
    "trace_20260125_205521.json": {"bug_id": "bug_032", "category": "async"},
    "trace_20260125_205532.json": {"bug_id": "bug_040", "category": "async"},
}


def calculate_similarity(code1: str, code2: str) -> float:
    """
    Calculate similarity ratio between two code snippets.
    Returns a float between 0 and 1.
    """
    if not code1 or not code2:
        return 0.0
    return difflib.SequenceMatcher(None, code1, code2).ratio()


def detect_loop(attempts: List[Dict]) -> Tuple[bool, List[float]]:
    """
    Detect if the agent made identical or very similar fixes across iterations.
    Returns (loop_detected, similarity_scores).
    """
    if len(attempts) < 2:
        return False, []
    
    similarity_scores = []
    for i in range(1, len(attempts)):
        prev_code = attempts[i-1].get("code", "")
        curr_code = attempts[i].get("code", "")
        score = calculate_similarity(prev_code, curr_code)
        similarity_scores.append(score)
    
    # Loop detected if any consecutive attempts are > 95% similar
    loop_detected = any(score > 0.95 for score in similarity_scores)
    
    return loop_detected, similarity_scores


def extract_final_error(attempts: List[Dict]) -> str:
    """Extract the final error message from the last attempt."""
    if not attempts:
        return "No attempts recorded"
    
    last_attempt = attempts[-1]
    error = last_attempt.get("error", "")
    stdout = last_attempt.get("stdout", "")
    
    # Try to extract assertion error or other specific errors
    combined = error + stdout
    
    # Look for common error patterns
    patterns = [
        r"AssertionError:?\s*(.+?)(?:\n|$)",
        r"TypeError:?\s*(.+?)(?:\n|$)",
        r"ValueError:?\s*(.+?)(?:\n|$)",
        r"E\s+assert\s+(.+?)(?:\n|$)",
        r"FAILED.*?-\s*(.+?)(?:\n|$)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, combined, re.MULTILINE)
        if match:
            return match.group(0).strip()[:200]
    
    return error[:200] if error else "Unknown error"


def categorize_failure(
    buggy_code: str, 
    test_code: str, 
    attempts: List[Dict],
    final_error: str,
    bug_category: str
) -> Tuple[FailureCategory, str, str]:
    """
    Analyze the failure and categorize it.
    Returns (category, root_cause, recommended_fix).
    """
    # Check for dependency issues
    if "ModuleNotFoundError" in final_error or "ImportError" in final_error:
        return (
            FailureCategory.DEPENDENCY_ISSUE,
            "Missing package/module that couldn't be auto-installed",
            "Add the required package to requirements.txt or handle import gracefully"
        )
    
    # Check for syntax errors
    if "SyntaxError" in final_error:
        return (
            FailureCategory.SYNTAX_ERROR,
            "Agent generated syntactically invalid Python code",
            "Add syntax validation before retry; include original code structure in prompt"
        )
    
    # Check for impossible timing requirements (async)
    if "elapsed" in final_error.lower() or "time" in test_code.lower():
        if bug_category == "async":
            return (
                FailureCategory.IMPOSSIBLE_REQUIREMENT,
                "Test expects timing that cannot be achieved (e.g., make 1s sleep run in <0.5s)",
                "Revise test to check non-blocking behavior differently, not wall-clock time"
            )
    
    # Check for async-specific issues
    if "async" in buggy_code.lower() or "async" in bug_category:
        if "generator" in final_error or "await" in final_error or "async" in final_error:
            return (
                FailureCategory.LOGIC_ERROR,
                "Agent doesn't understand async/await protocol (e.g., asynccontextmanager requires async def)",
                "Add explicit async patterns to system prompt; show correct async idioms as examples"
            )
    
    # Check for edge case issues
    if "None" in final_error or "empty" in final_error.lower() or "0" in final_error:
        return (
            FailureCategory.EDGE_CASE_BLINDNESS,
            "Agent missed edge cases like empty input, None values, or boundary conditions",
            "Add 'check edge cases' reminder to prompt; parse test cases to extract edge conditions"
        )
    
    # Check if test might be poorly designed
    if len(attempts) >= 5:
        # Check if agent tried reasonable fixes but all failed
        codes = [a.get("code", "") for a in attempts]
        if len(set(codes)) >= 3:  # At least 3 different attempts
            return (
                FailureCategory.TEST_DESIGN_ISSUE,
                "Agent tried multiple valid approaches but none satisfied the test - test may be too strict or ambiguous",
                "Review test assertions; consider if expected behavior is clearly specified"
            )
    
    # Default to logic error
    return (
        FailureCategory.LOGIC_ERROR,
        "Agent didn't correctly understand the bug or fix pattern",
        "Improve prompting with more specific debugging guidance"
    )


def load_trace(trace_path: Path) -> Optional[Dict]:
    """Load a trace file, handling missing files gracefully."""
    if not trace_path.exists():
        print(f"  ⚠️  Trace file not found: {trace_path.name}")
        return None
    
    try:
        with open(trace_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"  ❌ Invalid JSON in {trace_path.name}: {e}")
        return None


def analyze_bug(trace_data: Dict, bug_info: Dict) -> BugAnalysis:
    """Analyze a single bug's execution trace."""
    bug_id = bug_info["bug_id"]
    category = bug_info["category"]
    
    buggy_code = trace_data.get("buggy_code", "")
    test_code = trace_data.get("test_code", "")
    attempts = trace_data.get("attempts", [])
    success = trace_data.get("success", False)
    iterations = trace_data.get("iterations", len(attempts))
    
    # Extract installed packages if any
    installed_packages = []
    for attempt in attempts:
        stdout = attempt.get("stdout", "")
        # Look for our auto-install message
        pkg_matches = re.findall(r"Auto-installed: (\w+)", stdout)
        installed_packages.extend(pkg_matches)
    installed_packages = list(set(installed_packages))
    
    # Detect loops
    loop_detected, similarity_scores = detect_loop(attempts)
    
    # Get final error
    final_error = extract_final_error(attempts)
    
    # Categorize failure
    failure_category, root_cause, recommended_fix = categorize_failure(
        buggy_code, test_code, attempts, final_error, category
    )
    
    return BugAnalysis(
        bug_id=bug_id,
        category=category,
        iterations=iterations,
        success=success,
        buggy_code=buggy_code,
        test_code=test_code,
        attempts=attempts,
        final_error=final_error,
        failure_category=failure_category,
        root_cause=root_cause,
        recommended_fix=recommended_fix,
        loop_detected=loop_detected,
        similarity_scores=similarity_scores,
        installed_packages=installed_packages
    )


def truncate_code(code: str, max_lines: int = 30) -> str:
    """Truncate code to max_lines, adding ellipsis if needed."""
    lines = code.strip().split('\n')
    if len(lines) <= max_lines:
        return code.strip()
    return '\n'.join(lines[:max_lines]) + f"\n... ({len(lines) - max_lines} more lines)"


def generate_markdown_report(analyses: List[BugAnalysis]) -> str:
    """Generate a comprehensive markdown failure report."""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M IST")
    total_bugs = 50
    failures = len(analyses)
    successes = total_bugs - failures
    
    report = f"""# RLCEF Agent Failure Analysis

**Generated:** {timestamp}  
**Success Rate:** {successes}/{total_bugs} ({successes/total_bugs*100:.0f}%)  
**Failures Analyzed:** {failures}

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Bugs | {total_bugs} |
| Successes | {successes} |
| Failures | {failures} |
| Success Rate | {successes/total_bugs*100:.0f}% |

### Failure Categories

"""
    
    # Count by category
    category_counts: Dict[str, int] = {}
    for analysis in analyses:
        cat_name = analysis.failure_category.value if analysis.failure_category else "Unknown"
        category_counts[cat_name] = category_counts.get(cat_name, 0) + 1
    
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        report += f"- **{cat}:** {count} bug(s)\n"
    
    report += "\n---\n\n## Detailed Failure Analysis\n\n"
    
    # Individual bug analyses
    for analysis in analyses:
        report += f"""### Bug #{analysis.bug_id.split('_')[1]} ({analysis.category})

**Category:** {analysis.category}  
**Iterations:** {analysis.iterations} (max reached)  
**Loop Detected:** {"Yes ⚠️" if analysis.loop_detected else "No"}  
"""
        
        if analysis.installed_packages:
            report += f"**Auto-installed Packages:** {', '.join(analysis.installed_packages)}\n"
        
        report += f"""**Final Error:** 
```
{analysis.final_error}
```

#### Original Buggy Code
```python
{truncate_code(analysis.buggy_code)}
```

#### Test Requirements
```python
{truncate_code(analysis.test_code, 20)}
```

#### Fix Attempts

"""
        
        # Show each attempt
        for i, attempt in enumerate(analysis.attempts, 1):
            code = attempt.get("code", "N/A")
            passed = attempt.get("passed", False)
            error = attempt.get("error", "") or attempt.get("stdout", "")[:200]
            
            # Calculate similarity to previous if not first
            sim_note = ""
            if i > 1 and i-2 < len(analysis.similarity_scores):
                sim = analysis.similarity_scores[i-2]
                if sim > 0.95:
                    sim_note = f" ⚠️ **{sim*100:.0f}% similar to previous**"
                elif sim > 0.8:
                    sim_note = f" ({sim*100:.0f}% similar)"
            
            status = "✅ PASSED" if passed else "❌ FAILED"
            report += f"""**Iteration {i}:**{sim_note}
```python
{truncate_code(code, 15)}
```
Result: {status}

"""
            if not passed:
                # Extract key error
                error_short = error.replace('\n', ' ')[:150]
                report += f"Error: `{error_short}...`\n\n"
        
        # Root cause and recommendations
        cat_name = analysis.failure_category.value if analysis.failure_category else "Unknown"
        report += f"""#### Root Cause Analysis

{analysis.root_cause}

#### Failure Category

- [{"x" if cat_name == "Logic Error" else " "}] Logic Error
- [{"x" if cat_name == "Test Design Issue" else " "}] Test Design Issue  
- [{"x" if cat_name == "Edge Case Blindness" else " "}] Edge Case Blindness
- [{"x" if cat_name == "Syntax Error" else " "}] Syntax Error
- [{"x" if cat_name == "Dependency Issue" else " "}] Dependency Issue
- [{"x" if cat_name == "Impossible Requirement" else " "}] Impossible Requirement

#### Recommended Fix

{analysis.recommended_fix}

---

"""
    
    # Summary section
    report += """## Failure Patterns

### By Bug Category

"""
    
    bug_category_counts: Dict[str, int] = {}
    for analysis in analyses:
        bug_category_counts[analysis.category] = bug_category_counts.get(analysis.category, 0) + 1
    
    for cat, count in sorted(bug_category_counts.items(), key=lambda x: -x[1]):
        report += f"- **{cat}:** {count} failure(s)\n"
    
    # Loop detection summary
    loops = [a for a in analyses if a.loop_detected]
    if loops:
        report += f"\n### Loop Detection\n\n"
        report += f"**{len(loops)} bug(s)** showed the agent repeating similar fixes:\n"
        for a in loops:
            report += f"- {a.bug_id}: similarity scores {[f'{s:.0%}' for s in a.similarity_scores]}\n"
    
    # Common mistakes
    report += """
### Common Mistakes Observed

1. **Agent loops on same approach** - Doesn't try fundamentally different strategies
2. **Doesn't parse test assertions** - Misses exact requirements from test code
3. **Async pattern gaps** - Doesn't know `asynccontextmanager` requires `async def`
4. **Timing assumptions** - Can't reason about wall-clock time requirements

### Recommendations

#### Immediate (Prompt Engineering)

1. Add reflection step: "Why did the previous fix fail? What's different about this attempt?"
2. Parse test assertions explicitly and include in prompt
3. Add async-specific patterns to system prompt
4. Limit identical retries (if >90% similar, force different approach)

#### Fine-Tuning (Training Data)

1. Collect traces where agent correctly pivoted strategy
2. Include async idiom examples (asynccontextmanager + async def)
3. Add edge case reasoning chains

#### Test Design

1. Avoid timing-based assertions for async tests
2. Make expected behavior explicit in test names
3. Add comments explaining edge cases

---

*Report generated by `src/tools/analyze_failures.py`*
"""
    
    return report


def main():
    """Main entry point for failure analysis."""
    print("\n" + "=" * 70)
    print("🔍 RLCEF FAILURE ANALYSIS TOOL")
    print("=" * 70)
    
    training_data_dir = PROJECT_ROOT / "training_data"
    
    if not training_data_dir.exists():
        print("❌ training_data/ directory not found!")
        return
    
    print(f"\n📂 Scanning: {training_data_dir}")
    print(f"📊 Analyzing {len(FAILURE_TRACES)} failed traces...\n")
    
    analyses: List[BugAnalysis] = []
    
    for trace_filename, bug_info in FAILURE_TRACES.items():
        trace_path = training_data_dir / trace_filename
        print(f"  📄 {trace_filename} ({bug_info['bug_id']})...", end=" ")
        
        trace_data = load_trace(trace_path)
        if trace_data is None:
            print("SKIPPED")
            continue
        
        analysis = analyze_bug(trace_data, bug_info)
        analyses.append(analysis)
        
        status = "✅" if analysis.success else "❌"
        loop = "🔄" if analysis.loop_detected else ""
        print(f"{status} {analysis.failure_category.value if analysis.failure_category else 'Unknown'} {loop}")
    
    if not analyses:
        print("\n⚠️  No traces could be loaded. Check file paths.")
        return
    
    # Generate report
    print(f"\n📝 Generating failure report...")
    report = generate_markdown_report(analyses)
    
    # Save report
    report_path = training_data_dir / "failure_report.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"✅ Report saved to: {report_path}")
    
    # Print summary to console
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    print(f"\nFailures analyzed: {len(analyses)}")
    
    print("\nBy failure category:")
    category_counts: Dict[str, int] = {}
    for a in analyses:
        cat = a.failure_category.value if a.failure_category else "Unknown"
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  • {cat}: {count}")
    
    loops = sum(1 for a in analyses if a.loop_detected)
    if loops:
        print(f"\n⚠️  Loop detected in {loops} bug(s)")
    
    print("\n" + "=" * 70)
    print("✨ Analysis complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
