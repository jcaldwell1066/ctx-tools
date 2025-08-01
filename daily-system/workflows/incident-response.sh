#!/bin/bash
# Incident Response Workflow - Production issue handling

INCIDENT_ID="$1"
SEVERITY="$2"
DESCRIPTION="$3"

if [[ -z "$INCIDENT_ID" || -z "$SEVERITY" ]]; then
    echo "Usage: incident-response.sh INC-#### P[1-4] \"Description\""
    echo "Example: incident-response.sh INC-2025-001 P1 \"Payment API returning 500 errors\""
    exit 1
fi

CONTEXT_NAME="$INCIDENT_ID-incident"

echo "🚨 Setting up incident response for $INCIDENT_ID ($SEVERITY)..."

# Create incident context
ctx create "$CONTEXT_NAME" --description "INCIDENT $SEVERITY: $DESCRIPTION"
ctx switch "$CONTEXT_NAME"

# Set initial state based on severity
case "$SEVERITY" in
    "P1")
        ctx set-state blocked  # Critical - all hands
        RESPONSE_TIME="15 minutes"
        ;;
    "P2")
        ctx set-state in-progress  # High priority
        RESPONSE_TIME="1 hour"
        ;;
    "P3"|"P4")
        ctx set-state pending  # Normal priority
        RESPONSE_TIME="4 hours"
        ;;
esac

# Incident metadata
ctx note "INCIDENT: $INCIDENT_ID | SEVERITY: $SEVERITY"
ctx note "DESCRIPTION: $DESCRIPTION"
ctx note "DETECTED: $(date '+%Y-%m-%d %H:%M:%S')"
ctx note "RESPONSE_TIME_TARGET: $RESPONSE_TIME"

# Response checklist
ctx note "RESPONSE_CHECKLIST:"
ctx note "  ├─ STAKEHOLDERS: Notify appropriate teams"
ctx note "  ├─ INVESTIGATION: Identify root cause"
ctx note "  ├─ CONTAINMENT: Stop the bleeding"
ctx note "  ├─ RESOLUTION: Fix the issue"
ctx note "  └─ POST_MORTEM: Document lessons learned"

# Investigation framework
ctx note "INVESTIGATION:"
ctx note "  ├─ SYMPTOMS: [Document what users are experiencing]"
ctx note "  ├─ SCOPE: [How many users/systems affected]"
ctx note "  ├─ TIMELINE: [When did this start]"
ctx note "  └─ INITIAL_HYPOTHESIS: [Best guess at cause]"

# System health checks
ctx note "HEALTH_CHECKS:"
ctx note "  ├─ APPLICATION: [Service status]"
ctx note "  ├─ DATABASE: [Connection and performance]"
ctx note "  ├─ EXTERNAL_APIS: [Payment gateways, etc.]"
ctx note "  ├─ INFRASTRUCTURE: [Servers, load balancers]"
ctx note "  └─ MONITORING: [Alerts and metrics]"

echo "✅ Incident response context created: $CONTEXT_NAME"
echo ""
echo "Immediate actions:"
echo "  1. ctx-daily progress \"Notified on-call team\""
echo "  2. Document investigation findings with ctx notes"
echo "  3. Update stakeholders with ctx-daily progress"
echo ""
echo "Investigation commands:"
echo "  ctx-daily progress \"Database healthy - 100ms response time\""
echo "  ctx-daily progress \"Payment gateway returning 502 errors\""
echo "  ctx-daily progress \"Enabled circuit breaker - service recovering\""
echo ""
echo "Resolution:"
echo "  ctx-daily unblock \"Payment gateway resolved by provider\""
echo "  ctx set-state completed  # When incident fully resolved"