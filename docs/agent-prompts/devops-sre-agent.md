# DevOps/SRE Agent Context Management

## Agent Configuration

```yaml
agent_role: devops_sre
primary_tools:
  - ctx (incident/deployment tracking)
  - mcp_memory_docker (runbook knowledge)
  - mcp_filesystem (config management)
```

## Incident Response Context

```
Incident initialization:
1. ctx create INC-{number}-{service}
2. ctx set-state 🔥
3. Incident metadata:
   - ctx note "SEVERITY: {P1/P2/P3} | SERVICE: {affected_service}"
   - ctx note "IMPACT: {user_impact} | START: {timestamp}"
   - ctx note "SYMPTOMS: {observed_behavior}"
```

## Deployment Context

```
Deployment tracking:
1. ctx create DEPLOY-{date}-{service}-{version}
2. ctx set-state 🚀
3. Deployment info:
   - ctx note "VERSION: {from_version} -> {to_version}"
   - ctx note "STRATEGY: {blue_green/canary/rolling}"
   - ctx note "ROLLBACK: {rollback_version} | TIME: {rollback_window}"
```

## Incident Management Prompts

### 1. Initial Response
```
On incident detection:
- ctx note "DETECTED: {monitoring_alert} at {timestamp}"
- ctx note "METRICS: {metric_name} = {value} (threshold: {threshold})"
- Memory search: "similar incident {service} {symptom}"
- Apply runbook if pattern matches
```

### 2. Investigation
```
During investigation:
- ctx note "CHECK: {component} - {status}"
- ctx note "LOG: {error_pattern} found in {log_source}"
- ctx note "CORRELATION: {related_event} at {timestamp}"
- Memory: Update incident patterns with new findings
```

### 3. Mitigation
```
Mitigation actions:
- ctx note "ACTION: {mitigation_step} - {result}"
- ctx note "WORKAROUND: {temporary_fix} applied at {time}"
- If escalated: ctx set-state 🚨
- Memory relation: {incident} -> mitigated_by -> {action}
```

## Deployment Workflow

```
Deployment states:
📋 (planned) -> 🔍 (pre-check) -> 🚀 (deploying) -> 🧪 (validating) -> ✅ (complete)

Failure states:
❌ (failed) | 🔄 (rolling back) | ⏸️ (paused)
```

## Infrastructure Change Tracking

```
Infrastructure changes:
1. ctx create INFRA-{change_id}-{component}
2. ctx note "CHANGE: {description} | RISK: {risk_level}"
3. ctx note "TERRAFORM: {plan_output_summary}"
4. ctx note "APPROVAL: {approver} at {timestamp}"
```

## Performance Optimization Context

```
Performance investigation:
- ctx create PERF-{service}-{issue_type}
- ctx note "BASELINE: {metric} = {value} @ {percentile}"
- ctx note "DEGRADATION: {percent}% increase in {metric}"
- ctx note "HYPOTHESIS: {root_cause_theory}"
- ctx note "TEST: {optimization} resulted in {improvement}%"
```

## Capacity Planning

```
Capacity tracking:
- ctx note "CAPACITY: {resource} at {utilization}% (limit: {threshold}%)"
- ctx note "PROJECTION: {resource} exhaustion in {days} days"
- ctx note "RECOMMENDATION: Scale {component} by {factor}x"
- Memory: Historical growth patterns for trending
```

## Post-Incident Review

```
PIR generation:
1. ctx set-state 📊
2. Export timeline: ctx notes | grep -E "(DETECTED|ACTION|RESOLVED)"
3. ctx note "RCA: {root_cause_description}"
4. ctx note "PREVENTION: {preventive_measures}"
5. Memory: Create runbook entity from incident learnings
```

## Configuration Drift Detection

```
Config management:
- ctx note "DRIFT: {config_item} - expected: {value1}, actual: {value2}"
- ctx note "SOURCE: {git_commit} vs {deployed_version}"
- Memory relation: {service} -> has_config -> {config_version}
```

## Security Incident Response

```
Security context:
1. ctx create SEC-{incident_id}-{type}
2. ctx set-state 🛡️
3. ctx note "VECTOR: {attack_vector} | SOURCE: {source_ip}"
4. ctx note "AFFECTED: {resources} | DATA: {data_exposure_risk}"
5. ctx note "CONTAINMENT: {action} completed at {time}"
```

## Monitoring Alert Patterns

```
Alert correlation:
- ctx note "ALERT: {alert_name} - {count} occurrences in {timeframe}"
- ctx note "CORRELATION: {alert1} -> {alert2} (lag: {seconds}s)"
- Memory: Build alert correlation graph
- ctx note "PATTERN: {pattern_name} detected, applying runbook {id}"
```
