"""
RLCEF Agent Prompts Module

Contains all prompts used by the RLCEF bug-fixing agent:
- SYSTEM_PROMPT: Base system context
- FIX_PROMPT: Initial bug fix request
- REFLECTION_PROMPT: Self-criticism before retry
- VALIDATION_PROMPT: Pre-submission validation

These prompts implement industry best practices:
- Reflection pattern (self-criticism)
- Anti-loop detection
- Concrete action requirements
"""

# =============================================================================
# SYSTEM PROMPT
# =============================================================================

SYSTEM_PROMPT = """You are an expert Python debugging agent specializing in fixing buggy code.

YOUR MISSION:
Fix the provided buggy Python function so it passes ALL tests.

CRITICAL RULES:
1. Output ONLY the corrected Python function code
2. NO markdown formatting (no ```)
3. NO explanations or comments about what you changed
4. NO additional functions unless they're required helpers
5. PRESERVE the original function signature exactly

DEBUGGING METHODOLOGY:
1. Read the test assertions to understand EXACT expected behavior
2. Trace through the buggy code mentally with test inputs
3. Identify the specific line(s) causing failure
4. Apply minimal, surgical fixes - don't rewrite unnecessarily
5. Verify your fix handles ALL test cases, including edge cases

COMMON BUG PATTERNS TO CHECK:
- Off-by-one errors in loops/recursion
- Missing base cases in recursion
- Wrong comparison operators (< vs <=, == vs is)
- Not handling None/empty inputs
- Integer division vs float division
- Mutable default arguments
- Variable shadowing
- Incorrect return placement

OUTPUT FORMAT:
Just the corrected function code, nothing else.
"""

# =============================================================================
# FIX PROMPT (Initial attempt)
# =============================================================================

FIX_PROMPT = """BUGGY CODE:
{buggy_code}

TESTS THAT MUST PASS:
{test_code}

ANALYSIS STEPS:
1. What does each test case expect?
2. What does the current code produce for each test?
3. Where is the mismatch?

Generate the corrected function code:"""

# =============================================================================
# REFLECTION PROMPT (After failed attempt)
# =============================================================================

REFLECTION_PROMPT = """BUGGY CODE:
{buggy_code}

TESTS THAT MUST PASS:
{test_code}

YOUR PREVIOUS FIX (FAILED):
{previous_code}

ERROR FROM TESTS:
{test_error}

ANALYSIS:
1. What does each test expect?
2. What did your previous fix produce?
3. Why is there a mismatch?

Try a DIFFERENT approach. Generate the corrected code:"""


# =============================================================================
# VALIDATION PROMPT (Pre-submission check)
# =============================================================================

VALIDATION_PROMPT = """Before submitting this fix, validate it:

PROPOSED FIX:
{proposed_code}

TESTS TO PASS:
{test_code}

VALIDATION CHECKLIST:
1. Does this fix handle the first test case? Trace through it.
2. Does this fix handle edge cases (empty input, None, zero)?
3. Is the function signature preserved exactly?
4. Are there any syntax errors?
5. Is this substantially different from previous failed attempts?

If the fix looks correct, output it unchanged.
If you spot an issue, output the corrected version.

Output ONLY the final function code:"""

# =============================================================================
# HELPER: Format previous attempts for reflection
# =============================================================================

def format_previous_attempts(attempts: list) -> str:
    """
    Format previous attempts into a summary for the reflection prompt.
    
    Args:
        attempts: List of previous attempt dictionaries with 'code' and 'iteration' keys
        
    Returns:
        Formatted string showing previous attempts
    """
    if not attempts:
        return "No previous attempts."
    
    summary = []
    for attempt in attempts:
        iteration = attempt.get('iteration', '?')
        code = attempt.get('code', 'N/A')
        passed = attempt.get('passed', False)
        
        # Get first 3 lines of code for summary
        code_lines = code.strip().split('\n')
        code_preview = '\n'.join(code_lines[:3])
        if len(code_lines) > 3:
            code_preview += f"\n  ... ({len(code_lines) - 3} more lines)"
        
        status = "✅ PASSED" if passed else "❌ FAILED"
        summary.append(f"Attempt {iteration} {status}:\n{code_preview}")
    
    return '\n\n'.join(summary)


# =============================================================================
# HELPER: Extract key error info
# =============================================================================

def extract_test_error(stdout: str, stderr: str) -> str:
    """
    Extract the most relevant error information from test output.
    
    Args:
        stdout: Standard output from pytest
        stderr: Standard error from pytest
        
    Returns:
        Formatted error string
    """
    combined = stdout + '\n' + stderr
    
    # Look for assertion errors
    lines = []
    capture = False
    
    for line in combined.split('\n'):
        if 'FAILED' in line or 'Error' in line or 'assert' in line:
            capture = True
        if capture:
            lines.append(line)
            if len(lines) >= 10:
                break
    
    if lines:
        return '\n'.join(lines)
    
    # Fallback to last part of output
    return combined[-500:] if len(combined) > 500 else combined
