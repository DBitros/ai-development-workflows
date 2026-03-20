---
description: Interactive multi-agent development workflow with security and testing
---

# Multi-Agent Development Workflow

This command executes an interactive 7-agent development workflow with approval gates at each stage.

## Workflow Overview

```
1. Architecture Analysis (Architect Agent)
   → PAUSE: Review architecture compliance
   ↓
2. Requirements Research (Research Agent)
   → PAUSE: Review findings and requirements
   ↓
3. Implementation Planning (Planner Agent)
   → PAUSE: Review implementation plan
   ↓
4. Code Generation (Programmer Agent)
   → PAUSE: Review generated code
   ↓
5. Security Audit (Security Agent)
   → PAUSE: Review security findings
   ↓
6. Testing & Auto-Fix (Test Runner Agent)
   → PAUSE: Review test results and fixes
   ↓
7. Quality Assurance (QA Agent)
   → FINAL: Review QA report and approve deployment
```

## How It Works

When you invoke this command with a ticket or feature description:

1. **Execute a stage** using the appropriate specialized agent
2. **Show you the results** and what was discovered
3. **Ask for your approval** before proceeding to the next stage
4. **Wait for your "yes"** or feedback before continuing
5. **Repeat** until all 7 stages are complete

## Stage Details

### Stage 1: Architecture Analysis 🏛️

**Agent**: Architect Agent
**Purpose**: Validates requirements against TradeMe iOS architecture patterns

**What it checks**:
- Module dependency validation (Tuist constraints)
- Universal API pattern compliance (97% adoption)
- Dependencies framework usage
- Platform service integration patterns

**Output**: Architecture analysis document with compliance validation

**Approval Question**: "Architecture analysis complete. Ready to proceed with requirements research?"

---

### Stage 2: Requirements Research 🔍

**Agent**: Research Agent
**Purpose**: Deep codebase research and Layer 3 requirements creation

**Research capabilities** (uses same agents as `/ios-workflow`):
- `/agents:codebase-pattern-finder` - Find similar implementations
- `/agents:codebase-analyzer` - Analyze existing patterns
- `/agents:codebase-locator` - Locate relevant modules

**What it researches**:
- Existing patterns in 25,976+ Swift files
- Legacy integration constraints
- Existing service discovery
- Design system patterns

**Output**:
- Research findings document
- Layer 3 requirements document

**Approval Question**: "Requirements research complete. Ready to proceed with implementation planning?"

---

### Stage 3: Implementation Planning 📋

**Agent**: Planner Agent
**Purpose**: Creates Layer 5 implementation design with compliance validation

**What it plans**:
- Triple module pattern adherence
- RxSwift-Combine bridge patterns
- Testing strategy integration
- Build system compatibility

**Output**: Detailed implementation plan with step-by-step instructions

**Approval Question**: "Implementation plan complete. Ready to proceed with code generation?"

---

### Stage 4: Code Generation 💻

**Agent**: Programmer Agent
**Purpose**: Generates production-ready Swift code following TradeMe patterns

**What it generates**:
- Swift code following TradeMe conventions
- Proper module placement (Platform/Shared/Feature)
- Dependency injection using Dependencies framework
- Comprehensive test suites (Quick/Nimble)
- Tuist configuration

**Output**: Complete Swift modules with tests and documentation

**Approval Question**: "Code generation complete. Ready to proceed with security audit?"

---

### Stage 5: Security Audit 🔒

**Agent**: Security Engineer Agent
**Purpose**: Comprehensive security vulnerability scanning

**Security checks**:
- **OWASP Mobile Top 10**: All 10 vulnerability categories
- **iOS Security**: Keychain usage, certificate pinning, biometric auth
- **API Security**: Authentication flows, token handling, PII exposure
- **Code Security**: Hardcoded secrets, logging sensitive data, injection vulnerabilities

**Output**: Security report with:
- Risk score (0-100, lower is better)
- Security grade (A+ to F)
- Detailed findings by severity (Critical/High/Medium/Low)
- Remediation recommendations

**Approval Decision**:
- **If Critical Issues Found**: "🚨 CRITICAL security issues detected. Review and fix before proceeding."
- **If High Issues Found**: "⚠️ High-priority security issues found. Review recommended before testing."
- **If Clean**: "✅ Security audit passed. Ready to proceed with testing?"

