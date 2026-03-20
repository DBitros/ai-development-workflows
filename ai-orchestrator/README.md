# Multi-Agent Development System

> ⚠️ **DEPRECATED** - February 2026
>
> This Python-based orchestrator has been superseded by the pure Claude Code implementation at:
> **`/Users/dbitros/Development/claude-commands//orchestrator/`**
>
> **Why deprecated:**
> - Pure Claude Code commands are more flexible (individual agents can run standalone)
> - No Python dependency required
> - More recently maintained (Feb 2026 vs Dec 2024)
> - Better suited for Claude Code workflows
>
> **This repository is kept for:**
> - Historical reference
> - Potential use with other AIs (Codex, Gemini, Cursor)
> - Archive of the original Python implementation
>
> **For active  iOS development, use the claude-commands version.**

---

# Original Documentation (Historical Reference)

A sophisticated multi-agent workflow system for  iOS development that intelligently handles both **new feature development** and **crash/bug fixes** with specialized workflows that mirror real software development team dynamics.

## 🏗️ Directory Structure

```
ai-orchestrator/
├── agents/                    # Individual agent implementations
│   ├── architect.py          # 🏛️ Architecture analysis and validation
│   ├── researcher.py         # 🔍 Context gathering and requirements creation
│   ├── planner.py            # 📋 Implementation planning with compliance
│   ├── programmer.py         # 💻 Swift code generation
│   ├── security_agent.py     # 🔒 Security auditing and OWASP scanning
│   ├── test_runner.py        # 🧪 Testing with auto-fix retry loop
│   ├── qa_engineer.py        # ✅ Quality assurance and validation
│   └── crash_analyzer.py     # 🚨 Crash analysis and bug fix generation
├── orchestrator.py           # 🎭 Main workflow coordinator
├── config/                   # Agent configurations and settings
│   └── agents.yaml          # Agent roles and workflow configuration
├── tools/                    # Shared utilities and frameworks
│   ├── shared_utils.py      # Common functionality for all agents
│   └── workflow_classifier.py # Smart workflow type detection
├── .claude/                  # Claude Code commands
│   ├── commands/
│   │   ├── multi-agent-dev.md    # Interactive 7-stage workflow
│   │   ├── security-scan.md      # Security-only scanning
│   │   └── test-and-fix.md       # Testing with auto-fix
│   ├── WORKFLOW-GUIDE.md    # When to use what (decision tree)
│   └── README.md            # Commands documentation
├── work/                     # 📁 ALL OUTPUTS GO HERE
│   ├── specs/               # Specification documents
│   │   ├── requirements/    # Layer 3 requirements
│   │   ├── research/        # Research findings
│   │   ├── architecture/    # Architecture analysis
│   │   └── implementation-design/ # Layer 5-6 plans
│   ├── code/                # Generated Swift code
│   │   └── Modules/         # Triple module pattern
│   ├── reports/             # All validation reports
│   │   ├── security/        # Security audit reports
│   │   ├── testing/         # Test execution reports
│   │   ├── quality/         # QA validation reports
│   │   ├── crash-analysis/  # Crash investigation
│   │   └── crash-fix-validation/ # Fix validation
│   ├── logs/                # Workflow state and handoffs
│   └── agent-outputs/       # Agent intermediate outputs
├── examples/                # 📖 Example workflows and usage
└── templates/               # 📄 Code and document templates
```

**📌 IMPORTANT**: All outputs are organized in the `work/` folder. See [work/README.md](work/README.md) for detailed structure and what goes where.

## 🤖 Agent Architecture

This system implements **intelligent workflow routing** with multiple specialized agents:

## 🧠 **Smart Workflow Detection**

The system automatically detects the type of work and routes to the appropriate workflow:

- **🔍 Crash/Bug Fix Detection**: Identifies Firebase crashes, EXC_BREAKPOINT, SIGABRT, etc.
- **⚡ New Feature Detection**: Recognizes feature development requests
- **🔧 Enhancement Detection**: Detects improvement and optimization tasks
- **📊 Confidence Scoring**: Provides reasoning for classification decisions

## 🔀 **Multiple Workflows**

