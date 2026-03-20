#!/bin/bash
# Software Factory: Create new factory run structure
# Generic version - works for any project

set -e

# Usage
if [ $# -lt 2 ]; then
    echo "Usage: $0 <project-dir> <issue-id>"
    echo ""
    echo "Example:"
    echo "  $0 ~/Development/my-project feature-auth"
    echo "  $0 /path/to/project issue-42"
    echo ""
    exit 1
fi

PROJECT_DIR="$1"
ISSUE_ID="$2"

# Validate project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Error: Project directory does not exist: $PROJECT_DIR"
    exit 1
fi

# Create factory run structure
FACTORY_DIR="$PROJECT_DIR/.factory-run/$ISSUE_ID"

echo "🏭 Creating Software Factory run structure..."
echo "   Project: $PROJECT_DIR"
echo "   Issue: $ISSUE_ID"
echo ""

# Create directories
mkdir -p "$FACTORY_DIR/scenarios"
mkdir -p "$FACTORY_DIR/workspace"

# Get template directory (where this script lives)
TEMPLATE_DIR="$(cd "$(dirname "$0")" && pwd)"

# Copy templates
cp "$TEMPLATE_DIR/spec-template.md" "$FACTORY_DIR/SPEC.md"
cp "$TEMPLATE_DIR/scenario-template.py" "$FACTORY_DIR/scenarios/test_${ISSUE_ID//-/_}.py"
cp "$TEMPLATE_DIR/report-template.md" "$FACTORY_DIR/REPORT-TEMPLATE.md"

# Create a README in workspace
cat > "$FACTORY_DIR/workspace/README.md" << 'WORKSPACE_EOF'
# Workspace

This directory is for agent execution artifacts.

## Usage

Agents can use this directory for:
- Temporary files during execution
- Generated code before moving to project
- Execution logs and output
- Analysis results

## After Completion

- Move final code to project directories
- Keep logs for reference
- Archive or clean up temporary files
WORKSPACE_EOF

echo "✅ Factory run structure created:"
echo ""
echo "   $FACTORY_DIR/"
echo "   ├── SPEC.md (fill in requirements)"
echo "   ├── scenarios/test_${ISSUE_ID//-/_}.py (write validation tests)"
echo "   ├── workspace/ (for agent execution)"
echo "   └── REPORT-TEMPLATE.md (for results)"
echo ""
echo "📝 Next steps:"
echo "   1. Edit $FACTORY_DIR/SPEC.md"
echo "   2. Write scenarios in $FACTORY_DIR/scenarios/"
echo "   3. Run agents to build"
echo "   4. Validate with: python3 $FACTORY_DIR/scenarios/*.py"
echo "   5. Document results in REPORT"
echo ""
echo "🚀 Ready to ship 10x faster!"
