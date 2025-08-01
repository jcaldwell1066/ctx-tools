#!/bin/bash
# Payment Hotfix Collaboration Template
# Usage: ./payment-hotfix-template.sh JIRA-#### "Description"

JIRA_ID="$1"
DESCRIPTION="$2"
CONTEXT_NAME="payment-hotfix-${JIRA_ID}"

echo "🚀 Creating collaborative payment hotfix context..."

ctx create "$CONTEXT_NAME" --description "Payment hotfix: $DESCRIPTION"
ctx switch "$CONTEXT_NAME"

# Standard hotfix structure
ctx note "JIRA: $JIRA_ID | TYPE: Payment Hotfix"
ctx note "PHASE: Development | STATUS: Starting"
ctx note "STAKEHOLDERS: Dev Team, QA, Payment Ops"
ctx note "TEMPLATE: Payment hotfix collaboration pattern"

# Pre-populate collaboration checkpoints
ctx note "CHECKPOINT_1: Code Review Ready"
ctx note "  ├─ TESTS: Unit tests (target: 95%+ coverage)"
ctx note "  ├─ INTEGRATION: Payment gateway validation"
ctx note "  ├─ DOCS: Technical changes documented"
ctx note "  └─ HANDOFF: Ready for QA review"

ctx note "CHECKPOINT_2: QA Validation Complete"
ctx note "  ├─ FUNCTIONAL: Core payment flows tested"
ctx note "  ├─ REGRESSION: No payment disruption confirmed"
ctx note "  ├─ PERFORMANCE: Transaction time within SLA"
ctx note "  └─ HANDOFF: Ready for staging deployment"

ctx note "CHECKPOINT_3: Production Deployment Ready"
ctx note "  ├─ STAGING: Full integration validation"
ctx note "  ├─ ROLLBACK: Rollback plan documented"
ctx note "  ├─ MONITORING: Alerts configured"
ctx note "  └─ HANDOFF: Ready for production release"

ctx set-state in-progress

echo "✅ Context '$CONTEXT_NAME' created with collaboration structure"
echo "🔄 Switched to context: $CONTEXT_NAME"
echo ""
echo "Next steps:"
echo "  1. Begin development work"
echo "  2. Update checkpoints as you progress"
echo "  3. Use 'ctx note' to document key decisions"
echo "  4. Set state to 'in-review' when ready for handoff"