### 🚨 **Crash Fix Workflow** (New!)
- **Trigger**: Firebase crashes, EXC_BREAKPOINT, tableView nil access, etc.
- **Agents**: Crash Analyzer → QA Validation
- **Output**: Targeted fixes for existing code
- **Example**: `"VLP-427: Fix Firebase crash in DiscoverViewController"`

### 🏗️ **Feature Development Workflow**
- **Trigger**: New feature requests, "add", "create", "implement"
- **Agents**: Architect → Researcher → Planner → Programmer → QA
- **Output**: New modules following patterns
- **Example**: `"Add user profile caching feature"`

## 🤖 **Agent Architecture**

### 🚨 **Crash Analyzer Agent** (New!)
- **Role**: Analyzes Firebase crashes and generates targeted fixes for existing  code
- **Specializes in**: EXC_BREAKPOINT analysis, tableView lifecycle issues, view controller crashes
- **Works with**: Real  codebase at `/Users/dbitros/Development/`
- **Output**: Crash analysis reports with specific code fixes

### Traditional 7-Agent Feature Development:

### 1. 🏛️ **Architect Agent**
- **Role**: Analyzes requirements against  iOS architecture patterns
- **Specializes in**: Module dependency validation, Universal API compliance (97% adoption), Dependencies framework usage
- **Output**: Architecture analysis with compliance validation

### 2. 🔍 **Research Agent**
- **Role**: Researches existing patterns in 25,976+ Swift files, creates Layer 3 requirements
- **Specializes in**: Codebase pattern analysis, legacy integration constraints, existing service discovery
- **Output**: Research findings and comprehensive requirements documents

### 3. 📋 **Planner Agent**
- **Role**: Creates implementation plans with compliance validation
- **Specializes in**: Layer 5 implementation design, triple module patterns, reactive programming bridges
- **Output**: Detailed implementation plans with architecture compliance

### 4. 💻 **Programmer Agent**
- **Role**: Generates actual Swift code following  patterns
- **Specializes in**: Swift code generation, module placement, dependency injection, comprehensive testing
- **Output**: Production-ready Swift code with Tuist configuration

### 5. 🔒 **Security Engineer Agent** _(New!)_
- **Role**: Performs comprehensive security audits on generated code
- **Specializes in**: OWASP Mobile Top 10 scanning, iOS security (Keychain, certificate pinning, biometrics), API security (auth, tokens, PII), code security (secrets, injection)
- **Output**: Security audit reports with risk scores, vulnerability findings, and remediation recommendations

### 6. 🧪 **Test Runner Agent** _(New!)_
- **Role**: Runs comprehensive tests with intelligent auto-fix retry loop
- **Specializes in**: Swift unit tests, iOS UI testing (iOS Simulator MCP), web testing (Playwright MCP), deep codebase research on failures, auto-fix with 3-attempt retry
- **Output**: Test reports with pass/fail status, fix attempts, and detailed failure analysis

### 7. ✅ **QA Engineer Agent**
- **Role**: Tests and validates generated code with comprehensive quality assurance
- **Specializes in**: Build validation, unit test analysis, architecture compliance, performance benchmarking
- **Output**: Detailed quality reports with pass/fail status and improvement recommendations

## 🚀 Quick Start

### Basic Usage

**🚨 Crash Fix (Auto-detected):**
```bash
cd /Users/dbitros/Development/-agents
python3 orchestrator.py "VLP-427: Fix Firebase crash in DiscoverViewController.setUpSearchSuggestionsProvider"
```

**🏗️ Feature Development (Auto-detected):**
```bash
python3 orchestrator.py "VLP-XXX: Add user profile caching to reduce API calls"
```

**🔧 Enhancement (Auto-detected):**
```bash
python3 orchestrator.py "VLP-XXX: Improve search performance and add caching"
```

### 🎯 Claude Code Integration

The system includes Claude Code slash commands for easy access:

- **`/multi-agent "Description"`** - Run full workflow with auto-detection
- **`/multi-agent-dry-run "Description"`** - Preview workflow without execution
- **`/multi-agent-status [VLP-XXX]`** - Check workflow progress
- **`/multi-agent-help`** - Comprehensive help and troubleshooting
- **`/multi-agent-stats`** - View workflow analytics and trends

**Example Claude Commands:**
```
/multi-agent "VLP-427: Fix Firebase crash in DiscoverViewController"
/multi-agent-dry-run "Add user authentication module"
/multi-agent-status VLP-427
```

