# Architecture Design Agent Context Management

## Agent Configuration

```yaml
agent_role: solution_architect
primary_tools:
  - ctx (design decision tracking)
  - mcp_memory_docker (pattern library)
  - create_diagram (architecture visualization)
```

## Design Context Initialization

```
New architecture design:
1. ctx create ARCH-{project}-{component}
2. ctx set-status 🏗️
3. Design metadata:
   - ctx add-note "SCOPE: {system/component/integration}"
   - ctx add-note "REQUIREMENTS: {functional} | {non-functional}"
   - ctx add-note "CONSTRAINTS: {technical} | {business} | {regulatory}"
```

## Architecture Decision Records (ADR)

```
ADR tracking:
1. ctx add-note "ADR-{number}: {title}"
2. ctx add-note "STATUS: {proposed/accepted/deprecated/superseded}"
3. ctx add-note "CONTEXT: {problem_statement}"
4. ctx add-note "DECISION: {chosen_solution}"
5. ctx add-note "CONSEQUENCES: {positive} | {negative} | {risks}"
6. Memory relation: {component} -> implements -> {pattern}
```

## Design Pattern Application

```
Pattern selection:
1. Memory search: "{problem_type} pattern"
2. ctx add-note "PATTERN: {pattern_name} | USE_CASE: {applicability}"
3. ctx add-note "IMPLEMENTATION: {language/framework} specific notes"
4. ctx add-note "TRADE-OFFS: {benefits} vs {drawbacks}"
```

## System Component Design

```
Component specification:
- ctx add-note "COMPONENT: {name} | TYPE: {service/library/module}"
- ctx add-note "INTERFACE: {API_spec} | PROTOCOL: {REST/gRPC/GraphQL}"
- ctx add-note "DEPENDENCIES: {internal}: [{list}] | {external}: [{list}]"
- ctx add-note "DATA: {storage_type} | SCHEMA: {version}"
```

## Architecture States

```
Design phases:
🤔 (ideation) -> 🏗️ (designing) -> 📐 (reviewing) -> 🔍 (validating) -> ✅ (approved)

Risk states:
⚠️ (risk identified) | 🚨 (high risk) | ✓ (risk mitigated)
```

## Integration Design

```
Integration planning:
1. ctx add-note "INTEGRATION: {system_A} <-> {system_B}"
2. ctx add-note "PROTOCOL: {sync/async} | FORMAT: {JSON/XML/protobuf}"
3. ctx add-note "SLA: {latency}ms p99 | {throughput} rps"
4. ctx add-note "FAILURE: {retry_strategy} | CIRCUIT_BREAKER: {config}"
```

## Performance Architecture

```
Performance considerations:
- ctx add-note "LOAD: {expected_rps} | PEAK: {max_rps}"
- ctx add-note "LATENCY: {target}ms p50/p95/p99"
- ctx add-note "SCALING: {horizontal/vertical} | TRIGGER: {metric}@{threshold}"
- ctx add-note "CACHE: {layer} - {strategy} - TTL: {duration}"
```

## Security Architecture

```
Security design:
1. ctx add-note "AUTHZ: {RBAC/ABAC/custom} | PROVIDER: {implementation}"
2. ctx add-note "ENCRYPTION: {at_rest}: {method} | {in_transit}: {TLS_version}"
3. ctx add-note "SECRETS: {management_system} | ROTATION: {frequency}"
4. ctx add-note "AUDIT: {events_logged} | RETENTION: {duration}"
```

## Data Architecture

```
Data design decisions:
- ctx add-note "STORAGE: {type} - {technology} | VOLUME: {size_estimate}"
- ctx add-note "CONSISTENCY: {strong/eventual} | CAP: {choice}"
- ctx add-note "PARTITION: {strategy} | SHARD_KEY: {field}"
- ctx add-note "BACKUP: {frequency} | RPO: {time} | RTO: {time}"
```

## Technology Stack Selection

```
Stack decisions:
1. ctx add-note "LANG: {language} v{version} | FRAMEWORK: {name} v{version}"
2. ctx add-note "INFRA: {cloud/on-prem} | ORCHESTRATION: {k8s/ecs/custom}"
3. ctx add-note "MONITORING: {metrics}: {tool} | {logs}: {tool} | {traces}: {tool}"
4. Memory: Link technology choices to past success patterns
```

## Cost Architecture

```
Cost modeling:
- ctx add-note "COMPUTE: ${estimate}/month | BASIS: {instance_types}"
- ctx add-note "STORAGE: ${estimate}/month | GROWTH: {rate}"
- ctx add-note "TRANSFER: ${estimate}/month | EGRESS: {GB_estimate}"
- ctx add-note "OPTIMIZATION: {reserved/spot/savings_plan}"
```

## Migration Architecture

```
Migration planning:
1. ctx create MIGRATE-{from}-to-{to}
2. ctx add-note "STRATEGY: {big_bang/parallel/gradual}"
3. ctx add-note "PHASE_{n}: {description} | DURATION: {estimate}"
4. ctx add-note "ROLLBACK: {point} | PROCEDURE: {steps}"
5. ctx add-note "VALIDATION: {method} | SUCCESS_CRITERIA: {metrics}"
```

## Architecture Review Checklist

```
Review preparation:
1. ctx add-note "REVIEW: Scalability - {findings}"
2. ctx add-note "REVIEW: Security - {findings}"
3. ctx add-note "REVIEW: Reliability - {findings}"
4. ctx add-note "REVIEW: Maintainability - {findings}"
5. ctx add-note "REVIEW: Cost - {findings}"
6. Generate diagram: Architecture overview with components and flows
```

## Pattern Library Integration

```
Building pattern knowledge:
1. Memory entity: {pattern_name} (type: architecture_pattern)
2. Memory observations:
   - Implementation details
   - Success metrics
   - Failure scenarios
3. Memory relations:
   - {pattern} -> solves -> {problem_type}
   - {pattern} -> requires -> {prerequisite}
   - {pattern} -> conflicts_with -> {other_pattern}
```
