# Agentic Integration Guide for CTX

## Overview

This guide demonstrates how to leverage ctx with MCP tools for true agentic workflows. The combination enables stateful context management, persistent memory, and intelligent decision-making.

## Core Integration Pattern

```yaml
agent_stack:
  context_layer: ctx
  memory_layer: mcp_memory_docker
  execution_layer: mcp_filesystem/browser/terminal
  
workflow:
  1. Context establishment (ctx)
  2. Memory retrieval (mcp_memory)
  3. Task execution (domain tools)
  4. State update (ctx + memory)
```

## Sequential Thinking Pattern

### 1. Context-Aware Execution

```
Pattern: Load context -> Check memory -> Execute -> Update both

Example:
1. ctx switch {context_name}
2. memory search "{relevant_pattern}"
3. Execute task based on context + memory
4. ctx add-note "RESULT: {outcome}"
5. memory add observation to relevant entity
```

### 2. Decision Tree Navigation

```
Pattern: State-driven branching with memory consultation

if ctx_status == "🚫":
    memory search "unblock {blocker_type}"
    apply_solution_from_memory()
    ctx set-status "💻"
elif ctx_status == "👀":
    check_review_feedback()
    ctx add-note "FEEDBACK: {summary}"
    update_memory_with_patterns()
```

### 3. Failure Recovery

```
Pattern: Capture failure -> Find pattern -> Apply fix -> Document

on_error:
    ctx add-note "ERROR: {error_details}"
    solutions = memory search "{error_type} solution"
    if solutions:
        apply_solution(solutions[0])
        ctx add-note "APPLIED: {solution_id}"
    else:
        ctx set-status "🚫"
        escalate_to_human()
```

## Memory-Enhanced Context Patterns

### 1. Pattern Recognition

```
Workflow:
1. Analyze current context notes
2. Extract patterns: ctx show-notes | analyze_patterns()
3. Memory query: Similar patterns in history
4. Apply learned optimizations
5. Create new memory observations
```

### 2. Predictive Context Switching

```
Based on patterns:
- If PR merged -> Auto-switch to deployment context
- If tests fail -> Create debug context
- If blocked -> Search memory for unblockers
```

### 3. Knowledge Graph Integration

```
Context to Memory mapping:
- ctx context -> memory entity
- ctx notes -> memory observations  
- ctx status -> memory relations

Query examples:
- "Contexts that had similar blockers"
- "Successful patterns for {task_type}"
- "Team members who solved {problem}"
```

## Advanced Integration Scenarios

### 1. Multi-Agent Coordination

```
Agent A (Developer):
1. ctx create feature-xyz
2. Implement feature
3. ctx add-note "HANDOFF: Ready for review"
4. memory relation: feature-xyz -> ready_for -> review

Agent B (Reviewer):
1. memory search "ready_for review"
2. ctx switch feature-xyz
3. Perform review
4. ctx add-note "REVIEW: {feedback}"
```

### 2. Continuous Learning

```
Learning loop:
1. Execute task in context
2. Measure outcome metrics
3. Compare with memory patterns
4. Update memory with performance data
5. Adjust future execution strategies
```

### 3. Context Templates from Memory

```
Template generation:
1. memory search "successful {project_type} setup"
2. Extract common patterns
3. Generate ctx initialization script
4. Apply template to new projects
```

## State Machine Implementation

```python
class AgenticStateMachine:
    states = {
        "init": ["planning", "blocked"],
        "planning": ["development", "blocked"],
        "development": ["testing", "review", "blocked"],
        "review": ["development", "testing", "deployment"],
        "deployment": ["monitoring", "rollback"],
        "monitoring": ["completed", "incident"]
    }
    
    def transition(self, current_ctx):
        current_state = self.get_state_from_emoji(current_ctx.emoji)
        possible_next = self.states[current_state]
        
        # Consult memory for best transition
        memory_recommendation = memory_search(
            f"best transition from {current_state} given {current_ctx.notes[-1]}"
        )
        
        return self.apply_transition(memory_recommendation)
```

## Context Lifecycle Automation

### 1. Auto-Creation

```
Triggers:
- New JIRA ticket -> Create context
- PR opened -> Create review context  
- Incident alert -> Create incident context
```

### 2. Auto-Archival

```
Conditions:
- Status = ✅ for > 7 days
- No notes added for > 30 days
- Linked PR merged + deployed
```

### 3. Context Inheritance

```
Parent-child relationships:
- Epic context spawns feature contexts
- Feature context spawns task contexts
- Incident context spawns investigation contexts
```

## Performance Optimization

### 1. Context Preloading

```
On agent startup:
1. Load active contexts
2. Prefetch related memory entities
3. Cache frequent transitions
4. Prepare context-specific tools
```

### 2. Batch Operations

```
Efficient updates:
- Collect multiple notes before writing
- Batch memory queries
- Aggregate status transitions
```

### 3. Context Compression

```
For long-running contexts:
1. Summarize old notes periodically
2. Archive to memory as observations
3. Keep only recent/relevant in ctx
```

## Best Practices

### 1. Naming Conventions

```
Contexts: {type}-{identifier}-{component}
Notes: {CATEGORY}: {details} | {metadata}
Memory: Entities match context names
```

### 2. Status Emoji Semantics

```
Standardize across agents:
- 🆕 = Needs initialization
- 💻 = Active work
- 👀 = Awaiting input
- 🚫 = Blocked
- ✅ = Complete
```

### 3. Memory Hygiene

```
Regular maintenance:
- Deduplicate similar patterns
- Update outdated relations
- Prune irrelevant observations
- Strengthen successful patterns
```

## Integration Testing

```bash
# Test context-memory sync
ctx create test-integration
memory create entity "test-integration" type="test"
ctx add-note "TEST: Integration verified"
memory add observation "test-integration" "Integration verified"

# Verify bidirectional lookup
ctx show-notes | grep "TEST"
memory open "test-integration"
```

## Metrics and Monitoring

```
Track effectiveness:
- Context switch frequency
- Average context lifetime
- Memory query hit rate
- Pattern application success rate
- Time to resolution by context type
``` 