### Interactive Mode
```bash
./orchestrator.py
# Then enter commands interactively
```

### Advanced Commands
```bash
# Resume a previous workflow
./orchestrator.py --resume VLP-XXX

# Validate completed work
./orchestrator.py --validate VLP-XXX

# List all workflow sessions
./orchestrator.py --list
```

## 📋 Workflow Process

The system follows a **7-stage workflow** with quality gates:

1. **🏛️ Architecture Analysis** → Validates  iOS patterns
2. **🔍 Requirements Research** → Creates Layer 3 requirements + research
3. **📋 Implementation Planning** → Designs Layer 5 implementation with compliance
4. **💻 Code Generation** → Generates production Swift code + tests
5. **🔒 Security Audit** → OWASP Mobile Top 10 + iOS security scanning
6. **🧪 Testing & Auto-Fix** → Comprehensive testing with intelligent retry loop (up to 3 attempts)
7. **✅ Quality Assurance** → Final validation and compliance checking

Each stage includes **automatic handoffs** between agents with detailed summaries.

## 📁 Generated Outputs

**📌 ALL outputs are organized in the `work/` folder**

See [work/README.md](work/README.md) for complete documentation on what goes where.

### Specification Documents (`work/specs/`)
- **Requirements** (`work/specs/requirements/`): Layer 3 business and technical requirements
- **Research** (`work/specs/research/`): Codebase analysis and pattern identification
- **Architecture** (`work/specs/architecture/`): Architecture compliance analysis and decisions
- **Implementation Design** (`work/specs/implementation-design/`): Layer 5 detailed implementation plans

### Swift Code (`work/code/`)
- **Triple Module Pattern**: `{Module}/{ModuleApi}/{ModuleTests}`
- **Dependencies Framework**: Complete DI integration
- **Platform Services**: TMAPIClient, TMLogger, SessionManager integration
- **Comprehensive Testing**: Quick/Nimble test suites with mocks
- **Tuist Configuration**: Build system integration
- **Documentation**: README and usage examples
- **Location**: `work/code/Modules/`

### Security Reports (`work/reports/security/`)
- **OWASP Mobile Top 10**: Vulnerability scanning for all 10 categories
- **iOS Security Checks**: Keychain usage, certificate pinning, biometric auth
- **API Security**: Authentication flows, token handling, PII exposure
- **Code Security**: Hardcoded secrets, logging sensitive data, injection vulnerabilities
- **Risk Assessment**: 0-100 risk score with security grade (A-F)
- **Compliance Status**: Production-ready assessment and remediation guidance

### Test Reports (`work/reports/testing/`)
- **Unit Tests**: Swift test execution with Quick/Nimble
- **iOS UI Tests**: Automated testing using iOS Simulator MCP
- **Web Tests**: Playwright MCP integration for web/WebView testing
- **Auto-Fix Attempts**: Deep research and intelligent retry loop (up to 3 attempts)
- **Failure Analysis**: Root cause analysis with codebase pattern research
- **Success Rate**: Overall pass/fail metrics with recommendations

### Quality Assurance (`work/reports/quality/`)
- **Build Validation**: Compilation and syntax checking
- **Test Analysis**: Unit test coverage and pattern validation
- **Architecture Compliance**: Verification against  standards
- **Code Quality**: Documentation coverage, complexity analysis
- **Performance Metrics**: Optimization and bottleneck analysis
- **Overall Score**: 0-100 quality score with pass/fail recommendations

### Crash Reports (`work/reports/crash-analysis/` & `work/reports/crash-fix-validation/`)
- **Crash Analysis**: Root cause investigation for Firebase crashes
- **Fix Proposals**: Targeted fixes for existing  code
- **Fix Validation**: QA validation of crash fixes

## 🎯 Integration with 

###  AI Specs Integration
- **Reads from**: `/Users/dbitros/Development/-ai-specs/` for architecture context
- **Follows**: 7-layer specification methodology
- **Validates against**: Comprehensive iOS architecture guide (95-98% accuracy)

