#!/bin/bash
# DevOps/SRE Incident Response Agent Example

echo "=== Incident Response Agent Workflow ==="

# Incident detected
ctx create INC-2025-0147-payment-api
ctx set-state 🔥
ctx note "SEVERITY: P1 | SERVICE: payment-api"
ctx note "IMPACT: 500 errors on /api/v1/process - 15% of requests failing"
ctx note "SYMPTOMS: Spike in 5xx errors, latency increased 10x"

# Initial response
echo -e "\n🔍 Investigation:"
ctx note "DETECTED: CloudWatch alarm 'payment-api-5xx-rate' at 14:32 UTC"
ctx note "METRICS: error_rate = 15.2% (threshold: 1%)"
ctx note "CHECK: Database connections - HEALTHY"
ctx note "CHECK: External payment gateway - DEGRADED (timeouts)"
ctx note "LOG: 'Connection timeout after 30000ms' in payment-gateway-client.log"

# Mitigation
echo -e "\n🛠️ Mitigation Actions:"
ctx note "ACTION: Increased timeout from 30s to 60s - PARTIAL_SUCCESS"
ctx note "ACTION: Enabled circuit breaker with 50% threshold - SUCCESS"
ctx note "WORKAROUND: Routing 50% traffic to backup gateway at 14:45"
ctx note "METRICS: error_rate dropping - now at 2.1%"

# Escalation
ctx set-state 🚨
ctx note "ESCALATION: Paged payment gateway vendor - ticket #PG-8834"
ctx note "CORRELATION: Vendor confirmed regional degradation starting 14:25"

# Resolution
echo -e "\n✅ Resolution:"
ctx note "ACTION: Vendor resolved issue at 15:10"
ctx note "ACTION: Restored normal traffic routing at 15:20"
ctx note "METRICS: error_rate = 0.1% - back to normal"
ctx set-state 📊

# Post-incident
echo -e "\n📊 Post-Incident Review:"
ctx note "RCA: Payment gateway provider had database failover issue"
ctx note "PREVENTION: 1) Implement multi-region gateway failover"
ctx note "PREVENTION: 2) Reduce timeout to fail faster (10s)"
ctx note "PREVENTION: 3) Add pre-emptive health checks"

ctx status
