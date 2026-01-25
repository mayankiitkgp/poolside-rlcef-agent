"""
Run All Bugs: Execute RLCEF agent on all 50 bugs and collect training traces.

This script iterates through all bug files in bugs/, runs the RLCEF agent
on each one, and collects execution traces for training data.
"""

import sys
import time
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.agent.core import RLCEFAgent


def load_bug(bug_file_path: Path) -> Tuple[Optional[str], Optional[str]]:
    """
    Load buggy code and test code from a bug file.
    
    Args:
        bug_file_path: Path to the bug file
        
    Returns:
        Tuple of (buggy_code, test_code) or (None, None) if loading fails
    """
    try:
        content = bug_file_path.read_text()
        
        # Create a namespace to execute the file
        namespace: Dict[str, Any] = {}
        exec(content, namespace)
        
        buggy_code = namespace.get('BUGGY_CODE', '').strip()
        test_code = namespace.get('TEST_CODE', '').strip()
        
        if not buggy_code or not test_code:
            print(f"  ⚠️  Warning: Missing BUGGY_CODE or TEST_CODE in {bug_file_path.name}")
            return None, None
            
        return buggy_code, test_code
        
    except SyntaxError as e:
        print(f"  ❌ Syntax error in {bug_file_path.name}: {e}")
        return None, None
    except Exception as e:
        print(f"  ❌ Error loading {bug_file_path.name}: {e}")
        return None, None


def get_bug_id(filepath: Path) -> str:
    """Extract bug ID from filepath for sorting."""
    match = re.search(r'bug_(\d+)', filepath.name)
    return match.group(1) if match else "999"


