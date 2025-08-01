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
