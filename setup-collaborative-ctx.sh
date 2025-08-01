#!/bin/bash
# Collaborative CTX Setup Script
# Sets up your environment for team-based ctx workflows

echo "🚀 Setting up collaborative CTX environment..."
echo ""

# Check if ctx is installed and working
if ! command -v ctx &> /dev/null; then
    echo "❌ ctx command not found. Please install ctx-tools first."
    exit 1
fi

echo "✅ ctx-tools found: $(ctx --version 2>/dev/null || echo 'installed')"

# Create templates directory if it doesn't exist
mkdir -p ~/projects/active/ctx-tools/templates
echo "✅ Templates directory ready"

# Make all template scripts executable
chmod +x ~/projects/active/ctx-tools/templates/*.sh 2>/dev/null
echo "✅ Template scripts are executable"

# Create team aliases for quick access
echo "Creating team collaboration aliases..."

# Add aliases to shell profile (check which shell)
SHELL_PROFILE=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_PROFILE="$HOME/.bashrc"
fi

if [[ -n "$SHELL_PROFILE" ]]; then
    # Add ctx collaboration aliases
    cat >> "$SHELL_PROFILE" << 'EOF'

# CTX Collaborative Workflow Aliases
alias ctx-hotfix='~/projects/active/ctx-tools/templates/payment-hotfix-template.sh'
alias ctx-handoff='ctx set-state in-review && ctx note "HANDOFF: Ready for next phase"'
alias ctx-block='ctx set-state blocked && ctx note "BLOCKED: $(read -p "Reason: " reason; echo $reason)"'
alias ctx-done='ctx set-state completed && ctx note "COMPLETED: $(date)"'
alias ctx-team='ctx list --format=table | grep -v completed'
alias ctx-mine='ctx list --format=table | grep $(whoami)'

# Enhanced ctx status with team info
ctx-status() {
    echo "=== Current Context ==="
    ctx status
    echo ""
    echo "=== Team Contexts ==="
    ctx list --format=table | head -10
}

# Quick context switching with tab completion
ctx-switch() {
    if [[ $# -eq 0 ]]; then
        echo "Available contexts:"
        ctx list --format=simple
        return
    fi
    ctx switch "$1"
}

EOF

    echo "✅ Added collaboration aliases to $SHELL_PROFILE"
    echo "   Run 'source $SHELL_PROFILE' to activate aliases"
else
    echo "⚠️  Could not determine shell profile. Add aliases manually."
fi

# Create quick start guide
cat > ~/projects/active/ctx-tools/COLLABORATION_QUICK_START.md << 'EOF'
# CTX Collaborative Quick Start Guide

## 🚀 Quick Commands

### Start New Work
```bash
# For payment hotfixes
ctx-hotfix PAYMENT-1234 "Fix CyberSource validation"

# For general development  
ctx create feature-name --description "Description"
ctx set-state in-progress
```

### Team Handoffs
```bash
# Mark ready for review
ctx-handoff

# Block on dependency
ctx-block

# Complete work
ctx-done
```

### Team Visibility
```bash
# See all active team work
ctx-team

# Check current status
ctx-status

# Switch between contexts
ctx-switch context-name
```

## 📋 Templates Available

- `payment-hotfix-template.sh` - Structured payment hotfix workflow
- `handoff-checklist.md` - Team handoff requirements

## 🔄 Workflow States

- 🆕 `pending` - Not started
- 💻 `in-progress` - Active development
- 👀 `in-review` - Ready for handoff/review
- 🚫 `blocked` - Waiting on dependency
- ✅ `completed` - Work finished

## 🤝 Collaboration Best Practices

1. **Use structured notes**: `TYPE: description | METADATA: details`
2. **Clear handoffs**: Include branch, PR, and test instructions
3. **Update states**: Keep team informed of progress
4. **Document decisions**: Add rationale for technical choices
5. **Tag stakeholders**: Use @mentions in notes for visibility

## 🧠 Memory Integration

Your ctx contexts are connected to memory for knowledge retention:
- Technical patterns are captured automatically
- Previous solutions are searchable
- Team knowledge builds over time
EOF

echo "✅ Created quick start guide: ~/projects/active/ctx-tools/COLLABORATION_QUICK_START.md"
echo ""

# Test the setup
echo "🧪 Testing collaborative setup..."

# Test context creation
TEST_CONTEXT="collab-setup-test"
ctx create "$TEST_CONTEXT" --description "Testing collaborative setup" >/dev/null 2>&1

if ctx switch "$TEST_CONTEXT" >/dev/null 2>&1; then
    ctx note "SETUP: Collaborative environment configured successfully"
    ctx set-state completed >/dev/null 2>&1
    echo "✅ Context management working"
else
    echo "❌ Context creation test failed"
fi

echo ""
echo "🎉 Collaborative CTX setup complete!"
echo ""
echo "Next steps:"
echo "  1. source $SHELL_PROFILE  # Activate new aliases"
echo "  2. ctx-status             # Check current setup"
echo "  3. Read: ~/projects/active/ctx-tools/COLLABORATION_QUICK_START.md"
echo "  4. Try: ctx-hotfix DEMO-123 'Test collaborative workflow'"
echo ""
echo "Available templates:"
ls -la ~/projects/active/ctx-tools/templates/