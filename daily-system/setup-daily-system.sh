#!/bin/bash
# Setup Daily CTX System - One-time installation and configuration

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${BLUE}[SETUP]${NC} $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
warn() { echo -e "${YELLOW}⚠️${NC} $1"; }

DAILY_SYSTEM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.ctx-daily"

log "Setting up CTX Daily System..."
echo ""

# Check prerequisites
log "Checking prerequisites..."

if ! command -v ctx &> /dev/null; then
    echo "❌ ctx command not found. Please install ctx-tools first:"
    echo "   cd ~/projects/active/ctx-tools"
    echo "   python3 install_ctx.py"
    exit 1
fi

CTX_VERSION=$(ctx --version 2>/dev/null || echo "unknown")
success "ctx-tools found: $CTX_VERSION"

# Create installation directory
mkdir -p "$INSTALL_DIR/bin"
mkdir -p "$INSTALL_DIR/workflows"
mkdir -p "$INSTALL_DIR/templates"

# Copy daily system files
log "Installing daily system files..."

cp "$DAILY_SYSTEM_DIR/ctx-daily.sh" "$INSTALL_DIR/bin/"
cp -r "$DAILY_SYSTEM_DIR/workflows/"* "$INSTALL_DIR/workflows/" 2>/dev/null || true

success "Files installed to $INSTALL_DIR"

# Create symbolic link for easy access
SYMLINK_TARGET="$HOME/.local/bin/ctx-daily"
mkdir -p "$HOME/.local/bin"

if [[ -L "$SYMLINK_TARGET" ]]; then
    rm "$SYMLINK_TARGET"
fi

ln -s "$INSTALL_DIR/bin/ctx-daily.sh" "$SYMLINK_TARGET"
success "Created symlink: ctx-daily command available"

# Add to PATH if needed
SHELL_PROFILE=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_PROFILE="$HOME/.bashrc"
fi

if [[ -n "$SHELL_PROFILE" ]]; then
    # Check if ~/.local/bin is in PATH
    if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_PROFILE"
        warn "Added ~/.local/bin to PATH in $SHELL_PROFILE"
        warn "Run 'source $SHELL_PROFILE' or restart terminal"
    fi
    
    # Add workflow aliases
    cat >> "$SHELL_PROFILE" << 'EOF'

# CTX Daily System Aliases
alias ctx-payment-hotfix='$HOME/.ctx-daily/workflows/payment-hotfix.sh'
alias ctx-incident='$HOME/.ctx-daily/workflows/incident-response.sh'
alias ctx-today='ctx-daily start && ctx-daily status'
alias ctx-done='ctx-daily end'
alias ctx-focus='ctx-daily focus'

# Quick context switching
ctx-quick() {
    if [[ $# -eq 0 ]]; then
        ctx list --format=table | head -10
        return
    fi
    ctx switch "$1" && ctx status
}

EOF
    success "Added aliases to $SHELL_PROFILE"
fi

# Create default configuration
log "Creating default configuration..."

cat > "$HOME/.ctx-daily-config" << 'EOF'
# CTX Daily System Configuration
# Customize these settings for your team and workflow

# Team settings
TEAM_NAME="development-team"
PROJECT_PREFIX="PROJ"

# Work schedule
WORK_HOURS="09:00-17:00"
REVIEW_TIME="17:00"

# Integration URLs (optional)
JIRA_BASE_URL=""  # e.g., "https://yourcompany.atlassian.net"
GITHUB_ORG=""     # e.g., "your-org"

# Notification settings
SLACK_WEBHOOK=""  # For team notifications (future)
EMAIL_ALERTS=""   # For critical incidents (future)
EOF

success "Configuration created at ~/.ctx-daily-config"

# Create quick start guide
cat > "$INSTALL_DIR/QUICK_START.md" << 'EOF'
# CTX Daily System - Quick Start

## 🚀 Getting Started

### Daily Workflow
```bash
# Start your day
ctx-daily start

# Set today's focus
ctx-daily focus "Complete payment API integration"

# Start working on a task
ctx-daily work PAYMENT-5320 "Refund service implementation"

# Track progress throughout the day
ctx-daily progress "Completed database schema"
ctx-daily progress "Added CyberSource integration tests"

# Handle blockers
ctx-daily blocked "Need API keys from DevOps team"
ctx-daily unblock "Received keys and configured"

# Hand off to team
ctx-daily handoff review "PR #1234 ready for code review"

# End your day
ctx-daily end
```

### Specialized Workflows

#### Payment Hotfix
```bash
ctx-payment-hotfix PAYMENT-5320 "Fix CyberSource Level 3 validation"
# Creates structured payment hotfix context with testing framework
```

#### Incident Response
```bash
ctx-incident INC-2025-001 P1 "Payment API returning 500 errors"
# Creates incident response context with investigation checklist
```

### Quick Commands
```bash
ctx-today          # Start day and show status
ctx-done           # End day with summary
ctx-focus "task"   # Set daily focus
ctx-quick          # List contexts
ctx-quick PROJ-123 # Switch to context and show status
```

## 📋 Key Features

- **Daily Tracking**: Automatic daily context creation and management
- **Progress Logging**: Easy progress tracking with timestamps
- **Team Handoffs**: Structured handoff protocols
- **Blocker Management**: Track and resolve blockers
- **Specialized Workflows**: Payment hotfixes, incident response
- **Team Visibility**: See what everyone is working on

## ⚙️ Configuration

Edit `~/.ctx-daily-config` to customize:
- Team name and project prefixes
- Work hours and review times
- JIRA and GitHub integration URLs

## 🤝 Team Collaboration

The system is designed for team use:
- Shared context visibility
- Standardized handoff protocols
- Memory integration for knowledge sharing
- Export/import for context sharing

## 📚 Advanced Usage

See the full documentation in the ctx-tools repository for:
- Memory server integration
- Custom workflow templates
- Agent integration patterns
- Team onboarding guides
EOF

success "Quick start guide created at $INSTALL_DIR/QUICK_START.md"

# Test the installation
log "Testing installation..."

if command -v ctx-daily &> /dev/null; then
    success "ctx-daily command is available"
else
    warn "ctx-daily command not found in PATH"
    echo "Manual command: $INSTALL_DIR/bin/ctx-daily.sh"
fi

# Test ctx integration
if ctx list &> /dev/null; then
    success "ctx integration working"
else
    warn "ctx integration test failed"
fi

echo ""
log "🎉 CTX Daily System setup complete!"
echo ""
echo "Next steps:"
echo "  1. source $SHELL_PROFILE  # Activate new aliases"
echo "  2. ctx-daily start        # Begin daily tracking"
echo "  3. Read: $INSTALL_DIR/QUICK_START.md"
echo ""
echo "Available commands:"
echo "  ctx-daily start           # Begin daily tracking"
echo "  ctx-payment-hotfix        # Payment hotfix workflow"
echo "  ctx-incident              # Incident response workflow"
echo "  ctx-today                 # Quick daily start"
echo ""
echo "Configuration file: ~/.ctx-daily-config"
echo "Documentation: $INSTALL_DIR/QUICK_START.md"