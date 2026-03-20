# Software Factory + Worktree Workflow

**For work projects using git worktree and /set-workspace**

---

## 🚀 Complete Workflow (Copy & Paste)

### **For a FRESH Work Project** (First Time)

```bash
# 1. Navigate to your work project
cd /path/to/your-work-project

# 2. Set workspace (your existing command)
/set-workspace

# 3. Create factory structure
mkdir -p .factory-run/.templates

# 4. Copy worktree-aware templates
cp ~/Development/ai-tools/ai-factory-principles/templates/new-factory-run-worktree.sh .factory-run/.templates/
cp ~/Development/ai-tools/ai-factory-principles/templates/*.md .factory-run/.templates/
cp ~/Development/ai-tools/ai-factory-principles/templates/scenario-template.py .factory-run/.templates/

# 5. Make script executable
chmod +x .factory-run/.templates/new-factory-run-worktree.sh

# 6. Document knowledge base location
cat > .factory-run/KNOWLEDGE-BASE.md << 'EOF'
# Project Knowledge Base

**Check workspace for knowledge locations**:
- Run /get-workspace to see current context
- Look for: project/knowledge/, docs/, README.md
- Read patterns and gotchas before factory runs

**For agents**: Include knowledge file paths in SPEC.md
so agents read project context before implementing.
EOF

# DONE! Factory is set up for this project
```

**Time**: 2 minutes one-time setup

---

### **For Each New Feature** (Every Time)

```bash
# 1. Set workspace (if not already set)
/set-workspace

# 2. Create factory run
.factory-run/.templates/new-factory-run-worktree.sh my-feature-name

# 3. Fill in spec
cd .factory-run/my-feature-name
code SPEC.md
# Add knowledge base files for agent to read

# 4. Write scenarios
code scenarios/test_my_feature_name.py
# Write 3-6 tests defining success

# 5. Run baseline
python3 scenarios/test_my_feature_name.py
# Expect failures (feature not built yet)

# 6. Tell Claude Code (in conversation):
"Use Software Factory on my-feature-name.

Read knowledge base first:
- [list your knowledge files]

Spec: .factory-run/my-feature-name/SPEC.md
Scenarios: .factory-run/my-feature-name/scenarios/test_my_feature_name.py"

# 7. Wait for agent to build (~5-20 min)

# 8. Validate
python3 scenarios/test_my_feature_name.py
# Expect: All pass ✅

# 9. Ship
git add .
git commit -m "feat: implement my-feature-name"
# Continue with your normal workflow (MR, etc.)
```

**Time**: ~30 min total (vs 2-4 hours manual)

---

## 📝 Example: GenericCompany iOS Project

### **First Time Setup** (One-time)

```bash
# 1. Navigate to GenericCompany iOS project
cd ~/generic/ios-app  # or wherever it is

# 2. Set workspace
/set-workspace

# 3. Create factory structure
mkdir -p .factory-run/.templates

# 4. Copy templates
cp ~/Development/ai-tools/ai-factory-principles/templates/new-factory-run-worktree.sh .factory-run/.templates/
cp ~/Development/ai-tools/ai-factory-principles/templates/*.md .factory-run/.templates/
cp ~/Development/ai-tools/ai-factory-principles/templates/scenario-template.py .factory-run/.templates/

chmod +x .factory-run/.templates/new-factory-run-worktree.sh

# 5. Create knowledge pointer
cat > .factory-run/KNOWLEDGE-BASE.md << 'EOF'
# GenericCompany iOS Knowledge Base

**Locations**:
- Axiom/ - iOS patterns and skills
- project/knowledge/ - Project-specific patterns
- docs/ARCHITECTURE.md - System design
- README.md - Project overview

**Key patterns**:
- MVVM architecture
- SwiftUI composition patterns
- Coordinator navigation
- Clean architecture layers

**For factory runs**: Include Axiom skills and knowledge files in spec
EOF

# DONE! Factory ready for GenericCompany iOS
```

---

### **Every Feature** (With Worktree)

```bash
# 1. Set workspace for your ticket/branch
/set-workspace  # Sets up worktree

# 2. Create factory run
.factory-run/.templates/new-factory-run-worktree.sh fix-navigation-bug

# 3. Edit spec with iOS knowledge context
cd .factory-run/fix-navigation-bug
code SPEC.md
```

**In SPEC.md, add**:
```markdown
## Knowledge Context

**Agent: Read these first to understand GenericCompany iOS patterns**:
- `~/generic/ios-app/Axiom/ui-design/swiftui-navigation.md`
- `~/generic/ios-app/project/knowledge/patterns/coordinator-pattern.md`
- `~/generic/ios-app/project/knowledge/gotchas/swiftui-state-bugs.md`
- `~/generic/ios-app/README.md`

**Key patterns to follow**:
- Use Coordinator pattern for navigation
- Follow MVVM architecture
- Match existing SwiftUI composition style
- Check Axiom skills for iOS best practices
```

