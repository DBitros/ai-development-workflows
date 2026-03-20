"""
Software Factory Validation Scenarios: {{FEATURE_NAME}}

These scenarios define SUCCESS for the factory run.
All must pass before shipping.

Project: {{PROJECT_NAME}}
Issue: {{ISSUE_ID}}
"""

import os
import subprocess
from pathlib import Path
import sys


# ============================================================================
# CONFIGURATION - CUSTOMIZE THESE PATHS FOR YOUR PROJECT
# ============================================================================

# Path to your project directory
# Adjust the number of .parent calls based on where this file lives
PROJECT_DIR = Path(__file__).parent.parent.parent  # {{ADJUST_THIS}}

# Specific directories in your project
# Example for web app:
# SRC_DIR = PROJECT_DIR / "src"
# PUBLIC_DIR = PROJECT_DIR / "public"

# Example for Python project:
# SRC_DIR = PROJECT_DIR / "src"
# TESTS_DIR = PROJECT_DIR / "tests"

{{YOUR_PROJECT_DIRS_HERE}}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_file_size(path: Path) -> int:
    """Get file size in bytes."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.stat().st_size


def read_file(path: Path) -> str:
    """Read file contents."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def run_command(cmd: str, cwd: Path = None) -> subprocess.CompletedProcess:
    """Run a shell command and return result."""
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd or PROJECT_DIR
    )


def file_exists(path: Path) -> bool:
    """Check if file exists."""
    return path.exists()


def file_contains(path: Path, text: str) -> bool:
    """Check if file contains specific text."""
    content = read_file(path)
    return text in content


# ============================================================================
# SCENARIO 1: {{SCENARIO_1_NAME}}
# ============================================================================

def test_scenario_1_{{SCENARIO_1_SLUG}}():
    """
    Scenario 1: {{SCENARIO_1_DESCRIPTION}}

    Given: {{GIVEN}}
    When: {{WHEN}}
    Then: {{THEN}}
    """
    print(f"\n✓ Scenario 1: {{SCENARIO_1_NAME}}")

    # Your test code here
    # Example:
    # result = your_function()
    # assert result.success, "Function should succeed"

    {{YOUR_TEST_CODE_HERE}}

    print(f"  ✅ PASS")
    return True


# ============================================================================
# SCENARIO 2: {{SCENARIO_2_NAME}}
# ============================================================================

def test_scenario_2_{{SCENARIO_2_SLUG}}():
    """
    Scenario 2: {{SCENARIO_2_DESCRIPTION}}

    Given: {{GIVEN}}
    When: {{WHEN}}
    Then: {{THEN}}
    """
    print(f"\n✓ Scenario 2: {{SCENARIO_2_NAME}}")

    {{YOUR_TEST_CODE_HERE}}

    print(f"  ✅ PASS")
    return True


# ============================================================================
# SCENARIO 3: {{SCENARIO_3_NAME}}
# ============================================================================

def test_scenario_3_{{SCENARIO_3_SLUG}}():
    """
    Scenario 3: {{SCENARIO_3_DESCRIPTION}}

    Given: {{GIVEN}}
    When: {{WHEN}}
    Then: {{THEN}}
    """
    print(f"\n✓ Scenario 3: {{SCENARIO_3_NAME}}")

    {{YOUR_TEST_CODE_HERE}}

    print(f"  ✅ PASS")
    return True


# ============================================================================
# ADD MORE SCENARIOS AS NEEDED
# ============================================================================


# ============================================================================
# Test Runner
# ============================================================================

def run_all_scenarios():
    """Run all validation scenarios."""
    print("=" * 70)
    print("SOFTWARE FACTORY VALIDATION: {{FEATURE_NAME}}")
    print("=" * 70)

    scenarios = [
        ("Scenario 1: {{SCENARIO_1_NAME}}", test_scenario_1_{{SCENARIO_1_SLUG}}),
        ("Scenario 2: {{SCENARIO_2_NAME}}", test_scenario_2_{{SCENARIO_2_SLUG}}),
        ("Scenario 3: {{SCENARIO_3_NAME}}", test_scenario_3_{{SCENARIO_3_SLUG}}),
        # Add more scenarios here
    ]

    results = []

    for name, test_func in scenarios:
        try:
            test_func()
            results.append((name, "PASS"))
        except AssertionError as e:
            results.append((name, f"FAIL: {e}"))
        except Exception as e:
            results.append((name, f"ERROR: {e}"))

    # Summary
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    passed = sum(1 for _, status in results if status == "PASS")
    total = len(results)

    for name, status in results:
        icon = "✅" if status == "PASS" else "❌"
        print(f"{icon} {name}: {status}")

    print(f"\nPass Rate: {passed}/{total} ({passed/total*100:.0f}%)")

    if passed == total:
        print("\n🎉 ALL SCENARIOS PASSED! Ready to ship!")
        return True
    else:
        print(f"\n⚠️  {total - passed} scenarios failed. Feed back to agent for iteration.")
        return False


if __name__ == "__main__":
    success = run_all_scenarios()
    sys.exit(0 if success else 1)
