# Software Factory Templates

**Purpose**: Generic templates for starting factory runs on ANY project

---

## 📁 Templates Included

1. **new-factory-run.sh** - Setup script for new factory runs
2. **scenario-template.py** - Python test structure for validation scenarios
3. **spec-template.md** - Specification format (the "seed")
4. **report-template.md** - Results documentation

---

## 🚀 Quick Start

### Creating a New Factory Run

```bash
# Usage:
./new-factory-run.sh <project-dir> <issue-id>

# Example:
./new-factory-run.sh ~/Development/my-project feature-123

# Creates:
# ~/Development/my-project/.factory-run/feature-123/
#   ├── SPEC.md (from template)
#   ├── scenarios/test_feature.py (from template)
#   └── workspace/ (for agent work)
```

---

## 📝 Using Templates

### 1. Spec Template

**Copy and fill**:
```bash
cp spec-template.md /path/to/your-issue/SPEC.md
# Then edit and replace {{PLACEHOLDERS}}
```

**Placeholders**:
- `{{ISSUE_NUMBER}}` - Your issue/feature number
- `{{FEATURE_NAME}}` - What you're building
- `{{PROJECT_NAME}}` - Your project
- `{{REQUIREMENTS}}` - Fill in your requirements
- `{{SCENARIOS}}` - Define your validation scenarios

---

### 2. Scenario Template

**Copy and fill**:
```bash
cp scenario-template.py /path/to/your-issue/scenarios/test_feature.py
# Then replace {{PLACEHOLDERS}} and add your tests
```

**Placeholders**:
- `{{PROJECT_DIR}}` - Path to your project (e.g., /Users/you/project)
- `{{FEATURE_NAME}}` - Feature being tested
- `{{SCENARIO_1_NAME}}` - Your first scenario
- `{{SCENARIO_1_TEST}}` - Your test code

---

### 3. Report Template

**After factory run completes**:
```bash
cp report-template.md /path/to/your-issue/FACTORY-RUN-REPORT.md
# Fill in actual results, metrics, outcomes
```

---

## 🎯 Project-Specific Templates

For projects you use frequently (like PlannedEats), create optimized versions:

**Example**: PlannedEats templates
```bash
cd /Users/dbitros/Personal/PlannedEats/project/factory-run/.templates/
# Pre-configured with:
# - PlannedEats directory structure
# - Common helper functions
# - Project-specific paths
# - One-command setup
```

**Benefit**: Even faster setup (5 sec vs 20 min!)

---

## 📚 Template Philosophy

**Generic templates are**:
- ✅ Portable to any project
- ✅ Language-agnostic where possible
- ✅ Framework-neutral
- ⚠️ Require customization per use

**Optimized templates are**:
- ✅ Zero-config (paths baked in)
- ✅ Project-specific helpers
- ✅ Context-aware
- ⚠️ Only work for one project

**Use both**: Generic for new projects, optimized for frequent use!

---

**Version**: 1.0
**Last Updated**: March 2026