---

### Stage 6: Testing & Auto-Fix 🧪

**Agent**: Test Runner Agent
**Purpose**: Comprehensive testing with intelligent auto-fix retry loop

**Test types** (based on feature):
- **Unit Tests**: Swift/Quick/Nimble execution
- **iOS UI Tests**: iOS Simulator MCP integration
- **Web Tests**: Playwright MCP for WebView testing
- **API Tests**: Network request validation
- **Integration Tests**: Module compatibility

**Auto-Fix Capabilities**:
When tests fail, the agent automatically:
1. **Analyzes failures** - Categorizes error types
2. **Deep research** - Searches codebase, reviews requirements, checks architecture
3. **Generates fix** - Creates intelligent fixes based on research
4. **Applies fix** - Modifies code automatically
5. **Re-runs tests** - Validates the fix

**Auto-Fix Attempts**: Up to 3 attempts per failure

**Output**: Test report with:
- Test results (passed/failed/skipped)
- Success rate
- Fix attempts with detailed analysis
- Failure diagnostics

**Approval Decision**:
- **If All Tests Pass**: "✅ All tests passed! Ready to proceed with final QA?"
- **If Tests Failed After 3 Attempts**: "❌ Tests still failing. Review failures and provide guidance or type 'skip' to proceed to QA review."
- **If Auto-Fixed Successfully**: "🔄 Auto-fix successful after X attempts. Ready to proceed with QA?"

---

### Stage 7: Quality Assurance ✅

**Agent**: QA Engineer Agent
**Purpose**: Final comprehensive quality validation

**What it validates**:
- Build validation (compilation, syntax)
- Architecture compliance verification
- Code quality analysis (documentation, complexity)
- Performance benchmarking
- Final integration testing

**Output**: QA report with:
- Overall quality score (0-100)
- Pass/Fail/Review status
- Specific issues and recommendations
- Integration readiness assessment

**Final Decision**:
- **Score 80-100**: "✅ PASS - Ready for deployment!"
- **Score 60-79**: "⚠️ REVIEW - Issues need attention before integration"
- **Score 0-59**: "❌ FAIL - Critical issues require resolution"

---

## Usage Examples

### Basic Usage
```bash
# Interactive workflow with approval gates
/multi-agent-dev "VLP-123: Add user profile caching"

# You'll be prompted at each stage:
# → Stage 1 complete. Ready to proceed? (yes/no/feedback)
```

### With Ticket ID
```bash
/multi-agent-dev "VLP-456: Implement offline search caching"
```

### Resume Existing Workflow
```bash
/multi-agent-dev --resume VLP-123
```

### Crashlytics Bug Investigation
```bash
/multi-agent-dev "VLP-789: Fix Firebase crash in DiscoverViewController"
# Auto-detects crash workflow and adjusts accordingly
```

---

## Interactive Controls

At each approval gate, you can respond with:

- **"yes"** or **"y"** - Proceed to next stage
- **"no"** or **"n"** - Stop workflow and save state
- **"skip"** - Skip current stage (with warning)
- **"retry"** - Re-run current stage
- **Provide feedback** - Agent will adjust and retry current stage

---

## Integration with Python Orchestrator

This command is a **wrapper** around the Python orchestrator at:
```
/Users/dbitros/Development/ai-tools/ai-orchestrator/orchestrator.py
```

**How it works**:
1. Claude Code invokes the Python agent for each stage
2. Captures output and presents to user
3. Waits for user approval
4. Passes approval to next stage or stops

**Benefits**:
- ✅ Best of both worlds: Python agent power + Claude interactivity
- ✅ User control at each decision point
- ✅ Can adjust mid-workflow based on findings
- ✅ Uses same MCP tools as `/ios-workflow`

---

## Research Capabilities

The Research Agent (Stage 2) and Test Runner (Stage 6) both use **deep research** when needed:

### Codebase Research Agents
- `/agents:codebase-pattern-finder` - Finds similar Universal API implementations
- `/agents:codebase-analyzer` - Analyzes platform service integration patterns
- `/agents:codebase-locator` - Finds relevant modules following established architecture

