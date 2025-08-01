#!/bin/bash
# Payment Hotfix Workflow - Real daily-use pattern
# Based on your cybersource-testing-matrix expertise

JIRA_ID="$1"
DESCRIPTION="$2"

if [[ -z "$JIRA_ID" ]]; then
    echo "Usage: payment-hotfix.sh PAYMENT-#### \"Description\""
    echo "Example: payment-hotfix.sh PAYMENT-5320 \"Fix CyberSource Level 3 validation\""
    exit 1
fi

CONTEXT_NAME="$JIRA_ID-hotfix"

echo "🚀 Setting up payment hotfix workflow for $JIRA_ID..."

# Create and initialize context
ctx create "$CONTEXT_NAME" --description "Payment Hotfix: $DESCRIPTION"
ctx switch "$CONTEXT_NAME"
ctx set-state in-progress

# Standard payment hotfix structure (based on your proven patterns)
ctx note "JIRA: $JIRA_ID | TYPE: Payment Hotfix"
ctx note "DESCRIPTION: $DESCRIPTION"
ctx note "CREATED: $(date '+%Y-%m-%d %H:%M')"

# Technical setup checklist
ctx note "TECH_SETUP:"
ctx note "  ├─ BRANCH: feature/$JIRA_ID (to be created)"
ctx note "  ├─ ENVIRONMENT: dev-environment"
ctx note "  ├─ DATABASE: Payment service schemas"
ctx note "  └─ DEPENDENCIES: Payment gateway integrations"

# Testing framework (based on your cybersource expertise)
ctx note "TESTING_FRAMEWORK:"
ctx note "  ├─ INTEGRATION_TESTS: CyberSource Level 3 validation"
ctx note "  ├─ AUTH_VALIDATION: Auth ID and Token ID verification"
ctx note "  ├─ CARD_TYPE_VALIDATION: card_type_cd field handling"
ctx note "  ├─ ZERO_DOLLAR_FILTERING: Independent test coverage"
ctx note "  └─ DATABASE_VERIFICATION: Capture state and timestamps"

# Development checkpoints
ctx note "CHECKPOINT_1: Development Complete"
ctx note "  ├─ CODE: Implementation finished"
ctx note "  ├─ TESTS: Unit tests >95% coverage"
ctx note "  ├─ INTEGRATION: Payment gateway validation"
ctx note "  └─ READY: Code review"

ctx note "CHECKPOINT_2: Review Complete"
ctx note "  ├─ PR: Code review approved"
ctx note "  ├─ TESTS: All tests passing"
ctx note "  ├─ DOCS: Technical changes documented"
ctx note "  └─ READY: QA handoff"

ctx note "CHECKPOINT_3: QA Complete"
ctx note "  ├─ FUNCTIONAL: Payment flows tested"
ctx note "  ├─ REGRESSION: No payment disruption"
ctx note "  ├─ PERFORMANCE: Transaction time within SLA"
ctx note "  └─ READY: Deployment"

echo "✅ Payment hotfix context created: $CONTEXT_NAME"
echo ""
echo "Next steps:"
echo "  1. git checkout -b feature/$JIRA_ID"
echo "  2. ctx-daily progress \"Started implementation\""
echo "  3. Use standard ctx commands to track development"
echo "  4. ctx-daily handoff review (when ready for PR review)"
echo ""
echo "Context tracking commands:"
echo "  ctx-daily progress \"Completed database schema\""
echo "  ctx-daily progress \"Added CyberSource integration tests\""
echo "  ctx-daily blocked \"Need API keys from DevOps\""
echo "  ctx-daily handoff review \"PR #1234 ready for review\""