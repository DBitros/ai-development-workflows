# Workflow Guide: When to Use What

This guide helps you choose the right workflow tool for your task.

## 🎯 Quick Decision Tree

```
Need to develop new feature?
│
├─ YES → Is it iOS-specific with requirements phase?
│   │
│   ├─ YES → Use `/ios-workflow`
│   │         (Requirements-first, interactive, iOS-focused)
│   │
│   └─ NO → Use `/multi-agent-dev`
│             (Full 7-stage workflow with security & testing)
│
└─ NO → What do you need?
    │
    ├─ Security scan only → `/security-scan`
    │
    ├─ Test with auto-fix → `/test-and-fix`
    │
    ├─ Automated/batch → `python orchestrator.py`
    │
    └─ Check status → Check generated-specs/ and reports/
```

---

## 📊 Comparison Matrix

| Feature | `/ios-workflow` | `/multi-agent-dev` | Python Orchestrator | `/security-scan` | `/test-and-fix` |
|---------|----------------|-------------------|-------------------|-----------------|----------------|
| **Interactive** | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| **Approval Gates** | ✅ Each phase | ✅ Each stage | ❌ None | ❌ None | ❌ None |
| **iOS-Specific** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Requirements Phase** | ✅ Yes (Layer 3) | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Security Scan** | ❌ No | ✅ Yes (Stage 5) | ✅ Yes | ✅ Only | ❌ No |
| **Auto-Fix Testing** | ❌ No | ✅ Yes (Stage 6) | ✅ Yes | ❌ No | ✅ Only |
| **Deep Research** | ✅ Yes (Phase 2) | ✅ Yes (Stage 2, 6) | ✅ Yes | ❌ No | ✅ Yes |
| **CI/CD Ready** | ❌ No | ❌ No | ✅ Yes | ⚠️ Partial | ⚠️ Partial |
| **Batch Processing** | ❌ No | ❌ No | ✅ Yes | ❌ No | ❌ No |
| **MCP Integration** | ✅ Firebase, Context7 | ✅ iOS Sim, Playwright | ✅ All MCPs | ❌ No | ✅ iOS Sim, Playwright |
| **Worktree Support** | ✅ Yes (Phase 6) | ❌ No | ❌ No | ❌ No | ❌ No |
| **Architecture Validation** | ✅ Every phase | ✅ Stage 1, 7 | ✅ Yes | ❌ No | ❌ No |
| **Use Case** | iOS features with specs | General development | Automation | Quick security check | Test validation |

---

## 📋 Detailed Workflow Comparisons

### `/ios-workflow` - Requirements-First iOS Development

**Best for**:
- ✅ New iOS features requiring specifications
- ✅ Complex features needing thorough research
- ✅ When you want requirements before code
- ✅ Jira tickets requiring documentation
- ✅ Crashlytics bug investigations
- ✅ Features needing worktree isolation

**Process**:
```
0. Git Branch Setup (TradeMe project)
   ↓
1. Requirements Definition (Layer 3)
   ↓
2. Targeted Research (codebase analysis)
   ↓
3. Requirements Refinement (with findings)
   ↓
4. Advisory Council (optional technical review)
   ↓
5. Implementation Planning (Layer 5-6)
   ↓
6. Implementation Setup (worktree option)
```

**Research Agents Used**:
- `/agents:codebase-pattern-finder`
- `/agents:codebase-analyzer`
- `/agents:codebase-locator`

**Outputs**:
- `specifications/3-requirements/TICKET-ID-requirements.md`
- `specifications/4-research/TICKET-ID-research.md`
- `specifications/6-implementation-design-and-planning/TICKET-ID-implementation-plan.md`

**When NOT to use**:
- ❌ Quick fixes or small changes
- ❌ When specifications already exist
- ❌ Non-iOS projects
- ❌ When you need security/testing phases

---

### `/multi-agent-dev` - Complete 7-Stage Development

**Best for**:
- ✅ Full end-to-end development with security & testing
- ✅ When security audit is required
- ✅ When automated testing is needed
- ✅ Complex features requiring all phases
- ✅ Production-ready code generation
- ✅ When you want approval at each stage

**Process**:
```
1. Architecture Analysis
   ↓
2. Requirements Research
   ↓
3. Implementation Planning
   ↓
4. Code Generation
   ↓
5. Security Audit (OWASP Mobile Top 10, iOS security)
   ↓
6. Testing & Auto-Fix (up to 3 retry attempts)
   ↓
7. Quality Assurance
```