###  iOS Project Ready
- **Generated code** can be copied to `/Users/dbitros/Development//`
- **Follows**: Triple module pattern with Tuist 4.55.9 compatibility
- **Integrates**: Platform services via established API patterns
- **Respects**: Module hierarchy constraints (Platform → Shared → Feature)

## 🧪 Quality Assurance Features

The QA Engineer Agent provides **comprehensive validation**:

### Build Validation ✅
- Swift syntax and compilation checking
- Tuist configuration validation
- Dependency resolution verification

### Testing Analysis ✅
- Unit test structure and coverage
- Quick/Nimble integration validation
- Mock implementation verification

### Architecture Compliance ✅
- Triple module pattern verification
- Dependencies framework integration
- Platform service access validation
- Module hierarchy constraint checking

### Code Quality ✅
- Documentation coverage analysis
- Code complexity and maintainability
- Swift naming convention compliance
- Performance optimization analysis

### Scoring System 📊
- **0-59**: ❌ **FAIL** - Critical issues require resolution
- **60-79**: ⚠️ **REVIEW** - Issues need attention before integration
- **80-100**: ✅ **PASS** - Ready for integration and deployment

## 🔒 Security Features

The Security Engineer Agent provides **comprehensive security auditing**:

### OWASP Mobile Top 10 🛡️
- M1: Improper Platform Usage
- M2: Insecure Data Storage (UserDefaults vs Keychain)
- M3: Insecure Communication (HTTP vs HTTPS, certificate pinning)
- M4: Insecure Authentication (token handling, session management)
- M5: Insufficient Cryptography (weak algorithms, hardcoded keys)
- M6: Insecure Authorization
- M7: Client Code Quality (injection vulnerabilities)
- M8: Code Tampering (jailbreak detection)
- M9: Reverse Engineering
- M10: Extraneous Functionality (debug code in production)

### iOS-Specific Security 📱
- Keychain usage validation
- Certificate pinning implementation
- Biometric authentication (Face ID/Touch ID)
- Secure Enclave integration
- WebView JavaScript execution safety

### API Security 🌐
- Authentication header validation
- Token handling and storage
- PII exposure in logs
- SQL injection prevention
- Hardcoded API URL detection

### Code Security 💻
- Hardcoded secrets detection (API keys, tokens, passwords)
- Sensitive data in comments
- Debug code in production builds
- Logging sensitive information

### Risk Assessment 📊
- **Risk Score**: 0-100 (lower is better)
- **Security Grade**: A+ to F
- **Compliance Status**: Production-ready assessment
- **Critical Issues**: Immediate blockers highlighted

## 🧪 Testing & Auto-Fix Features

The Test Runner Agent provides **intelligent testing with deep research**:

### Comprehensive Testing 🔍
- **Unit Tests**: Swift/Quick/Nimble test execution
- **iOS UI Tests**: iOS Simulator MCP integration for automated UI testing
- **Web Tests**: Playwright MCP for WebView and web interface testing
- **API Tests**: Network request validation and error handling
- **Integration Tests**: Module integration and platform service compatibility

### Auto-Fix Retry Loop 🔄
When tests fail, the system automatically:
1. **Analyzes failures** - Categorizes errors (syntax, imports, type errors, etc.)
2. **Deep research** - Searches codebase for patterns, reviews requirements, checks architecture guidance
3. **Generates fix** - Creates intelligent fixes based on research findings
4. **Applies fix** - Modifies code automatically
5. **Re-runs tests** - Validates the fix

**Auto-Fix Attempts**: Up to 3 attempts with increasing sophistication
**Success Rate**: Fixes 70%+ of simple issues (syntax, imports, missing components)

### Deep Research on Failure 📚
When tests fail, the system researches:
- **Codebase Patterns**: Searches 25,976+ Swift files for similar implementations
- **Requirements Context**: Reviews specification documents for guidance
- **Architecture Guidance**: Consults  iOS architecture best practices
- **Similar Implementations**: Finds successful patterns to model after

### Test Reporting 📊
- **Success Rate**: Pass/fail metrics
- **Fix Attempts**: Detailed log of each auto-fix attempt
- **Failure Analysis**: Root cause identification
- **Recommendations**: Next steps for manual intervention if needed

## 📖 Example Usage