```bash
# 4. Write scenarios (Swift tests or validation scripts)
code scenarios/test_fix_navigation_bug.py  # or .swift

# 5. Tell Claude Code:
"Use Software Factory on fix-navigation-bug.

Current workspace: [from /get-workspace]

Read knowledge base first:
- Axiom/ui-design/swiftui-navigation.md
- project/knowledge/patterns/coordinator-pattern.md

Spec: .factory-run/fix-navigation-bug/SPEC.md"

# 6. Agent builds following your iOS patterns

# 7. Validate and ship via MR
```

---

## 🔑 Key Integration Points

### **With /set-workspace**

**BEFORE factory run**:
```bash
# 1. Set workspace (your existing workflow)
/set-workspace

# This sets up:
# - Current project location
# - Worktree branch
# - Knowledge base paths
# - Context for work
```

**THEN factory run**:
```bash
# 2. Create factory structure (uses current workspace)
.factory-run/.templates/new-factory-run-worktree.sh <feature>

# The script automatically:
# ✅ Detects current worktree
# ✅ Uses workspace directory
# ✅ Creates structure in right place
```

---

### **With /get-workspace**

**Check context**:
```bash
/get-workspace
```

**Outputs something like**:
```yaml
project: generic-ios
worktree: /path/to/worktrees/VLP-1234
knowledge: /path/to/project/knowledge
main_repo: /path/to/main/repo
```

**Use this info** when telling agent what to read:
```
"Read knowledge base at: [path from /get-workspace]
 Working in worktree: [path from /get-workspace]"
```

---

## 📋 Complete Commands for FRESH Work Project

**Copy and run these in order**:

```bash
# ============================================
# ONE-TIME SETUP (Per Project)
# ============================================

# 1. Set workspace
/set-workspace

# 2. Create factory structure
mkdir -p .factory-run/.templates

# 3. Copy worktree-aware templates
cp ~/Development/ai-tools/ai-factory-principles/templates/new-factory-run-worktree.sh .factory-run/.templates/
cp ~/Development/ai-tools/ai-factory-principles/templates/*.md .factory-run/.templates/
cp ~/Development/ai-tools/ai-factory-principles/templates/scenario-template.py .factory-run/.templates/

# 4. Make executable
chmod +x .factory-run/.templates/new-factory-run-worktree.sh

# 5. Document knowledge
cat > .factory-run/KNOWLEDGE-BASE.md << 'EOF'
# Knowledge Base

Use /get-workspace to find knowledge locations.

Typical paths:
- project/knowledge/patterns/
- project/knowledge/gotchas/
- project/knowledge/decisions/
- Axiom/ (for iOS projects)
- docs/
EOF

# DONE - Factory ready!
```

---

```bash
# ============================================
# PER FEATURE (Every Ticket)
# ============================================

# 1. Set workspace for ticket
/set-workspace  # Select ticket/branch

# 2. Get workspace context
/get-workspace  # Note the paths

# 3. Create factory run
.factory-run/.templates/new-factory-run-worktree.sh my-feature

# 4. Edit spec (include knowledge paths from step 2)
cd .factory-run/my-feature
code SPEC.md

# 5. Write scenarios
code scenarios/test_my_feature.py

# 6. Run baseline
python3 scenarios/test_my_feature.py

# 7. Tell Claude:
"Use Software Factory on my-feature in current workspace.

Workspace: [paste from /get-workspace]

Read knowledge:
- [knowledge files relevant to this feature]

Spec: .factory-run/my-feature/SPEC.md"

# 8. Agent builds

# 9. Validate
python3 scenarios/test_my_feature.py

# 10. Ship (your normal MR workflow)
git add .
git commit -m "feat: my feature"
# etc.
```

---

## 💡 The Key Difference

**PlannedEats workflow**:
- Fixed directory structure
- Single main worktree
- Pre-configured paths

**Work project workflow** (with worktrees):
- Multiple worktrees (one per ticket)
- Workspace changes per ticket
- Paths determined by /set-workspace
- Knowledge base in main repo

**The worktree script handles this automatically!** ✅

---

## 🎯 Summary - What You Need

**For FRESH work project, run these**:

```bash
/set-workspace
mkdir -p .factory-run/.templates
cp ~/Development/ai-tools/ai-factory-principles/templates/new-factory-run-worktree.sh .factory-run/.templates/
cp ~/Development/ai-tools/ai-factory-principles/templates/*.{md,py} .factory-run/.templates/
chmod +x .factory-run/.templates/new-factory-run-worktree.sh
```

**Then for each feature**:

```bash
/set-workspace
.factory-run/.templates/new-factory-run-worktree.sh <feature-name>
# Fill spec and scenarios
# Tell me: "Use factory on <feature-name>"
```

**That's it!** The script adapts to wherever /set-workspace puts you! 🚀

**Want to try it on a work ticket right now?**