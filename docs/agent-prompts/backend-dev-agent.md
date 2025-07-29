# Backend Developer Agent Context Management

## Agent Configuration

```yaml
agent_role: backend_developer
primary_tools:
  - ctx (context management)
  - mcp_memory_docker (persistent memory)
  - mcp_filesystem (code navigation)
```

## Context Initialization Prompt

```
Initialize development context for service implementation:
1. Create context: ctx create {JIRA_ID}-{service_name}
2. Set status: ctx set-state 💻
3. Add technical metadata:
   - ctx note "SERVICE: {service_name} | ENDPOINT: {endpoint_path}"
   - ctx note "BRANCH: feature/{JIRA_ID} | TARGET: {target_env}"
   - ctx note "DEPENDENCIES: {list_dependencies}"
4. Create memory entities:
   - Entity: {service_name} (type: service)
   - Relations: implements -> {endpoint_path}, uses -> {dependencies}
```

## Development Workflow Prompts

### 1. Service Implementation Start
```
When implementing new service endpoint:
- Switch context: ctx switch {JIRA_ID}-{service_name}
- Update status: ctx set-state 🔨
- Track progress: ctx note "IMPL: {component} - {status}"
- Memory update: Add observation to service entity with implementation decisions
```

### 2. Test Development
```
For unit test creation:
- ctx note "TEST: {test_file} - {coverage}% - {test_count} tests"
- ctx note "MOCK: {external_service} - {mock_strategy}"
- Memory relation: {test_class} -> tests -> {service_method}
```

### 3. Integration Point Documentation
```
When integrating with external services:
- ctx note "INTEGRATION: {service} - {endpoint} - {auth_method}"
- ctx note "CONFIG: {env_var} = {value_pattern}"
- Memory entity: {external_service} (type: integration)
- Memory relation: {service_name} -> depends_on -> {external_service}
```

## State Transitions

```
Development States:
🆕 -> 💻 -> 🔨 -> 🧪 -> 👀 -> 🚀 -> ✅

Blocked States:
🚫 (blocked) | ⏸️ (on-hold) | 🐛 (debugging)
```

## Code Review Preparation

```
Before submitting PR:
1. ctx set-state 👀
2. ctx note "PR: #{pr_number} - {pr_url}"
3. ctx note "CHANGES: {files_changed} files, +{additions}/-{deletions}"
4. Generate handoff:
   - Create contexts/{JIRA_ID}-handoff.md
   - Include: API contracts, test coverage, deployment notes
```

## Memory Integration Pattern

```
Sequential thinking with memory:
1. Search existing patterns: memory search "similar service implementation"
2. Load context: ctx switch {context_name}
3. Retrieve decisions: ctx notes | grep "DECISION:"
4. Update memory: Create observation linking current implementation to pattern
```

## Error Tracking

```
When encountering errors:
- ctx note "ERROR: {error_type} - {file}:{line} - {description}"
- ctx note "FIX: {solution_description} - {commit_hash}"
- Memory observation: Add error pattern and solution to service entity
```

## Context Archival

```
On completion:
1. ctx set-state ✅
2. Export context: ctx export {context_name} > archives/{JIRA_ID}.json
3. Memory relation: {service_name} -> completed_in -> {sprint_id}
4. ctx close {context_name}
```