### Research Process
1. **Pattern Discovery**: Search 25,976+ Swift files for similar implementations
2. **Requirements Review**: Check Layer 3 requirements and research documents
3. **Architecture Validation**: Consult TradeMe iOS architecture guide
4. **Best Practice Identification**: Find successful patterns to model after

**When research triggers**:
- During Stage 2 (Requirements Research) - Always
- During Stage 6 (Testing) - When tests fail and auto-fix needs guidance

---

## File Output Structure

After completion, you'll have:

```
ai-orchestrator/
├── generated-specs/
│   ├── requirements/VLP-123-requirements.md
│   ├── research/VLP-123-research.md
│   ├── architecture/VLP-123-architecture-analysis.md
│   └── implementation-design/VLP-123-implementation-plan.md
├── generated-code/
│   └── Modules/
│       ├── UserProfileCache/
│       ├── UserProfileCacheApi/
│       └── UserProfileCacheTests/
├── security-reports/
│   └── VLP-123-security-report.md
├── test-reports/
│   └── VLP-123-test-report.md
└── quality-reports/
    └── VLP-123-qa-report.md
```

---

## Comparison: Interactive vs Automated

### Use `/multi-agent-dev` (This Command) When:
- ✅ You want control at each stage
- ✅ Exploring a new feature or complex change
- ✅ Learning how the system works
- ✅ Need to adjust based on findings
- ✅ Working on critical/sensitive features

### Use Python Orchestrator Directly When:
- ✅ Running in CI/CD pipeline
- ✅ Batch processing multiple tickets
- ✅ Automated code generation workflows
- ✅ Headless/unattended execution needed

---

## Execution Instructions

When this command is invoked:

1. **Parse Input**: Extract ticket ID and description
2. **Initialize Workflow**: Create workflow context
3. **Execute Stage 1**: Run Architect Agent
4. **Present Results**: Show architecture analysis to user
5. **Wait for Approval**: Prompt user with "Ready to proceed to requirements research?"
6. **On 'yes'**: Continue to Stage 2
7. **On 'no'**: Save workflow state for later resume
8. **On feedback**: Adjust current stage and retry
9. **Repeat**: For all 7 stages

**Critical**: Each stage MUST wait for user approval before proceeding to the next stage.

---

## Success Criteria

This workflow is successful when:

1. **All Stages Complete**: All 7 agents have executed successfully
2. **Security Passed**: No critical security issues (or addressed)
3. **Tests Passed**: All tests passing (or failures documented)
4. **QA Score ≥ 80**: Quality score meets threshold
5. **User Approval**: User has approved each stage
6. **Documentation Complete**: All reports generated

---

## Example Session

```
User: /multi-agent-dev "VLP-123: Add caching layer for user profiles"

Claude:
🤖 Starting Multi-Agent Development Workflow
📋 Task: VLP-123: Add caching layer for user profiles
🔄 7-stage workflow with approval gates

🏛️ STAGE 1: Architecture Analysis
[Runs Architect Agent...]

✅ Architecture analysis complete!
📄 File: generated-specs/architecture/VLP-123-architecture-analysis.md

Key Findings:
- ✅ Module placement: Feature layer (UserProfileCache)
- ✅ Dependencies: TMAPIClient, SessionManager via Dependencies framework
- ✅ Triple module pattern required
- ⚠️ Performance: Consider cache invalidation strategy

Ready to proceed to requirements research? (yes/no/feedback)

User: yes

Claude:
🔍 STAGE 2: Requirements Research
[Launches research agents...]
[Deep codebase search using pattern-finder, analyzer, locator...]

✅ Requirements research complete!
📄 Files:
- generated-specs/research/VLP-123-research.md
- generated-specs/requirements/VLP-123-requirements.md

Key Discoveries:
- Found similar pattern in PropertyCache module
- Identified 3 cache invalidation strategies in use
- Platform service TMAPIClient provides caching primitives
- Must integrate with SessionManager for user lifecycle

Ready to proceed to implementation planning? (yes/no/feedback)

User: yes

[... continues through all 7 stages ...]
```

---

*🤖 Powered by TradeMe Multi-Agent Development System*
