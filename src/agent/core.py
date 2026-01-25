"""
RLCEF Agent Core Module

The main bug-fixing engine implementing industry best practices:
- Reflection pattern: Self-criticism before retry
- Loop detection: Prevents identical fix attempts
- Validation: Pre-submission syntax and signature checks
- Rich tracing: Detailed execution traces for training

This module provides the RLCEFAgent class with the fix_bug() method.
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from groq import Groq

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.agent.prompts import (
    SYSTEM_PROMPT,
    FIX_PROMPT,
    REFLECTION_PROMPT,
    format_previous_attempts,
    extract_test_error
)
from src.agent.utils import (
    detect_loop,
    clean_code_response,
    validate_python_syntax,
    check_signature_match,
    calculate_similarity
)
from src.sandbox.executor import CodeSandbox


class RLCEFAgent:
    """
    Reinforcement Learning from Code Execution Feedback Agent.
    
    This agent iteratively fixes buggy code using execution feedback,
    implementing reflection and loop detection patterns.
    """
    
    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",  
        max_iterations: int = 5,
        temperature: float = 0.7,
        loop_threshold: float = 0.90,
        enable_reflection: bool = True,
        enable_validation: bool = True,
        verbose: bool = True
    ):
        """
        Initialize the RLCEF Agent.
        
        Args:
            model: LLM model to use
            max_iterations: Maximum fix attempts
            temperature: LLM temperature (higher = more creative)
            loop_threshold: Similarity threshold for loop detection
            enable_reflection: Whether to use reflection prompt on retries
            enable_validation: Whether to validate syntax before execution
            verbose: Whether to print progress
        """
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = model
        self.max_iterations = max_iterations
        self.temperature = temperature
        self.loop_threshold = loop_threshold
        self.enable_reflection = enable_reflection
        self.enable_validation = enable_validation
        self.verbose = verbose
        self.sandbox = CodeSandbox()
    
    def fix_bug(
        self,
        buggy_code: str,
        test_code: str,
        save_trace: bool = True,
        trace_dir: str = "training_data"
    ) -> Dict[str, Any]:
        """
        Attempt to fix a buggy piece of code.
        
        Args:
            buggy_code: The buggy Python code
            test_code: The pytest test code
            save_trace: Whether to save execution trace
            trace_dir: Directory for saving traces
            
        Returns:
            Dictionary with success status, final code, and trace
        """
        attempts: List[Dict[str, Any]] = []
        final_code: Optional[str] = None
        success = False
        
        if self.verbose:
            print("🔧 Starting bug fix loop...")
        
        for iteration in range(1, self.max_iterations + 1):
            if self.verbose:
                print(f"\n--- Iteration {iteration}/{self.max_iterations} ---")
            
            # Generate fix prompt
            if iteration == 1:
                # First attempt: use standard fix prompt
                prompt = self._create_initial_prompt(buggy_code, test_code)
            else:
                # Subsequent attempts: use reflection prompt
                prompt = self._create_reflection_prompt(
                    buggy_code,
                    test_code,
                    attempts,
                    iteration
                )
            
            # Generate fix
            fixed_code = self._generate_fix(prompt)
            
            if self.verbose:
                print(f"📝 Generated fix ({len(fixed_code)} chars)")
            
            # Pre-validation
            if self.enable_validation:
                is_valid, validation_result = self._validate_fix(
                    fixed_code, 
                    buggy_code,
                    attempts
                )
                
                if not is_valid:
                    if self.verbose:
                        print(f"⚠️  Validation issue: {validation_result}")
                    # Request regeneration with higher temperature
                    fixed_code = self._regenerate_with_feedback(
                        prompt, 
                        validation_result,
                        min(self.temperature + 0.2, 1.0)
                    )
            
            # Execute tests
            result = self.sandbox.execute(fixed_code, test_code)
            
            # Record attempt
            attempt = {
                "iteration": iteration,
                "code": fixed_code,
                "passed": result.get("passed", False),
                "error": result.get("stderr", ""),
                "stdout": result.get("stdout", ""),
                "installed_packages": result.get("installed_packages", [])
            }
            attempts.append(attempt)
            
            if result.get("passed"):
                success = True
                final_code = fixed_code
                if self.verbose:
                    print(f"✅ Tests passed!")
                break
            else:
                if self.verbose:
                    error_preview = result.get("stderr", "")[:100]
                    print(f"❌ Tests failed: {error_preview}...")
        
        # Build result
        result_dict = {
            "success": success,
            "iterations": len(attempts),
            "final_code": final_code,
            "attempts": attempts,
            "buggy_code": buggy_code,
            "test_code": test_code
        }
        
        # Save trace
        if save_trace:
            trace_path = self._save_trace(result_dict, trace_dir)
            result_dict["trace_path"] = str(trace_path)
            if self.verbose:
                print(f"\n💾 Trace saved: {trace_path}")
        
        return result_dict
    
    def _create_initial_prompt(self, buggy_code: str, test_code: str) -> str:
        """Create the initial fix prompt."""
        return FIX_PROMPT.format(
            buggy_code=buggy_code,
            test_code=test_code
        )
    
    def _create_reflection_prompt(
        self,
        buggy_code: str,
        test_code: str,
        attempts: List[Dict],
        iteration: int
    ) -> str:
        """Create a reflection prompt with previous attempt analysis."""
        if not self.enable_reflection:
            return self._create_initial_prompt(buggy_code, test_code)
        
        last_attempt = attempts[-1]
        previous_code = last_attempt.get("code", "")
        test_error = extract_test_error(
            last_attempt.get("stdout", ""),
            last_attempt.get("error", "")
        )
        
        previous_summary = format_previous_attempts(attempts)
        
        return REFLECTION_PROMPT.format(
            buggy_code=buggy_code,
            test_code=test_code,
            iteration=iteration - 1,
            previous_code=previous_code,
            test_error=test_error,
            previous_attempts_summary=previous_summary
        )
    
    def _generate_fix(self, prompt: str) -> str:
        """Generate a fix using the LLM."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=2048
        )
        
        raw_response = response.choices[0].message.content
        return clean_code_response(raw_response)
    
    def _regenerate_with_feedback(
        self, 
        original_prompt: str, 
        feedback: str,
        temperature: float
    ) -> str:
        """Regenerate fix with validation feedback."""
        enhanced_prompt = f"""{original_prompt}

VALIDATION FEEDBACK (fix these issues):
{feedback}

Generate the corrected code:"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": enhanced_prompt}
            ],
            temperature=temperature,
            max_tokens=2048
        )
        
        raw_response = response.choices[0].message.content
        return clean_code_response(raw_response)
    
    def _validate_fix(
        self,
        fixed_code: str,
        original_code: str,
        previous_attempts: List[Dict]
    ) -> Tuple[bool, str]:
        """
        Validate a fix before execution.
        
        Checks:
        1. Syntax validity
        2. Function signature preservation
        3. Loop detection (similarity to previous attempts)
        
        Returns:
            Tuple of (is_valid, feedback_message)
        """
        issues = []
        
        # Check syntax
        is_valid_syntax, syntax_error = validate_python_syntax(fixed_code)
        if not is_valid_syntax:
            issues.append(f"Syntax error: {syntax_error}")
        
        # Check signature
        sig_match, sig_message = check_signature_match(original_code, fixed_code)
        if not sig_match:
            issues.append(f"Signature issue: {sig_message}")
        
        # Check for loops
        is_loop, similarity, matching_iter = detect_loop(
            fixed_code, 
            previous_attempts,
            self.loop_threshold
        )
        if is_loop:
            issues.append(
                f"Loop detected: {similarity:.0%} similar to attempt {matching_iter}. "
                "Try a fundamentally different approach."
            )
        
        if issues:
            return False, '\n'.join(issues)
        
        return True, "Valid"
    
    def _save_trace(self, result: Dict, trace_dir: str) -> Path:
        """Save execution trace for training data."""
        Path(trace_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_path = Path(trace_dir) / f"trace_{timestamp}.json"
        
        trace_data = {
            "timestamp": datetime.now().isoformat(),
            "model": self.model,
            "max_iterations": self.max_iterations,
            "reflection_enabled": self.enable_reflection,
            "buggy_code": result["buggy_code"],
            "test_code": result["test_code"],
            "attempts": result["attempts"],
            "final_code": result["final_code"],
            "success": result["success"],
            "iterations": result["iterations"]
        }
        
        with open(trace_path, 'w') as f:
            json.dump(trace_data, f, indent=2)
        
        return trace_path


# =============================================================================
# Convenience function for backward compatibility
# =============================================================================

def fix_code_with_rlcef(
    buggy_code: str,
    test_code: str,
    max_iterations: int = 5,
    save_trace: bool = True,
    enable_reflection: bool = True
) -> Dict[str, Any]:
    """
    Fix buggy code using the RLCEF agent.
    
    This is a convenience function for backward compatibility.
    
    Args:
        buggy_code: The buggy Python code
        test_code: pytest test code
        max_iterations: Maximum fix attempts
        save_trace: Whether to save execution trace
        enable_reflection: Whether to use reflection on retries
        
    Returns:
        Result dictionary with success status and trace
    """
    agent = RLCEFAgent(
        max_iterations=max_iterations,
        enable_reflection=enable_reflection,
        verbose=True
    )
    
    return agent.fix_bug(
        buggy_code=buggy_code,
        test_code=test_code,
        save_trace=save_trace
    )


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🤖 RLCEF Agent v2.0 - With Reflection & Loop Detection")
    print("=" * 70)
    
    # Demo bug
    buggy_code = '''
def factorial(n):
    return n * factorial(n - 1)  # Missing base case
'''

    test_code = '''
import sys
sys.path.insert(0, '.')
from temp_module import factorial

def test_factorial_5():
    assert factorial(5) == 120

def test_factorial_0():
    assert factorial(0) == 1

def test_factorial_1():
    assert factorial(1) == 1
'''

    print("\n📋 Buggy Code:")
    print(buggy_code)
    print("\n📋 Tests:")
    print(test_code[:200] + "...")
    print()
    
    result = fix_code_with_rlcef(
        buggy_code=buggy_code,
        test_code=test_code,
        save_trace=True,
        enable_reflection=True
    )
    
    print("\n" + "=" * 70)
    print("📊 RESULT")
    print("=" * 70)
    print(f"Success: {'✅ Yes' if result['success'] else '❌ No'}")
    print(f"Iterations: {result['iterations']}")
    
    if result['final_code']:
        print("\n📝 Final Code:")
        print("-" * 40)
        print(result['final_code'])
    
    print("=" * 70)