**Research Capabilities**:
- Stage 2: Deep codebase research (same agents as `/ios-workflow`)
- Stage 6: Research on test failures for auto-fix

**Outputs**:
- All specification documents (requirements, research, architecture, plan)
- Generated Swift code with tests
- Security report with risk assessment
- Test report with auto-fix attempts
- QA report with quality score

**When NOT to use**:
- ❌ Just need requirements (use `/ios-workflow`)
- ❌ Just need security scan (use `/security-scan`)
- ❌ Just need testing (use `/test-and-fix`)
- ❌ Automated/batch execution (use Python orchestrator)

---

### Python Orchestrator - Automated Execution

**Best for**:
- ✅ CI/CD pipeline integration
- ✅ Batch processing multiple tickets
- ✅ Headless/unattended execution
- ✅ Automated code generation workflows
- ✅ When user interaction not available

**Usage**:
```bash
# Single ticket
python3 orchestrator.py "VLP-123: Add caching layer"

# Resume previous workflow
python3 orchestrator.py --resume VLP-123

# Validate completed work
python3 orchestrator.py --validate VLP-123

# List all workflows
python3 orchestrator.py --list
```

**Process**:
- Same 7 stages as `/multi-agent-dev`
- **NO approval gates** - runs automatically
- Saves state for resume if interrupted
- Can be triggered from CI/CD

**Outputs**: Same as `/multi-agent-dev`

**When NOT to use**:
- ❌ When you want to review each stage
- ❌ Exploratory development work
- ❌ Learning how the system works
- ❌ When you might want to adjust mid-workflow

---

### `/security-scan` - Quick Security Audit

**Best for**:
- ✅ Quick security check on existing code
- ✅ Before committing code
- ✅ Before creating PR
- ✅ Independent security validation
- ✅ Checking for common vulnerabilities

**What it scans**:
- OWASP Mobile Top 10 vulnerabilities
- iOS-specific security (Keychain, certificate pinning, biometrics)
- API security (auth, tokens, PII)
- Code security (hardcoded secrets, logging)

**Usage**:
```bash
# Scan specific ticket
/security-scan VLP-123

# Scan latest generated code
/security-scan
```

**Output**:
- Security grade (A+ to F)
- Risk score (0-100)
- Findings by severity
- Remediation recommendations
- Report: `security-reports/TICKET-ID-security-report.md`

**When NOT to use**:
- ❌ When full workflow needed
- ❌ If security is just one part of larger process

---

### `/test-and-fix` - Testing with Auto-Fix

**Best for**:
- ✅ Validating generated code
- ✅ Running tests with auto-fix capabilities
- ✅ Debugging test failures
- ✅ Before committing changes
- ✅ Quick test validation

**What it tests**:
- Unit tests (Swift/Quick/Nimble)
- iOS UI tests (iOS Simulator MCP)
- Web tests (Playwright MCP)
- API integration tests
- Module integration tests

**Auto-Fix Process**:
1. Analyzes failures (categorize error types)
2. Deep research (searches codebase, requirements, architecture)
3. Generates fixes based on research
4. Applies fixes automatically
5. Re-runs tests
6. Repeats up to 3 times

**Usage**:
```bash
# Test specific ticket
/test-and-fix VLP-123

# Test with custom retry attempts
/test-and-fix VLP-123 --max-attempts 5
```

**Output**:
- Test results (pass/fail by type)
- Success rate
- Fix attempts with analysis
- Failure diagnostics
- Report: `test-reports/TICKET-ID-test-report.md`

**When NOT to use**:
- ❌ When full workflow needed
- ❌ If testing is just one part of larger process

---

## 🎯 Real-World Scenarios

### Scenario 1: New iOS Feature with Jira Ticket

**Goal**: Implement VLP-456: "Add offline search caching"

**Recommended**: `/ios-workflow`

**Why**: Need requirements phase, thorough research, specifications for Jira

**Process**:
```bash
/ios-workflow "VLP-456: Add offline search caching"
```

You'll get:
- Requirements document (Layer 3)
- Research findings
- Implementation plan (Layer 5-6)
- Optional worktree for implementation

**Then**: Implement code manually or use `/multi-agent-dev` for code generation

---

### Scenario 2: Quick Feature with Security & Testing

**Goal**: Implement a small caching utility with full validation

**Recommended**: `/multi-agent-dev`

**Why**: Need code generation + security + testing, but not full requirements phase