### 🚨 Crash Fix Analysis (New!)
```bash
python3 orchestrator.py "VLP-427: Fix Firebase crash in DiscoverViewController.setUpSearchSuggestionsProvider - EXC_BREAKPOINT when accessing tableView before viewDidLoad"
```

**Crash Fix Output:**
```
work/reports/
├── crash-analysis/
│   └── VLP-427-crash-analysis.md    # Root cause analysis and proposed fixes
└── crash-fix-validation/
    └── VLP-427-crash-fix-validation.md    # QA validation of the fix
```

### 🏗️ Create a User Caching Service (Feature Development)
```bash
python3 orchestrator.py "VLP-123: Add user profile caching to reduce API calls"
```

**Expected Output Structure:**
```
work/
├── specs/
│   ├── requirements/VLP-123-requirements.md
│   ├── research/VLP-123-research.md
│   ├── architecture/VLP-123-architecture-analysis.md
│   └── implementation-design/VLP-123-implementation-plan.md
├── code/
│   └── Modules/
│       ├── UserProfileCache/
│       │   ├── Sources/UserProfileCache*.swift
│       │   ├── Project.swift
│       │   └── Scripts/build.sh
│       ├── UserProfileCacheApi/
│       │   ├── Sources/UserProfileCache*.swift
│       │   └── Project.swift
│       └── UserProfileCacheTests/
│           ├── Tests/UserProfileCacheTests.swift
│           └── Project.swift
└── reports/
    ├── security/VLP-123-security-report.md
    ├── testing/VLP-123-test-report.md
    └── quality/VLP-123-qa-report.md
```

## ⚡ Performance & Features

### 🚀 **Core Capabilities**
- **Smart Workflow Routing**: Automatic detection of crash fixes vs feature development
- **Real  Integration**: Works directly with `/Users/dbitros/Development/` codebase
- **Parallel Agent Execution**: Agents work concurrently where possible
- **Resume Capability**: Workflows can be resumed from any stage
- **Quality Gates**: Automatic validation at each stage

### 🔍 **Crash Analysis Features**
- **Firebase Crash Detection**: Parses EXC_BREAKPOINT, SIGABRT, tableView nil access
- **Root Cause Analysis**: Identifies specific code issues and lifecycle problems
- **Targeted Fixes**: Generates patches for existing code instead of new modules
- **Real Codebase Analysis**: Analyzes actual  Swift files

### 📊 **Quality & Reliability**
- **Comprehensive Logging**: Full audit trail of agent decisions
- **Error Recovery**: Graceful handling of failures with state preservation
- **Architecture Compliance**: 97% alignment with  iOS patterns
- **Multi-Workflow Support**: Handles crashes, features, and enhancements

## 🔧 Configuration

### Agent Configuration (`config/agents.yaml`)
- **Agent roles and specializations**
- **Workflow stages and checkpoints**
- **Output directory structure**
- **Quality gate requirements**

### Customization
- **Agent prompts and behavior**
- **Quality thresholds and metrics**
- **Output formats and templates**
- **Integration with existing tools**

## 📚 Architecture Compliance

The system follows ** iOS architecture patterns**:

- ✅ **Universal API Architecture** (97% adoption)
- ✅ **Dependencies Framework** (187+ usages)
- ✅ **Triple Module Pattern** (Platform/Shared/Feature hierarchy)
- ✅ **Platform Service Integration** (TMAPIClient, TMLogger, SessionManager)
- ✅ **Reactive Programming Bridges** (RxSwift ↔ Combine)
- ✅ **Design System Integration** (Tangram2, TangramUI, TMUILibrary)
- ✅ **Testing Strategy** (Quick/Nimble + universal placeholder patterns)

## 🧪 Testing the System

### **Step-by-Step Testing Guide**

#### 1. **Basic Test Run**
Start with a simple test to verify the system works:
```bash
cd /Users/dbitros/Development/-agents
python orchestrator.py "TEST-001: Add user preference caching"
```

#### 2. **Interactive Mode**
Try the interactive mode for more control:
```bash
python orchestrator.py
# Then type: TEST-002: Create notification settings manager
```

#### 3. **Real  Feature**
Once basic tests work, try actual features:
```bash
python orchestrator.py "VLP-456: Add offline search caching to improve app performance"
```

