# Agent Context Management Documentation

## Overview

This directory contains prompt templates and integration patterns for using ctx with various agent roles. Each document provides engineering-focused, practical guidance for implementing context-aware agent workflows.

## Agent Types

### Development Agents
- **[Backend Developer](./backend-dev-agent.md)** - Service implementation, testing, code review workflows
- **[Architecture Design](./architecture-design-agent.md)** - ADRs, pattern selection, system design

### Operations Agents
- **[DevOps/SRE](./devops-sre-agent.md)** - Incident response, deployments, infrastructure changes
- **[QA Testing](./qa-test-agent.md)** - Test execution, defect tracking, regression management

### Productivity Agents
- **[Personal Productivity](./personal-productivity-agent.md)** - Task management, learning, habit tracking

### Integration Guide
- **[Agentic Integration](./agentic-integration-guide.md)** - Advanced patterns for ctx + MCP tool integration

## Core Concepts

### Context Lifecycle
```
create -> active -> in_progress -> review -> complete -> archive
```

### Status Emoji Standards
- 🆕 New/Unstarted
- 💻 Active development
- 🔨 Implementation in progress
- 🧪 Testing
- 👀 In review
- 🚀 Deploying
- ✅ Complete
- 🚫 Blocked
- 🔥 Incident/Urgent

### Note Categories
- **SERVICE**: Service/component metadata
- **IMPL**: Implementation progress
- **TEST**: Test results and coverage
- **ERROR**: Error tracking
- **FIX**: Solutions applied
- **DECISION**: Architectural decisions
- **INTEGRATION**: External service details
- **CONFIG**: Configuration values

## Integration with MCP Tools

### Memory Server
- Entities mirror context names
- Observations capture context notes
- Relations model dependencies

### Sequential Execution
```
ctx -> memory lookup -> task execution -> dual update
```

### State Machine Pattern
Context status drives agent behavior through predictable state transitions.

## Usage Examples

See `/examples` directory for practical demonstrations:
- `agent-backend-dev.sh` - Backend development workflow
- `agent-qa-testing.sh` - QA test execution
- `agent-incident-response.sh` - Incident management

## Best Practices

1. **Structured Notes**: Use consistent prefixes (CATEGORY: details)
2. **Status Accuracy**: Update emoji to reflect true state
3. **Memory Sync**: Keep memory entities aligned with contexts
4. **Batch Operations**: Group related updates for efficiency
5. **Context Hygiene**: Archive completed contexts after 7 days

## Performance Considerations

- Limit active contexts to <50 for optimal performance
- Use grep/search for large note collections
- Implement note summarization for long-running contexts
- Cache frequently accessed memory patterns

## Extension Points

- Custom plugins for domain-specific workflows
- Integration with external systems (JIRA, GitHub)
- Automated context creation from webhooks
- Context templates from successful patterns
