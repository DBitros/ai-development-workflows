---
description: Run tests with intelligent auto-fix retry loop
---

# Test and Fix

Run comprehensive tests with auto-fix retry loop (up to 3 attempts).

## Usage

```bash
# Test specific ticket
/test-and-fix VLP-123

# Test latest generated code
/test-and-fix

# Test with custom max attempts
/test-and-fix VLP-123 --max-attempts 5
```

## What It Does

Runs the Test Runner Agent to:

1. **Execute Comprehensive Tests**
   - Swift unit tests (Quick/Nimble)
   - iOS UI tests (iOS Simulator MCP)
   - Web tests (Playwright MCP)
   - API integration tests
   - Module integration tests

2. **Auto-Fix on Failure**
   When tests fail, automatically:
   - **Analyze**: Categorize errors (syntax, imports, types, etc.)
   - **Research**: Deep dive into codebase for patterns
   - **Fix**: Generate and apply intelligent fixes
   - **Retest**: Validate fixes
   - **Retry**: Up to 3 attempts

3. **Deep Research on Failure**
   Uses same research agents as `/ios-workflow`:
   - `/agents:codebase-pattern-finder` - Find similar working implementations
   - `/agents:codebase-analyzer` - Analyze existing patterns
   - `/agents:codebase-locator` - Locate relevant code

## Auto-Fix Process

```
Test Fails
    ↓
Analyze Failure (categorize error type)
    ↓
Deep Research (search codebase, check requirements, review architecture)
    ↓
Generate Fix (based on research findings)
    ↓
Apply Fix (modify code automatically)
    ↓
Re-run Tests
    ↓
Still Failing? → Retry (up to 3 times)
    ↓
Success or Manual Review Needed
```

## Output

Test report with:
- **Test Results**: Pass/fail breakdown by type
- **Success Rate**: Overall percentage
- **Fix Attempts**: Detailed log of each auto-fix
- **Failure Analysis**: Root cause identification
- **Recommendations**: Next steps if manual intervention needed

**Report Location**: `test-reports/[TICKET-ID]-test-report.md`

## Example Output

```
🧪 Test and Fix Complete: VLP-123

Test Results:
  ✅ Unit Tests: 15/15 passed
  ✅ iOS UI Tests: 3/3 passed
  ⏭️ Web Tests: 0 skipped
  ✅ API Tests: 2/2 passed
  ✅ Integration: 1/1 passed

Success Rate: 100%
Total Duration: 12.5s

Auto-Fix Attempts: 2
  Attempt 1: Fixed missing import (Foundation)
  Attempt 2: Fixed type mismatch in API response handling

Final Status: ✅ ALL TESTS PASSED

Full report: test-reports/VLP-123-test-report.md
```

## Example with Failures

```
🧪 Test and Fix Complete: VLP-123

Test Results:
  ✅ Unit Tests: 12/15 passed
  ❌ iOS UI Tests: 2/3 failed
  ⏭️ Web Tests: 0 skipped
  ✅ API Tests: 2/2 passed
  ✅ Integration: 1/1 passed

Success Rate: 85%
Total Duration: 18.3s

Auto-Fix Attempts: 3

  Attempt 1: Fixed syntax error in UserCache.swift
    ✅ Re-test: 13/15 unit tests passed

  Attempt 2: Added missing UIKit import
    ✅ Re-test: 14/15 unit tests passed

  Attempt 3: Complex type error - requires manual review
    ❌ Re-test: Still 1 failing test

Failed Tests:
  ❌ UserProfileCacheTests.testConcurrentAccess
     Error: Thread sanitizer detected data race
     Location: UserProfileCacheTests.swift:78

Recommendations:
  1. Review thread safety in UserProfileCache.swift
  2. Add synchronization for cache access
  3. Consider using actor pattern for Swift 5.5+

Final Status: ⚠️ MANUAL REVIEW NEEDED

Full report: test-reports/VLP-123-test-report.md
```

## Research Details

When tests fail, the system researches:

### 1. Codebase Patterns
```
Searching 25,976+ Swift files for:
  - Similar test implementations
  - Successful patterns for same functionality
  - Error handling approaches
```

### 2. Requirements Context
```
Reviewing specification documents:
  - Layer 3 requirements
  - Research findings
  - Implementation plan
```

### 3. Architecture Guidance
```
Consulting TradeMe iOS architecture:
  - Universal API patterns
  - Dependencies framework usage
  - Platform service integration
  - Testing best practices
```

### 4. Similar Implementations
```
Finding successful examples:
  - Working test suites
  - Proven fix patterns
  - Architecture-compliant solutions
```

## Fix Success Rate

Based on error type:

| Error Type | Auto-Fix Success Rate |
|-----------|----------------------|
| Syntax Errors | ~95% |
| Missing Imports | ~90% |
| Simple Type Errors | ~70% |
| Complex Logic | ~40% |
| Thread Safety | ~20% |

## Execution

When invoked:

1. Determine test types needed (based on code)
2. Run all applicable tests
3. If failures detected:
   - Analyze failure patterns
   - Launch deep research
   - Generate fixes based on research
   - Apply fixes automatically
   - Re-run tests
   - Repeat up to 3 times
4. Generate comprehensive test report
5. Display summary with recommendations

## When to Use

- **After code generation** - Validate generated code
- **Before committing** - Ensure all tests pass
- **After manual changes** - Quick validation
- **Debugging test failures** - Auto-fix capabilities
- **CI/CD integration** - Automated testing with fixes

## Integration with MCP Tools

The Test Runner uses MCP tools for advanced testing:

### iOS Simulator MCP
```
Tools used:
  - mcp__ios-simulator__launch_app
  - mcp__ios-simulator__ui_tap
  - mcp__ios-simulator__ui_type
  - mcp__ios-simulator__screenshot
  - mcp__ios-simulator__ui_describe_all
```

### Playwright MCP
```
Tools used:
  - mcp__plugin_playwright_playwright__browser_navigate
  - mcp__plugin_playwright_playwright__browser_click
  - mcp__plugin_playwright_playwright__browser_type
  - mcp__plugin_playwright_playwright__browser_snapshot
```

*Note: Full MCP integration is implemented in the Test Runner Agent*

---

*🧪 Powered by TradeMe Test Runner Agent with Deep Research*
