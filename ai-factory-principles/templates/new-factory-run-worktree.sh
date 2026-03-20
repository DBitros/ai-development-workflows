#!/bin/bash
# Software Factory: Create new factory run in worktree-based project
# Designed for work projects using git worktree workflow

set -e

# Usage
if [ $# -lt 1 ]; then
    echo "Usage: $0 <feature-id>"
    echo ""
    echo "This script works with your current worktree/workspace."
    echo "Run /set-workspace FIRST to configure your working directory."
    echo ""
    echo "Example:"
    echo "  /set-workspace                    # Set up your workspace"
    echo "  $0 add-retry-logic                # Create factory run"
    echo ""
    exit 1
fi

FEATURE_ID="$1"

# Use current working directory (should be set by /set-workspace)
PROJECT_DIR="$(pwd)"

# Check if we're in a git worktree
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    WORKTREE_ROOT=$(git rev-parse --show-toplevel)
    echo "✅ Detected git worktree: $WORKTREE_ROOT"
else
    echo "⚠️  Not in a git repository. Continuing anyway..."
    WORKTREE_ROOT="$PROJECT_DIR"
fi

# Look for factory-run directory
# Try common locations:
FACTORY_DIR=""
for candidate in \
    "$WORKTREE_ROOT/.factory-run" \
    "$WORKTREE_ROOT/project/factory-run" \
    "$PROJECT_DIR/.factory-run" \
    "$PROJECT_DIR/factory-run"; do

    if [ -d "$candidate" ]; then
        FACTORY_DIR="$candidate"
        break
    fi
done

# If not found, create in worktree root
if [ -z "$FACTORY_DIR" ]; then
    FACTORY_DIR="$WORKTREE_ROOT/.factory-run"
    mkdir -p "$FACTORY_DIR"
    echo "📁 Created factory directory: $FACTORY_DIR"
fi

RUN_DIR="$FACTORY_DIR/$FEATURE_ID"

echo "🏭 Creating Software Factory run..."
echo "   Feature: $FEATURE_ID"
echo "   Worktree: $WORKTREE_ROOT"
echo "   Factory: $FACTORY_DIR"
echo ""

# Create structure
mkdir -p "$RUN_DIR/scenarios"
mkdir -p "$RUN_DIR/workspace"

# Get template directory (where this script lives)
TEMPLATE_DIR="$(cd "$(dirname "$0")" && pwd)"

# Copy templates
cp "$TEMPLATE_DIR/spec-template.md" "$RUN_DIR/SPEC.md"
cp "$TEMPLATE_DIR/scenario-template.py" "$RUN_DIR/scenarios/test_${FEATURE_ID//-/_}.py"
cp "$TEMPLATE_DIR/report-template.md" "$RUN_DIR/REPORT-TEMPLATE.md"

# Update placeholder paths in scenario template
# Replace {{PROJECT_DIR}} with actual worktree path
sed -i '' "s|{{PROJECT_DIR}}|$WORKTREE_ROOT|g" "$RUN_DIR/scenarios/test_${FEATURE_ID//-/_}.py" 2>/dev/null || true

# Create workspace README
cat > "$RUN_DIR/workspace/README.md" << 'WORKSPACE_EOF'
# Workspace

Agent execution artifacts go here.

## Current Worktree

This factory run is associated with the current git worktree.
Changes will be made to the worktree's files.

## Usage

- Agents use this for temporary files
- Keep execution logs here
- Generated code before moving to source
WORKSPACE_EOF

echo "✅ Factory run structure created:"
echo ""
echo "   $RUN_DIR/"
echo "   ├── SPEC.md (fill in requirements)"
echo "   ├── scenarios/test_${FEATURE_ID//-/_}.py (write tests)"
echo "   ├── workspace/ (agent execution)"
echo "   └── REPORT-TEMPLATE.md (results)"
echo ""
echo "📝 Next steps:"
echo "   1. Edit: $RUN_DIR/SPEC.md"
echo "   2. Write scenarios: $RUN_DIR/scenarios/"
echo "   3. Tell Claude: 'Use factory on $FEATURE_ID'"
echo "   4. Include knowledge base files to read"
echo "   5. Validate and ship!"
echo ""
echo "💡 Knowledge Base:"
echo "   Check /get-workspace for knowledge locations"
echo "   Include knowledge files in your spec for agent to read"
echo ""
echo "🚀 Ready to ship 10x faster!"
