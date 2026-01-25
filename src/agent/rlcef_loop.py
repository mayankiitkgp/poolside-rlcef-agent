import os
import json
import argparse
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

from src.sandbox.executor import CodeSandbox


def fix_code_with_rlcef(
    buggy_code: str,
    test_code: str,
    max_iterations: int = 5,
    save_trace: bool = True
) -> Dict[str, Any]:
    """
    Fix buggy code using RLCEF loop with Groq LLM and sandbox execution.
    
    Args:
        buggy_code: The buggy Python function code to fix
        test_code: Test code that the fixed function must pass
        max_iterations: Maximum number of fix attempts (default: 5)
        save_trace: Whether to save execution trace to training_data/ (default: True)
    
    Returns:
        Dictionary containing:
        - success: bool - Whether the code was successfully fixed
        - final_code: str or None - The corrected code if successful
        - iterations: int - Number of iterations used
        - trace: List[Dict] - History of attempts and feedback
    """
    # Load environment variables and get API key
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found in environment. "
            "Please set it in your .env file."
        )
    
    # Initialize Groq client
    client = Groq(api_key=api_key)
    model = "llama-3.3-70b-versatile"
    
    # Create training_data directory if it doesn't exist
    if save_trace:
        Path("training_data").mkdir(exist_ok=True)
    
    # Initialize loop variables
    iteration = 0
    conversation_history: List[Dict[str, Any]] = []
    sandbox = CodeSandbox()
    
    # System prompt for the LLM
    system_prompt = (
        "You are an expert code fixing agent. Fix Python functions to pass all tests. "
        "Output ONLY the corrected Python function code with no markdown, "
        "no explanations, no backticks."
    )
    
    # Result variable to store final outcome
    result_dict = {
        "success": False,
        "final_code": None,
        "iterations": max_iterations,
        "trace": conversation_history
    }
    
    # Main RLCEF loop
    try:
        while iteration < max_iterations:
            # Format previous attempts and feedback
            feedback_section = ""
            if conversation_history:
                feedback_section = "\n".join([
                    f"Attempt {entry['iteration']}:\n"
                    f"Code:\n{entry['code']}\n"
                    f"Result: {'PASSED' if entry['feedback'].get('passed') else 'FAILED'}\n"
                    f"Feedback: {entry['feedback'].get('error', 'N/A')}\n"
                    for entry in conversation_history
                ])
            else:
                feedback_section = "No previous attempts yet."
            
            # Build user prompt
            user_prompt = f"""BUGGY CODE:
{buggy_code}

TESTS TO PASS:
{test_code}

PREVIOUS ATTEMPTS AND FEEDBACK:
{feedback_section}

Generate the corrected function code:"""
            
            # Call Groq API
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=2000
                )
                
                # Extract generated code
                generated_code = response.choices[0].message.content.strip()
                
                # Strip markdown formatting if present
                if generated_code.startswith("```python"):
                    generated_code = generated_code.replace("```python", "", 1)
                if generated_code.startswith("```"):
                    generated_code = generated_code.replace("```", "", 1)
                if generated_code.endswith("```"):
                    generated_code = generated_code.rsplit("```", 1)[0]
                generated_code = generated_code.strip()
                
            except Exception as e:
                # Handle API failures
                error_result = {
                    "success": False,
                    "final_code": None,
                    "iterations": iteration + 1,
                    "trace": conversation_history,
                    "error": f"API call failed: {str(e)}"
                }
                result_dict = error_result
                break
            
            # Execute the generated code with tests
            try:
                execution_result = sandbox.execute(generated_code, test_code, timeout=10)
            except Exception as e:
                execution_result = {
                    "passed": False,
                    "error": f"Execution error: {str(e)}",
                    "stdout": "",
                    "stderr": str(e)
                }
            
            # Check if tests passed
            if execution_result.get("passed", False):
                # Success! Return the fixed code
                conversation_history.append({
                    "iteration": iteration + 1,
                    "code": generated_code,
                    "feedback": execution_result
                })
                result_dict = {
                    "success": True,
                    "final_code": generated_code,
                    "iterations": iteration + 1,
                    "trace": conversation_history
                }
                break
            
            # Tests failed, record attempt and continue
            conversation_history.append({
                "iteration": iteration + 1,
                "code": generated_code,
                "feedback": execution_result
            })
            iteration += 1
            
            # Update result specific to failure case if loop finishes
            if iteration == max_iterations:
                result_dict = {
                    "success": False,
                    "final_code": None,
                    "iterations": max_iterations,
                    "trace": conversation_history
                }

    finally:
        # Save trace if requested
        if save_trace:
            trace = {
                "timestamp": datetime.now().isoformat(),
                "buggy_code": buggy_code,
                "test_code": test_code,
                "attempts": [
                    {
                        "iteration": entry['iteration'],
                        "code": entry['code'],
                        "passed": entry['feedback'].get('passed', False),
                        "error": entry['feedback'].get('stderr', '') or entry['feedback'].get('error', ''),
                        "stdout": entry['feedback'].get('stdout', '')
                    }
                    for entry in conversation_history
                ],
                "final_code": result_dict.get('final_code'),
                "success": result_dict.get('success', False),
                "iterations": result_dict.get('iterations', 0)
            }
            
            trace_filename = f"trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            trace_file = Path("training_data") / trace_filename
            try:
                with open(trace_file, 'w') as f:
                    json.dump(trace, f, indent=2)
                print(f"\n✅ Trace saved to: {trace_file}")
            except Exception as e:
                print(f"\n❌ Failed to save trace: {e}")

    return result_dict


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Run RLCEF agent to fix buggy code")
    parser.add_argument("--save-trace", action=argparse.BooleanOptionalAction, default=True, help="Save execution traces to training_data/")
    args = parser.parse_args()
    
    # Define buggy code (factorial with missing base case - infinite recursion)
    buggy_code = """def factorial(n):
    return n * factorial(n - 1)  # missing base case"""
    
    # Define test code
    test_code = """import sys
sys.path.insert(0, '.')
from temp_module import factorial

def test_factorial_5():
    assert factorial(5) == 120

def test_factorial_0():
    assert factorial(0) == 1

def test_factorial_1():
    assert factorial(1) == 1

def test_factorial_3():
    assert factorial(3) == 6
"""
    
    # Run RLCEF loop
    print("=" * 60)
    print("RLCEF Loop: Fixing Buggy Factorial Function")
    print("=" * 60)
    print(f"\nBuggy Code:\n{buggy_code}\n")
    print(f"Tests:\n{test_code}\n")
    print("=" * 60)
    print("Starting RLCEF loop...\n")
    
    result = fix_code_with_rlcef(
        buggy_code, 
        test_code, 
        max_iterations=5,
        save_trace=args.save_trace
    )
    
    # Print results
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    if result["success"]:
        print(f"✅ SUCCESS! Fixed in {result['iterations']} iteration(s)\n")
        print("Final Code:")
        print("-" * 60)
        print(result["final_code"])
        print("-" * 60)
    else:
        print(f"❌ FAILED after {result['iterations']} iteration(s)\n")
        if "error" in result:
            print(f"Error: {result['error']}\n")
    
    # Show trace of attempts
    print("\n" + "=" * 60)
    print("TRACE OF ATTEMPTS")
    print("=" * 60)
    
    for entry in result["trace"]:
        print(f"\n--- Iteration {entry['iteration']} ---")
        print(f"Code:\n{entry['code']}\n")
        
        feedback = entry["feedback"]
        if feedback.get("passed"):
            print("✅ PASSED")
        else:
            print("❌ FAILED")
            # Prefer showing the error string if it exists
            error_msg = feedback.get('error')
            if not error_msg and feedback.get('stderr'):
                error_msg = feedback.get('stderr')
            elif not error_msg:
                error_msg = "Unknown error"
                
            print(f"Error: {error_msg}")
            
            if feedback.get("stderr") and feedback.get("stderr") != error_msg:
                print(f"Stderr: {feedback['stderr']}")
            if feedback.get("stdout"):
                print(f"Stdout: {feedback['stdout']}")
    
    print("\n" + "=" * 60)
