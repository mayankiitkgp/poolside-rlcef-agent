"""
Code Sandbox Executor Module

This module provides a safe execution environment for running Python code with tests.
It uses pytest to execute test cases and captures detailed results.

Features:
- Isolated temp directory execution
- Auto-detection and installation of missing packages
- Detailed test result parsing
- Timeout protection
"""

import os
import re
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from datetime import datetime


# Common module name to package name mappings
# (when import name differs from pip package name)
MODULE_TO_PACKAGE = {
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
    "PIL": "Pillow",
    "yaml": "PyYAML",
    "bs4": "beautifulsoup4",
    "dateutil": "python-dateutil",
}


class CodeSandbox:
    """
    A sandbox environment for executing Python code with pytest tests.
    
    This class provides isolated execution of Python code along with test cases,
    capturing detailed results including pass/fail status, output, and errors.
    
    Features:
    - Self-healing: Auto-installs missing packages on first failure
    - Tracks installed dependencies
    - Writes discovered requirements to file for later review
    """
    
    def __init__(self, requirements_file: Optional[str] = "requirements_discovered.txt"):
        """
        Initialize the CodeSandbox.
        
        Args:
            requirements_file: Path to file for logging discovered dependencies.
                              Set to None to disable logging.
        """
        self.requirements_file = requirements_file
        self._session_installed: Set[str] = set()  # Track installs in this session
    
    def execute(
        self, 
        code_str: str, 
        test_str: str, 
        timeout: int = 30,
        pip_timeout: int = 60,
        max_install_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Execute Python code with pytest tests in a controlled environment.
        
        This method implements a self-healing pattern:
        1. Run pytest first
        2. If missing module detected, install it
        3. Retry pytest (up to max_install_retries times)
        
        Args:
            code_str: The Python code to be tested (module implementation)
            test_str: The pytest test code to validate the implementation
            timeout: Maximum execution time in seconds for pytest (default: 30)
            pip_timeout: Maximum time in seconds for pip install (default: 60)
            max_install_retries: Max number of install-retry cycles (default: 3)
            
        Returns:
            A dictionary containing:
                - passed (bool): True if all tests passed
                - stdout (str): Full output from pytest
                - stderr (str): Error messages if any
                - tests (List[Dict]): List of test results
                - installed_packages (List[str]): Packages auto-installed
                
        Example:
            >>> sandbox = CodeSandbox()
            >>> result = sandbox.execute(code_str, test_str, timeout=10)
            >>> print(result['passed'])
            True
        """
        temp_dir = None
        temp_module_path = None
        temp_test_path = None
        installed_packages: List[str] = []
        
        try:
            # Create temporary directory for isolation
            temp_dir = tempfile.mkdtemp(prefix="code_sandbox_")
            temp_module_path = Path(temp_dir) / "temp_module.py"
            temp_test_path = Path(temp_dir) / "test_temp_module.py"
            
            # Write code and test files
            self._write_file(temp_module_path, code_str)
            self._write_file(temp_test_path, test_str)
            
            # ---------------------------------------------------------
            # SELF-HEALING LOOP: Run pytest, detect missing modules,
            # install them, and retry
            # ---------------------------------------------------------
            retry_count = 0
            modules_installed_this_run: Set[str] = set()
            
            while retry_count <= max_install_retries:
                # Execute pytest
                result = self._run_pytest(temp_test_path, timeout)
                
                # Check for missing module errors
                missing_modules = self._extract_missing_modules(
                    result['stdout'], 
                    result['stderr']
                )
                
                # Filter out modules we've already tried to install
                new_missing = [m for m in missing_modules if m not in modules_installed_this_run]
                
                if not new_missing:
                    # No new missing modules - either success or real error
                    break
                
                # Install missing modules
                for module in new_missing:
                    install_success = self._install_package(
                        module, 
                        temp_dir, 
                        pip_timeout
                    )
                    modules_installed_this_run.add(module)
                    
                    if install_success:
                        installed_packages.append(module)
                        self._session_installed.add(module)
                        self._log_discovered_requirement(module)
                
                retry_count += 1
            
            # ---------------------------------------------------------
            # Parse final pytest output
            # ---------------------------------------------------------
            parsed_result = self._parse_pytest_output(
                result['stdout'], 
                result['stderr'],
                result['returncode']
            )
            
            # Add installed packages to result
            parsed_result['installed_packages'] = installed_packages
            
            return parsed_result
            
        except SyntaxError as e:
            return self._create_error_result(
                f"Syntax Error: {str(e)}",
                error_type="SyntaxError",
                installed_packages=installed_packages
            )
        except subprocess.TimeoutExpired:
            return self._create_error_result(
                f"Execution timed out after {timeout} seconds",
                error_type="TimeoutError",
                installed_packages=installed_packages
            )
        except Exception as e:
            return self._create_error_result(
                f"Unexpected error: {str(e)}",
                error_type=type(e).__name__,
                installed_packages=installed_packages
            )
        finally:
            # Clean up temporary files
            self._cleanup(temp_dir, temp_module_path, temp_test_path)
    
    def _extract_missing_modules(self, stdout: str, stderr: str) -> List[str]:
        """
        Extract missing module names from pytest output.
        
        Looks for patterns like:
        - ModuleNotFoundError: No module named 'pandas'
        - ImportError: No module named 'numpy'
        
        Returns:
            List of missing module names
        """
        combined = stdout + "\n" + stderr
        
        # Pattern to match "No module named 'module_name'" or "No module named module_name"
        patterns = [
            r"No module named ['\"](\w+)['\"]",
            r"No module named (\w+)",
            r"ModuleNotFoundError:.*['\"](\w+)['\"]",
        ]
        
        modules = set()
        for pattern in patterns:
            matches = re.findall(pattern, combined)
            modules.update(matches)
        
        return list(modules)
    
    def _install_package(
        self, 
        module_name: str, 
        temp_dir: str, 
        timeout: int
    ) -> bool:
        """
        Install a package using pip.
        
        Args:
            module_name: The module name (will be mapped to package name if needed)
            temp_dir: Target directory for installation
            timeout: Maximum time for pip install
            
        Returns:
            True if installation succeeded, False otherwise
        """
        # Map module name to package name if needed
        package_name = MODULE_TO_PACKAGE.get(module_name, module_name)
        
        try:
            # Use the current Python interpreter's pip
            cmd = [
                sys.executable, 
                '-m', 
                'pip', 
                'install', 
                package_name,
                '--quiet',
                '--disable-pip-version-check',
                '--target', temp_dir
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                print(f"  📦 Auto-installed: {package_name}")
                return True
            else:
                # If mapped name failed, try original module name
                if package_name != module_name:
                    cmd[4] = module_name
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=timeout
                    )
                    if result.returncode == 0:
                        print(f"  📦 Auto-installed: {module_name}")
                        return True
                
                print(f"  ⚠️  Failed to install: {package_name}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"  ⚠️  Timeout installing: {package_name}")
            return False
        except Exception as e:
            print(f"  ⚠️  Error installing {package_name}: {e}")
            return False
    
    def _log_discovered_requirement(self, module_name: str) -> None:
        """
        Log discovered requirements to a file for later review.
        
        Appends the module name with timestamp to requirements_discovered.txt
        """
        if not self.requirements_file:
            return
            
        try:
            package_name = MODULE_TO_PACKAGE.get(module_name, module_name)
            timestamp = datetime.now().isoformat()
            
            with open(self.requirements_file, 'a') as f:
                f.write(f"{package_name}  # discovered {timestamp}\n")
                
        except Exception as e:
            print(f"  ⚠️  Failed to log requirement: {e}")
    
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
        # Use system Python to ensure access to installed packages
        cmd = [
            sys.executable,
            '-m',
            'pytest',
            str(test_path),
            '-v',
            '--tb=short',
            '--color=no'  # Disable color codes for easier parsing
        ]
        
        # Set PYTHONPATH to include the temp directory
        env = os.environ.copy()
        parent_dir = str(test_path.parent)
        env['PYTHONPATH'] = parent_dir + os.pathsep + env.get('PYTHONPATH', '')
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=test_path.parent,
                env=env
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
        
        # Check for import errors or module errors in stderr/stdout
        combined = stdout + stderr
        if "ModuleNotFoundError" in combined or "ImportError" in combined:
            # Extract the actual error message
            error_match = re.search(r"(ModuleNotFoundError|ImportError):?\s*(.+?)(?:\n|$)", combined)
            error_msg = error_match.group(0).strip() if error_match else "Import error occurred"
            return self._create_error_result(
                error_msg,
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
        error_type: str = "Error",
        installed_packages: List[str] = None
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
            }],
            "installed_packages": installed_packages or []
        }
    
    def _cleanup(
        self, 
        temp_dir: str, 
        temp_module_path: Path, 
        temp_test_path: Path
    ) -> None:
        """Clean up temporary files and directory."""
        import shutil
        try:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            # Log but don't raise - cleanup failures shouldn't break execution
            print(f"Warning: Cleanup failed: {e}")


# Example Usage
if __name__ == "__main__":
    print("=" * 70)
    print("🧪 SELF-HEALING SANDBOX DEMO")
    print("=" * 70)
    
    # Example: Code that requires pandas (not in standard library)
    pandas_code = """
import pandas as pd

def clean_names(df):
    '''Clean name column by uppercasing, handling None values.'''
    df['name'] = df['name'].apply(lambda x: x.upper() if isinstance(x, str) else x)
    return df
"""

    pandas_test = """
import sys
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
"""

    print("\n📝 Testing code that imports 'pandas'...")
    print("   (Sandbox will auto-install if needed)\n")
    
    # Create sandbox and execute
    sandbox = CodeSandbox(requirements_file="requirements_discovered.txt")
    result = sandbox.execute(pandas_code, pandas_test, timeout=30, pip_timeout=60)
    
    # Display results
    print("\n" + "=" * 70)
    print("📊 EXECUTION RESULTS")
    print("=" * 70)
    print(f"\nOverall Status: {'✅ PASSED' if result['passed'] else '❌ FAILED'}")
    print(f"Total Tests: {len(result['tests'])}")
    
    if result.get('installed_packages'):
        print(f"\n📦 Auto-installed packages: {result['installed_packages']}")
    
    print("\nIndividual Test Results:")
    print("-" * 50)
    
    for test in result['tests']:
        status = "✅ PASS" if test['passed'] else "❌ FAIL"
        print(f"  {status} - {test['name']}")
        if test['error'] and not test['passed']:
            print(f"       Error: {test['error'][:80]}...")
    
    if result['stderr']:
        print("\n⚠️  Errors:")
        print(result['stderr'][:500])
    
    print("\n" + "=" * 70)
    print("✨ Demo complete!")
    print("=" * 70)
