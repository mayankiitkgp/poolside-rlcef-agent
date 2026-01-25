"""
Code Sandbox Executor Module

This module provides a safe execution environment for running Python code with tests.
It uses pytest to execute test cases and captures detailed results.
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any


class CodeSandbox:
    """
    A sandbox environment for executing Python code with pytest tests.
    
    This class provides isolated execution of Python code along with test cases,
    capturing detailed results including pass/fail status, output, and errors.
    """
    
    def execute(
        self, 
        code_str: str, 
        test_str: str, 
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Execute Python code with pytest tests in a controlled environment.
        
        Args:
            code_str: The Python code to be tested (module implementation)
            test_str: The pytest test code to validate the implementation
            timeout: Maximum execution time in seconds (default: 30)
            
        Returns:
            A dictionary containing:
                - passed (bool): True if all tests passed
                - stdout (str): Full output from pytest
                - stderr (str): Error messages if any
                - tests (List[Dict]): List of test results with name, passed status, and errors
                
        Example:
            >>> sandbox = CodeSandbox()
            >>> result = sandbox.execute(code_str, test_str, timeout=10)
            >>> print(result['passed'])
            True
        """
        temp_dir = None
        temp_module_path = None
        temp_test_path = None
        
        try:
            # Create temporary directory for isolation
            temp_dir = tempfile.mkdtemp(prefix="code_sandbox_")
            temp_module_path = Path(temp_dir) / "temp_module.py"
            temp_test_path = Path(temp_dir) / "test_temp_module.py"
            
            # Write code and test files
            self._write_file(temp_module_path, code_str)
            self._write_file(temp_test_path, test_str)
            
            # Execute pytest with timeout
            result = self._run_pytest(temp_test_path, timeout)
            
            # Parse pytest output
            parsed_result = self._parse_pytest_output(
                result['stdout'], 
                result['stderr'],
                result['returncode']
            )
            
            return parsed_result
            
        except SyntaxError as e:
            return self._create_error_result(
                f"Syntax Error: {str(e)}",
                error_type="SyntaxError"
            )
        except subprocess.TimeoutExpired:
            return self._create_error_result(
                f"Execution timed out after {timeout} seconds",
                error_type="TimeoutError"
            )
        except Exception as e:
            return self._create_error_result(
                f"Unexpected error: {str(e)}",
                error_type=type(e).__name__
            )
        finally:
            # Clean up temporary files
            self._cleanup(temp_dir, temp_module_path, temp_test_path)
    
    def _write_file(self, path: Path, content: str) -> None:
        """Write content to a file, checking for syntax errors first."""
        # Check for syntax errors before writing
        try:
            compile(content, str(path), 'exec')
        except SyntaxError as e:
            raise SyntaxError(f"Syntax error in {path.name}: {e.msg} at line {e.lineno}")
        
        path.write_text(content, encoding='utf-8')
    
    def _run_pytest(self, test_path: Path, timeout: int) -> Dict[str, Any]:
        """Run pytest on the test file with specified timeout."""
        cmd = [
            "pytest",
            str(test_path),
            "-v",
            "--tb=short",
            "--color=no"  # Disable color codes for easier parsing
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=test_path.parent
            )
            
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except FileNotFoundError:
            raise ImportError(
                "pytest is not installed. Please install it with: pip install pytest"
            )
        except subprocess.TimeoutExpired:
            raise
    
    def _parse_pytest_output(
        self, 
        stdout: str, 
        stderr: str, 
        returncode: int
    ) -> Dict[str, Any]:
        """Parse pytest output to extract test results."""
        tests = []
        
        # Check for import errors or module errors in stderr
        if "ModuleNotFoundError" in stderr or "ImportError" in stderr:
            return self._create_error_result(
                f"Import Error: {stderr}",
                error_type="ImportError"
            )
        
        # Parse individual test results
        # Pattern: test_file.py::test_name PASSED or FAILED
        test_pattern = r'(test_\w+\.py::test_\w+)\s+(PASSED|FAILED)'
        matches = re.findall(test_pattern, stdout)
        
        for test_full_name, status in matches:
            # Extract just the test function name
            test_name = test_full_name.split("::")[-1]
            passed = (status == "PASSED")
            
            # Extract error message for failed tests
            error_msg = ""
            if not passed:
                error_msg = self._extract_error_for_test(stdout, test_name)
            
            tests.append({
                "name": test_name,
                "passed": passed,
                "error": error_msg
            })
        
        # Determine overall pass status
        all_passed = all(test['passed'] for test in tests) if tests else False
        
        # Handle case where no tests were collected
        if not tests and "no tests ran" in stdout.lower():
            return self._create_error_result(
                "No tests were collected",
                error_type="NoTestsError"
            )
        
        return {
            "passed": all_passed,
            "stdout": stdout,
            "stderr": stderr,
            "tests": tests
        }
    
    def _extract_error_for_test(self, stdout: str, test_name: str) -> str:
        """Extract error message for a specific failed test."""
        # Look for the test failure section
        pattern = rf'{test_name}.*?(?=test_\w+|=====|$)'
        match = re.search(pattern, stdout, re.DOTALL)
        
        if match:
            error_section = match.group(0)
            # Extract the actual error message (usually after "AssertionError" or similar)
            error_lines = []
            capture = False
            for line in error_section.split('\n'):
                if 'AssertionError' in line or 'Error' in line or 'assert' in line:
                    capture = True
                if capture and line.strip():
                    error_lines.append(line.strip())
                    if len(error_lines) >= 3:  # Limit error message length
                        break
            return ' '.join(error_lines) if error_lines else "Test failed"
        
        return "Test failed (error details not found)"
    
    def _create_error_result(
        self, 
        error_message: str, 
        error_type: str = "Error"
    ) -> Dict[str, Any]:
        """Create a standardized error result dictionary."""
        return {
            "passed": False,
            "stdout": "",
            "stderr": error_message,
            "tests": [{
                "name": error_type,
                "passed": False,
                "error": error_message
            }]
        }
    
    def _cleanup(
        self, 
        temp_dir: str, 
        temp_module_path: Path, 
        temp_test_path: Path
    ) -> None:
        """Clean up temporary files and directory."""
        try:
            if temp_module_path and temp_module_path.exists():
                temp_module_path.unlink()
            if temp_test_path and temp_test_path.exists():
                temp_test_path.unlink()
            if temp_dir and os.path.exists(temp_dir):
                os.rmdir(temp_dir)
        except Exception as e:
            # Log but don't raise - cleanup failures shouldn't break execution
            print(f"Warning: Cleanup failed: {e}")