def run_all_bugs(
    max_iterations: int = 5,
    save_traces: bool = True,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run RLCEF agent on all bugs and collect statistics.
    
    Args:
        max_iterations: Max fix attempts per bug
        save_traces: Whether to save execution traces
        verbose: Print detailed progress
        
    Returns:
        Summary dictionary with results
    """
    bugs_dir = PROJECT_ROOT / "bugs"
    
    if not bugs_dir.exists():
        print("❌ bugs/ directory not found. Run generate_bugs.py first.")
        return {"error": "bugs directory not found"}
    
    # Find all bug files
    bug_files: List[Path] = []
    categories = ["recursion", "etl", "sql", "async", "edge_cases"]
    
    for category in categories:
        category_dir = bugs_dir / category
        if category_dir.exists():
            bug_files.extend(category_dir.glob("bug_*.py"))
    
    # Sort by bug ID
    bug_files.sort(key=lambda p: get_bug_id(p))
    
    total_bugs = len(bug_files)
    print(f"\n🔍 Found {total_bugs} bug files to process\n")
    print("=" * 70)
    
    # Track results
    results: List[Dict[str, Any]] = []
    fixed_count = 0
    failed_count = 0
    skipped_count = 0
    total_iterations = 0
    
    start_time = time.time()
    
    for idx, bug_file in enumerate(bug_files, 1):
        bug_id = bug_file.stem  # e.g., "bug_001"
        category = bug_file.parent.name  # e.g., "recursion"
        
        print(f"\n📦 [{idx}/{total_bugs}] Processing {bug_id} ({category})")
        print("-" * 50)
        
        # Load bug
        buggy_code, test_code = load_bug(bug_file)
        
        if buggy_code is None or test_code is None:
            print(f"  ⏭️  Skipping {bug_id} due to loading error")
            skipped_count += 1
            results.append({
                "bug_id": bug_id,
                "category": category,
                "status": "skipped",
                "error": "Failed to load bug file"
            })
            continue
        
        # Run RLCEF agent (v2.0 with reflection and loop detection)
        try:
            bug_start = time.time()
            
            # Use new reflection-enabled agent
            agent = RLCEFAgent(
                max_iterations=max_iterations,
                enable_reflection=True,
                enable_validation=True,
                verbose=False  # Clean output for batch processing
            )
            
            result = agent.fix_bug(
                buggy_code=buggy_code,
                test_code=test_code,
                save_trace=save_traces
            )
            bug_elapsed = time.time() - bug_start
            
            if result.get("success"):
                fixed_count += 1
                total_iterations += result.get("iterations", 0)
                print(f"  ✅ FIXED in {result.get('iterations', '?')} iteration(s) ({bug_elapsed:.1f}s)")
                results.append({
                    "bug_id": bug_id,
                    "category": category,
                    "status": "fixed",
                    "iterations": result.get("iterations"),
                    "time": bug_elapsed
                })
            else:
                failed_count += 1
                total_iterations += result.get("iterations", max_iterations)
                error_msg = result.get("error", "Max iterations reached")
                print(f"  ❌ FAILED after {result.get('iterations', max_iterations)} iterations")
                if verbose and error_msg:
                    print(f"     Error: {error_msg[:100]}...")
                results.append({
                    "bug_id": bug_id,
                    "category": category,
                    "status": "failed",
                    "iterations": result.get("iterations"),
                    "error": error_msg,
                    "time": bug_elapsed
                })
                
        except Exception as e:
            failed_count += 1
            print(f"  💥 CRASHED: {str(e)[:100]}")
            results.append({
                "bug_id": bug_id,
                "category": category,
                "status": "crashed",
                "error": str(e)
            })
    
    total_time = time.time() - start_time
    attempted = fixed_count + failed_count
    success_rate = (fixed_count / attempted * 100) if attempted > 0 else 0
    avg_time = total_time / total_bugs if total_bugs > 0 else 0
    avg_iterations = total_iterations / attempted if attempted > 0 else 0
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"  📁 Total bugs:        {total_bugs}")
    print(f"  ✅ Fixed:             {fixed_count}")
    print(f"  ❌ Failed:            {failed_count}")
    print(f"  ⏭️  Skipped:           {skipped_count}")
    print(f"  📈 Success rate:      {success_rate:.1f}%")
    print(f"  ⏱️  Total time:        {total_time:.1f}s")
    print(f"  ⏱️  Avg time/bug:      {avg_time:.1f}s")
    print(f"  🔄 Avg iterations:    {avg_iterations:.1f}")
    print("=" * 70)
    
    # Category breakdown
    print("\n📊 BY CATEGORY:")
    print("-" * 50)
    for category in categories:
        cat_results = [r for r in results if r["category"] == category]
        cat_fixed = sum(1 for r in cat_results if r["status"] == "fixed")
        cat_total = len(cat_results)
        cat_rate = (cat_fixed / cat_total * 100) if cat_total > 0 else 0
        status_emoji = "🟢" if cat_rate >= 70 else "🟡" if cat_rate >= 40 else "🔴"
        print(f"  {status_emoji} {category:12} {cat_fixed}/{cat_total} ({cat_rate:.0f}%)")
    print("-" * 50)
    
    summary = {
        "total_bugs": total_bugs,
        "fixed": fixed_count,
        "failed": failed_count,
        "skipped": skipped_count,
        "success_rate": success_rate,
        "total_time": total_time,
        "avg_time_per_bug": avg_time,
        "avg_iterations": avg_iterations,
        "results": results
    }
    
    # Save summary to file
    summary_file = PROJECT_ROOT / "training_data" / "run_summary.json"
    try:
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"\n💾 Summary saved to: {summary_file}")
    except Exception as e:
        print(f"\n⚠️  Failed to save summary: {e}")
    
    return summary


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🚀 RLCEF Bug Runner v2.0 - With Reflection & Loop Detection")
    print("=" * 70)
    print(f"📂 Project root: {PROJECT_ROOT}")
    print(f"📂 Training data: {PROJECT_ROOT / 'training_data'}")
    
    # Run all bugs
    summary = run_all_bugs(
        max_iterations=5,
        save_traces=True,
        verbose=True
    )
    
    print("\n" + "=" * 70)
    print("🏁 COMPLETE!")
    print("=" * 70)
    print(f"\n📂 Execution traces saved to: {PROJECT_ROOT / 'training_data'}")
    print("   Use these traces for model fine-tuning or analysis.\n")
