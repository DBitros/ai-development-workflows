# Claude Commands for Multi-Agent Development

This directory contains Claude Code commands that provide interactive access to the multi-agent development system.

## Available Commands

### 🎯 Main Workflows

#### `/multi-agent-dev`
Complete 7-stage interactive development workflow with approval gates.

```bash
/multi-agent-dev "VLP-123: Add caching layer"
```

**Stages**:
1. 🏛️ Architecture Analysis
2. 🔍 Requirements Research (with deep codebase research)
3. 📋 Implementation Planning
4. 💻 Code Generation
5. 🔒 Security Audit (OWASP Mobile Top 10)
6. 🧪 Testing & Auto-Fix (up to 3 retry attempts)
7. ✅ Quality Assurance

**Features**:
- Interactive approval gates at each stage
- Deep research using specialized agents
- Auto-fix for test failures
- Comprehensive reporting

---

### 🔒 Security

#### `/security-scan`
Quick security audit on generated code.

```bash
/security-scan VLP-123
```

**Scans for**:
- OWASP Mobile Top 10 vulnerabilities
- iOS-specific security issues
- API security problems
- Hardcoded secrets and sensitive data

**Output**: Security report with risk score (0-100) and grade (A-F)

---

### 🧪 Testing

#### `/test-and-fix`
Run tests with intelligent auto-fix retry loop.

```bash
/test-and-fix VLP-123
```

**Features**:
- Comprehensive testing (Unit, iOS UI, Web, API, Integration)
- Auto-fix on failure (up to 3 attempts)
- Deep research to find solutions
- Uses iOS Simulator MCP and Playwright MCP

**Auto-fix success rate**:
- Syntax errors: ~95%
- Missing imports: ~90%
- Simple type errors: ~70%

---

## When to Use What?

See **[WORKFLOW-GUIDE.md](./WORKFLOW-GUIDE.md)** for detailed comparison and decision tree.

### Quick Reference

```
New iOS feature with specs?
  → Use /ios-workflow (in trademe-ai-specs)

Need full development with security & testing?
  → Use /multi-agent-dev

Just need security check?
  → Use /security-scan

Just need test validation?
  → Use /test-and-fix

Need automation/CI-CD?
  → Use Python orchestrator directly
```

---

## Comparison with `/ios-workflow`

| Feature | `/ios-workflow` | `/multi-agent-dev` |
|---------|----------------|-------------------|
| **Purpose** | Requirements-first iOS development | Complete code generation workflow |
| **Best For** | Jira tickets needing specs | Quick features with full validation |
| **Phases** | 6 phases (requirements → plan) | 7 stages (architecture → QA) |
| **Security** | ❌ No | ✅ Yes (Stage 5) |
| **Testing** | ❌ No | ✅ Yes with auto-fix (Stage 6) |
| **Code Generation** | ❌ Manual | ✅ Automatic (Stage 4) |
| **Worktree** | ✅ Yes | ❌ No |
| **Research** | ✅ Phase 2 | ✅ Stage 2 & 6 |

**Recommendation**: Start with `/ios-workflow` for requirements, then use `/multi-agent-dev` for implementation.

---

## Output Structure

**📌 ALL outputs go to the `work/` folder**

After running workflows, you'll find:

```
ai-orchestrator/
└── work/                          # ALL OUTPUTS HERE
    ├── specs/
    │   ├── requirements/TICKET-ID-requirements.md
    │   ├── research/TICKET-ID-research.md
    │   ├── architecture/TICKET-ID-architecture-analysis.md
    │   └── implementation-design/TICKET-ID-implementation-plan.md
    │
    ├── code/
    │   └── Modules/
    │       ├── [ModuleName]/
    │       ├── [ModuleName]Api/
    │       └── [ModuleName]Tests/
    │
    ├── reports/
    │   ├── security/TICKET-ID-security-report.md
    │   ├── testing/TICKET-ID-test-report.md
    │   └── quality/TICKET-ID-qa-report.md
    │
    └── logs/
        └── TICKET-ID-context.json
```

See [../work/README.md](../work/README.md) for complete documentation on what goes where.

---

## Examples

### Example 1: Full Feature Development

```bash
# Interactive workflow with all stages
/multi-agent-dev "VLP-456: Add offline search caching"

# You'll approve each stage:
# → Architecture analysis complete. Proceed? (yes/no)
# → Requirements research complete. Proceed? (yes/no)
# → ...
# → All stages complete! ✅
```

### Example 2: Security Check Only

```bash
# Quick security scan
/security-scan VLP-456

# Output:
# Security Grade: B
# Risk Score: 15/100
# Findings: 1 HIGH, 3 MEDIUM, 2 LOW
```

### Example 3: Test with Auto-Fix

```bash
# Run tests with auto-fix
/test-and-fix VLP-456

# If tests fail:
# Auto-fix attempt 1: Fixed missing import
# Auto-fix attempt 2: Fixed type mismatch
# All tests passed! ✅
```

---

## Python Orchestrator (Automated)

For non-interactive execution:

```bash
# From ai-orchestrator directory
python3 orchestrator.py "VLP-123: Add caching layer"

# Or with options
python3 orchestrator.py --resume VLP-123
python3 orchestrator.py --validate VLP-123
python3 orchestrator.py --list
```

**Use when**:
- CI/CD pipelines
- Batch processing
- Automated workflows
- No user interaction available

---

## Research Capabilities

Both `/multi-agent-dev` and `/test-and-fix` use deep research agents:

### Agents Used
- `/agents:codebase-pattern-finder` - Find similar implementations
- `/agents:codebase-analyzer` - Analyze existing patterns
- `/agents:codebase-locator` - Locate relevant modules

### When Research Triggers
- **Stage 2** (Requirements Research): Always
- **Stage 6** (Testing): When tests fail and auto-fix needs guidance

### What It Searches
- 25,976+ Swift files in TradeMe codebase
- Requirements and specification documents
- Architecture guide and best practices
- Successful pattern implementations

---

## Architecture Compliance

All workflows validate against TradeMe iOS architecture:

✅ **Universal API Architecture** (97% adoption)
✅ **Triple Module Pattern** ({Module}/{ModuleApi}/{ModuleTests})
✅ **Dependencies Framework** integration
✅ **Module Hierarchy** (Platform → Shared → Feature)
✅ **Design System** (Tangram2, Chassis, TMUILibrary)
✅ **Platform Services** (TMAPIClient, TMLogger, SessionManager)

---

## Tips

1. **Start with requirements**: Use `/ios-workflow` first for complex features
2. **Use approval gates**: Interactive commands let you review each stage
3. **Leverage auto-fix**: `/test-and-fix` succeeds ~70% of the time
4. **Check security**: Always run `/security-scan` before committing
5. **Review reports**: Even if QA passes, read recommendations

---

## Getting Help

- **Workflow Guide**: See [WORKFLOW-GUIDE.md](./WORKFLOW-GUIDE.md)
- **Main README**: See [../README.md](../README.md)
- **Agent Documentation**: See agent source files in `../agents/`

---

*🤖 Powered by TradeMe Multi-Agent Development System*