**Process**:
```bash
/multi-agent-dev "Add UserPreference caching utility"
```

You'll get:
- Complete implementation (7 stages)
- Security audit
- Automated testing with fixes
- QA validation
- All reports

---

### Scenario 3: Security Review of Existing Code

**Goal**: Check if generated code has security issues

**Recommended**: `/security-scan`

**Why**: Just need security audit, nothing else

**Process**:
```bash
/security-scan VLP-123
```

You'll get:
- Security grade and risk score
- Vulnerability findings
- Remediation guidance
- Security report

---

### Scenario 4: Crashlytics Bug Investigation

**Goal**: Fix VLP-789: "DiscoverViewController crash on viewDidLoad"

**Recommended**: `/ios-workflow`

**Why**: Crashlytics bugs need thorough investigation and research

**Process**:
```bash
/ios-workflow "VLP-789: Fix DiscoverViewController crash"
```

The workflow will:
- Use Firebase MCP for crash analysis
- Research similar crashes in codebase
- Create comprehensive fix plan
- Provide implementation guidance

---

### Scenario 5: CI/CD Automated Code Generation

**Goal**: Automatically generate code for 10 tickets every night

**Recommended**: Python Orchestrator

**Why**: Needs headless execution, no user interaction

**Process**:
```bash
#!/bin/bash
# CI/CD script
for ticket in VLP-{100..110}; do
  python3 orchestrator.py "$ticket: Auto-generated feature"
done
```

Runs unattended, generates all reports

---

### Scenario 6: Test Validation Before PR

**Goal**: Ensure all tests pass before creating PR

**Recommended**: `/test-and-fix`

**Why**: Just need testing, auto-fix failures if possible

**Process**:
```bash
/test-and-fix VLP-123
```

If tests fail, auto-fix will:
- Research codebase for solutions
- Apply fixes automatically
- Retry up to 3 times
- Report results

---

## 🔄 Common Workflow Combinations

### Combination 1: Requirements → Full Development

```bash
# Step 1: Create requirements and research
/ios-workflow "VLP-123: New feature"
# ... complete through implementation plan

# Step 2: Generate code with security & testing
/multi-agent-dev "VLP-123: New feature"
# Uses existing requirements, adds code + security + tests
```

**Result**: Complete documentation + production-ready code

---

### Combination 2: Development → Validation

```bash
# Step 1: Generate code
/multi-agent-dev "Quick caching utility"
# ... generates code

# Step 2: Extra security check
/security-scan

# Step 3: Extra test validation
/test-and-fix
```

**Result**: Triple validation (QA + Security + Testing)

---

### Combination 3: Manual Code → Validation

```bash
# You wrote code manually

# Step 1: Security check
/security-scan VLP-123

# Step 2: Test with auto-fix
/test-and-fix VLP-123
```

**Result**: Validated manually-written code

---

## 📚 Summary Recommendations

### Use `/ios-workflow` when:
- Creating Jira tickets with specifications
- Need requirements-first approach
- Crashlytics bug investigations
- Complex iOS features
- Want worktree isolation

### Use `/multi-agent-dev` when:
- Need complete end-to-end development
- Security audit required
- Automated testing needed
- Production-ready code generation
- Want approval gates

### Use Python Orchestrator when:
- CI/CD automation
- Batch processing
- Headless execution
- No user interaction available

### Use `/security-scan` when:
- Quick security check only
- Before committing code
- Independent validation

### Use `/test-and-fix` when:
- Test validation only
- Auto-fix capabilities needed
- Before creating PR

---

## 🔧 Tips & Best Practices

### 1. Start with Requirements
For complex features, always start with `/ios-workflow` to get proper requirements and research before coding.

### 2. Use Approval Gates for Critical Work
For production features, use interactive commands (`/ios-workflow`, `/multi-agent-dev`) to review each stage.

### 3. Automate Repetitive Tasks
For batch processing or CI/CD, use Python orchestrator.

### 4. Validate Before Committing
Always run `/security-scan` and `/test-and-fix` before committing code.

### 5. Leverage Auto-Fix
Let `/test-and-fix` handle simple test failures automatically - it succeeds ~70% of the time on syntax/import issues.

### 6. Review Security Reports
Even if security scan passes, review the report for best practice recommendations.

### 7. Use Research Capabilities
Both `/ios-workflow` and `/multi-agent-dev` have deep research - use them to learn from existing codebase patterns.

---

*🤖 Choose the right tool for the job and let the agents handle the complexity!*
