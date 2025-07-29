#!/bin/bash
# DevOps/SRE Incident Response Agent Example

echo "=== Incident Response Agent Workflow ==="

# Incident detected
ctx create INC-2025-0147-payment-api
ctx set-status 🔥
ctx add-note "SEVERITY: P1 | SERVICE: payment-api"
ctx add-note "IMPACT: 500 errors on /api/v1/process - 15% of requests failing"
ctx add-note "SYMPTOMS: Spike in 5xx errors, latency increased 10x"

# Initial response
echo -e "\n🔍 Investigation:"
ctx add-note "DETECTED: CloudWatch alarm 'payment-api-5xx-rate' at 14:32 UTC"
ctx add-note "METRICS: error_rate = 15.2% (threshold: 1%)"
ctx add-note "CHECK: Database connections - HEALTHY"
ctx add-note "CHECK: External payment gateway - DEGRADED (timeouts)"
ctx add-note "LOG: 'Connection timeout after 30000ms' in payment-gateway-client.log"

# Mitigation
echo -e "\n🛠️ Mitigation Actions:"
ctx add-note "ACTION: Increased timeout from 30s to 60s - PARTIAL_SUCCESS"
ctx add-note "ACTION: Enabled circuit breaker with 50% threshold - SUCCESS"
ctx add-note "WORKAROUND: Routing 50% traffic to backup gateway at 14:45"
ctx add-note "METRICS: error_rate dropping - now at 2.1%"

# Escalation
ctx set-status 🚨
ctx add-note "ESCALATION: Paged payment gateway vendor - ticket #PG-8834"
ctx add-note "CORRELATION: Vendor confirmed regional degradation starting 14:25"

# Resolution
echo -e "\n✅ Resolution:"
ctx add-note "ACTION: Vendor resolved issue at 15:10"
ctx add-note "ACTION: Restored normal traffic routing at 15:20"
ctx add-note "METRICS: error_rate = 0.1% - back to normal"
ctx set-status 📊

# Post-incident
echo -e "\n📊 Post-Incident Review:"
ctx add-note "RCA: Payment gateway provider had database failover issue"
ctx add-note "PREVENTION: 1) Implement multi-region gateway failover"
ctx add-note "PREVENTION: 2) Reduce timeout to fail faster (10s)"
ctx add-note "PREVENTION: 3) Add pre-emptive health checks"

ctx status