# Example Usage
if __name__ == "__main__":
    # Example: Buggy factorial function with infinite recursion
    buggy_code = """
def factorial(n):
    '''Calculate factorial of n (buggy implementation with infinite recursion)'''
    if n == 0:
        return 1
    # Bug: missing base case check, will cause infinite recursion for negative numbers
    return n * factorial(n - 1)
"""

    test_code = """
from temp_module import factorial

def test_factorial_positive():
    '''Test factorial with positive number'''
    assert factorial(5) == 120
    assert factorial(3) == 6
    assert factorial(1) == 1

def test_factorial_zero():
    '''Test factorial with zero'''
    assert factorial(0) == 1
"""

    # Create sandbox and execute
    sandbox = CodeSandbox()
    result = sandbox.execute(buggy_code, test_code, timeout=5)
    
    # Display results
    print("=" * 60)
    print("CODE SANDBOX EXECUTION RESULTS")
    print("=" * 60)
    print(f"\nOverall Status: {'✓ PASSED' if result['passed'] else '✗ FAILED'}")
    print(f"\nTotal Tests: {len(result['tests'])}")
    print("\nIndividual Test Results:")
    print("-" * 60)
    
    for test in result['tests']:
        status = "✓ PASS" if test['passed'] else "✗ FAIL"
        print(f"\n{status} - {test['name']}")
        if test['error']:
            print(f"  Error: {test['error']}")
    
    print("\n" + "=" * 60)
    print("FULL OUTPUT:")
    print("=" * 60)
    print(result['stdout'])
    
    if result['stderr']:
        print("\n" + "=" * 60)
        print("ERRORS:")
        print("=" * 60)
        print(result['stderr'])
    
    print("\n" + "=" * 60)
    print("RETURNED DICTIONARY:")
    print("=" * 60)
    import json
    print(json.dumps(result, indent=2))
