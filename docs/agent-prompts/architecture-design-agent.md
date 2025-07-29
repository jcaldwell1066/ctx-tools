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
2. ctx set-state 🏗️
3. Design metadata:
   - ctx note "SCOPE: {system/component/integration}"
   - ctx note "REQUIREMENTS: {functional} | {non-functional}"
   - ctx note "CONSTRAINTS: {technical} | {business} | {regulatory}"
```

## Architecture Decision Records (ADR)

```
ADR tracking:
1. ctx note "ADR-{number}: {title}"
2. ctx note "STATUS: {proposed/accepted/deprecated/superseded}"
3. ctx note "CONTEXT: {problem_statement}"
4. ctx note "DECISION: {chosen_solution}"
5. ctx note "CONSEQUENCES: {positive} | {negative} | {risks}"
6. Memory relation: {component} -> implements -> {pattern}
```

## Design Pattern Application

```
Pattern selection:
1. Memory search: "{problem_type} pattern"
2. ctx note "PATTERN: {pattern_name} | USE_CASE: {applicability}"
3. ctx note "IMPLEMENTATION: {language/framework} specific notes"
4. ctx note "TRADE-OFFS: {benefits} vs {drawbacks}"
```

## System Component Design

```
Component specification:
- ctx note "COMPONENT: {name} | TYPE: {service/library/module}"
- ctx note "INTERFACE: {API_spec} | PROTOCOL: {REST/gRPC/GraphQL}"
- ctx note "DEPENDENCIES: {internal}: [{list}] | {external}: [{list}]"
- ctx note "DATA: {storage_type} | SCHEMA: {version}"
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
1. ctx note "INTEGRATION: {system_A} <-> {system_B}"
2. ctx note "PROTOCOL: {sync/async} | FORMAT: {JSON/XML/protobuf}"
3. ctx note "SLA: {latency}ms p99 | {throughput} rps"
4. ctx note "FAILURE: {retry_strategy} | CIRCUIT_BREAKER: {config}"
```

## Performance Architecture

```
Performance considerations:
- ctx note "LOAD: {expected_rps} | PEAK: {max_rps}"
- ctx note "LATENCY: {target}ms p50/p95/p99"
- ctx note "SCALING: {horizontal/vertical} | TRIGGER: {metric}@{threshold}"
- ctx note "CACHE: {layer} - {strategy} - TTL: {duration}"
```

## Security Architecture

```
Security design:
1. ctx note "AUTHZ: {RBAC/ABAC/custom} | PROVIDER: {implementation}"
2. ctx note "ENCRYPTION: {at_rest}: {method} | {in_transit}: {TLS_version}"
3. ctx note "SECRETS: {management_system} | ROTATION: {frequency}"
4. ctx note "AUDIT: {events_logged} | RETENTION: {duration}"
```

## Data Architecture

```
Data design decisions:
- ctx note "STORAGE: {type} - {technology} | VOLUME: {size_estimate}"
- ctx note "CONSISTENCY: {strong/eventual} | CAP: {choice}"
- ctx note "PARTITION: {strategy} | SHARD_KEY: {field}"
- ctx note "BACKUP: {frequency} | RPO: {time} | RTO: {time}"
```

## Technology Stack Selection

```
Stack decisions:
1. ctx note "LANG: {language} v{version} | FRAMEWORK: {name} v{version}"
2. ctx note "INFRA: {cloud/on-prem} | ORCHESTRATION: {k8s/ecs/custom}"
3. ctx note "MONITORING: {metrics}: {tool} | {logs}: {tool} | {traces}: {tool}"
4. Memory: Link technology choices to past success patterns
```

## Cost Architecture

```
Cost modeling:
- ctx note "COMPUTE: ${estimate}/month | BASIS: {instance_types}"
- ctx note "STORAGE: ${estimate}/month | GROWTH: {rate}"
- ctx note "TRANSFER: ${estimate}/month | EGRESS: {GB_estimate}"
- ctx note "OPTIMIZATION: {reserved/spot/savings_plan}"
```

## Migration Architecture

```
Migration planning:
1. ctx create MIGRATE-{from}-to-{to}
2. ctx note "STRATEGY: {big_bang/parallel/gradual}"
3. ctx note "PHASE_{n}: {description} | DURATION: {estimate}"
4. ctx note "ROLLBACK: {point} | PROCEDURE: {steps}"
5. ctx note "VALIDATION: {method} | SUCCESS_CRITERIA: {metrics}"
```

## Architecture Review Checklist

```
Review preparation:
1. ctx note "REVIEW: Scalability - {findings}"
2. ctx note "REVIEW: Security - {findings}"
3. ctx note "REVIEW: Reliability - {findings}"
4. ctx note "REVIEW: Maintainability - {findings}"
5. ctx note "REVIEW: Cost - {findings}"
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