### **Expected Workflow Output**
You'll see progress through all 5 stages:
```
🤖 ===  Multi-Agent Development System ===
🎯 Task: TEST-001: Add user preference caching
============================================================

🚀 Starting 🏛️  Architecture Analysis...
✅ Architecture analysis complete
🚀 Starting 🔍 Requirements Research...
✅ Research and requirements complete
🚀 Starting 📋 Implementation Planning...
✅ Implementation design complete
🚀 Starting 💻 Code Generation...
✅ Code generation complete: 23 files created
🚀 Starting 🧪 Quality Assurance...
✅ QA testing complete: Overall score 87/100
🎉 Code ready for integration!

📊 Workflow Summary for TEST-001
✅ Completed Stages: 5/5
📂 Generated Artifacts: 6 documents + 23 code files
🎯 Next Steps: Review QA report and integrate code
```

### **Advanced Commands**
```bash
# Resume interrupted workflow
python orchestrator.py --resume TEST-001

# Validate completed work
python orchestrator.py --validate TEST-001

# List all workflow sessions
python orchestrator.py --list

# Interactive mode
python orchestrator.py
```

### **Progressive Testing Strategy**
Recommended testing order:

1. **🧪 Simple Test**: `"TEST-001: Add user preference storage"`
2. **📱 UI Test**: `"TEST-002: Create settings screen component"`
3. **🌐 API Test**: `"TEST-003: Add API response caching layer"`
4. **🎯 Real Feature**: `"VLP-XXX: Your actual  ticket"`

### **Quality Score Expectations**
- **80-100**: ✅ **Excellent** - Ready for production
- **60-79**: ⚠️ **Good** - Minor improvements needed
- **40-59**: 🔧 **Fair** - Some issues to address
- **<40**: ❌ **Poor** - Significant problems

### **Generated File Structure After Test**
```
ai-orchestrator/
└── work/
    ├── specs/
    │   ├── requirements/TEST-001-requirements.md
    │   ├── research/TEST-001-research.md
    │   ├── architecture/TEST-001-architecture-analysis.md
    │   └── implementation-design/TEST-001-implementation-plan.md
    ├── code/
    │   └── Modules/
    │       ├── UserPreferenceCache/
    │       ├── UserPreferenceCacheApi/
    │       └── UserPreferenceCacheTests/
    ├── reports/
    │   ├── security/TEST-001-security-report.md
    │   ├── testing/TEST-001-test-report.md
    │   └── quality/TEST-001-qa-report.md
    └── logs/
        ├── TEST-001-context.json
        └── TEST-001-handoff-*.md
```

### **Checking Generated Files**
```bash
# Review all outputs for a ticket
ls -R work/ | grep TEST-001

# Review generated artifacts
ls -la work/specs/
ls -la work/code/Modules/
ls -la work/reports/

# Read reports
cat work/reports/security/TEST-001-security-report.md
cat work/reports/testing/TEST-001-test-report.md
cat work/reports/quality/TEST-001-qa-report.md

# Check specific Swift files
cat work/code/Modules/UserPreferenceCache/Sources/*.swift
```

## 🚨 **Troubleshooting**

### **Common Issues & Solutions**

#### Python Dependencies
```bash
pip install pyyaml
```

#### File Permissions
```bash
chmod +x orchestrator.py
```

#### Missing Directories
```bash
# System will auto-create, but verify base structure:
ls -la /Users/dbitros/Development/-agents/
```

#### Architecture Context Missing
```bash
# Verify -ai-specs is accessible:
ls -la /Users/dbitros/Development/-ai-specs/
```

### **Error Recovery**
- **Workflow interrupted**: Use `--resume TICKET-ID` to continue
- **Agent fails**: Check logs in `logs/` directory for details
- **Quality issues**: Review QA report for specific improvement suggestions
- **Build problems**: Check generated build scripts in `generated-code/`

## 🚀 Next Steps After Generation

1. **Review QA Report** - Check quality score and address issues
2. **Build Validation** - Run generated build scripts
3. **Copy to  Project** - Integrate with main iOS codebase
4. **Manual Testing** - Validate integration and functionality
5. **Performance Testing** - Benchmark against requirements
6. **Deploy** - Release to appropriate environment

---

*🤖 Powered by  Multi-Agent Development System*
*Bridging AI assistance with  iOS architecture excellence*
