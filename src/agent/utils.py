"""
RLCEF Agent Utilities Module

Contains utility functions for the RLCEF agent:
- Loop detection
- Code similarity checking  
- Code validation
- Response cleaning
"""

import re
import difflib
from typing import List, Dict, Any, Tuple, Optional


def calculate_similarity(code1: str, code2: str) -> float:
    """
    Calculate similarity ratio between two code snippets.
    
    Args:
        code1: First code snippet
        code2: Second code snippet
        
    Returns:
        Float between 0.0 (completely different) and 1.0 (identical)
    """
    if not code1 or not code2:
        return 0.0
    
    # Normalize whitespace for fairer comparison
    code1_normalized = ' '.join(code1.split())
    code2_normalized = ' '.join(code2.split())
    
    return difflib.SequenceMatcher(None, code1_normalized, code2_normalized).ratio()


def detect_loop(
    new_code: str, 
    previous_attempts: List[Dict[str, Any]], 
    threshold: float = 0.90
) -> Tuple[bool, float, Optional[int]]:
    """
    Detect if new code is too similar to a previous attempt.
    
    Args:
        new_code: The newly generated code
        previous_attempts: List of previous attempt dicts with 'code' key
        threshold: Similarity threshold to consider a loop (default 0.90)
        
    Returns:
        Tuple of (is_loop, max_similarity, matching_iteration)
    """
    if not previous_attempts:
        return False, 0.0, None
    
    max_similarity = 0.0
    matching_iteration = None
    
    for attempt in previous_attempts:
        prev_code = attempt.get('code', '')
        if not prev_code:
            continue
            
        similarity = calculate_similarity(new_code, prev_code)
        
        if similarity > max_similarity:
            max_similarity = similarity
            matching_iteration = attempt.get('iteration')
    
    is_loop = max_similarity >= threshold
    
    return is_loop, max_similarity, matching_iteration


def clean_code_response(response: str) -> str:
    """
    Clean LLM response to extract pure Python code.
    
    Removes:
    - Markdown code blocks
    - Explanatory text
    - Leading/trailing whitespace
    
    Args:
        response: Raw LLM response
        
    Returns:
        Cleaned Python code
    """
    code = response.strip()
    
    # Remove markdown code blocks
    if code.startswith("```python"):
        code = code[9:]
    elif code.startswith("```"):
        code = code[3:]
    
    if code.endswith("```"):
        code = code[:-3]
    
    code = code.strip()
    
    # Try to extract just the function if there's extra text
    lines = code.split('\n')
    clean_lines = []
    in_function = False
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines at start
        if not clean_lines and not stripped:
            continue
            
        # Detect function start
        if stripped.startswith('def ') or stripped.startswith('async def '):
            in_function = True
            indent_level = len(line) - len(line.lstrip())
            clean_lines.append(line)
            continue
        
        # If in function, include lines that are indented or empty
        if in_function:
            current_indent = len(line) - len(line.lstrip()) if stripped else indent_level + 1
            
            if stripped and current_indent <= indent_level and not stripped.startswith('def '):
                # End of function (new top-level code that's not a function)
                break
            
            clean_lines.append(line)
    
    if clean_lines:
        return '\n'.join(clean_lines)
    
    return code


def validate_python_syntax(code: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that code is syntactically correct Python.
    
    Args:
        code: Python code to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        compile(code, '<string>', 'exec')
        return True, None
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"


def extract_function_signature(code: str) -> Optional[str]:
    """
    Extract the function signature from code.
    
    Args:
        code: Python code containing a function definition
        
    Returns:
        Function signature string or None if not found
    """
    match = re.search(r'^(async\s+)?def\s+(\w+)\s*\([^)]*\)', code, re.MULTILINE)
    if match:
        return match.group(0)
    return None


def check_signature_match(original_code: str, fixed_code: str) -> Tuple[bool, str]:
    """
    Check if the fixed code preserves the original function signature.
    
    Args:
        original_code: Original buggy code
        fixed_code: Fixed code
        
    Returns:
        Tuple of (matches, message)
    """
    original_sig = extract_function_signature(original_code)
    fixed_sig = extract_function_signature(fixed_code)
    
    if not original_sig:
        return True, "Could not extract original signature"
    
    if not fixed_sig:
        return False, "Fixed code missing function definition"
    
    # Normalize whitespace
    original_normalized = ' '.join(original_sig.split())
    fixed_normalized = ' '.join(fixed_sig.split())
    
    if original_normalized == fixed_normalized:
        return True, "Signature preserved"
    
    # Check if just the function name matches
    original_name = re.search(r'def\s+(\w+)', original_sig)
    fixed_name = re.search(r'def\s+(\w+)', fixed_sig)
    
    if original_name and fixed_name and original_name.group(1) == fixed_name.group(1):
        return True, "Function name preserved (parameters may differ)"
    
    return False, f"Signature mismatch: expected '{original_sig}', got '{fixed_sig}'"


def get_code_hash(code: str) -> str:
    """
    Get a simple hash of code for quick comparison.
    
    Args:
        code: Python code
        
    Returns:
        Hash string
    """
    import hashlib
    normalized = ' '.join(code.split())
    return hashlib.md5(normalized.encode()).hexdigest()[:8]
