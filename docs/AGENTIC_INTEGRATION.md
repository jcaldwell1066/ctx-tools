# Comprehensive Agentic Integration Guide for CTX

This document provides complete setup and integration patterns for using CTX with AI agents, Cursor IDE, and MCP (Model Context Protocol) servers.

## Table of Contents

1. [Quick Setup](#quick-setup)
2. [MCP Integration](#mcp-integration)
3. [Cursor IDE Integration](#cursor-ide-integration)
4. [Agent Workflow Patterns](#agent-workflow-patterns)
5. [Memory Server Integration](#memory-server-integration)
6. [Production Deployment](#production-deployment)
7. [Troubleshooting](#troubleshooting)

## Quick Setup

### Prerequisites

- Python 3.7+ with `pip`
- Cursor IDE (recommended) or VS Code
- CTX tools installed (`pip install -e .`)

### 1. Install CTX Tools

```bash
# Clone and install
git clone https://github.com/yourusername/ctx-tools.git
cd ctx-tools
python3 install_ctx.py
```

### 2. Configure Cursor IDE

The project includes pre-configured VS Code/Cursor settings:

```bash
# Files already configured:
.vscode/mcp.json       # MCP server for ctx integration
.vscode/settings.json  # Python environment and CTX vars
.vscode/tasks.json     # Quick access to ctx commands
```

### 3. Test Integration

```bash
# Test basic functionality
ctx create test-integration --description "Testing agentic setup"
ctx set-state in-progress
ctx note "Integration test started"

# Test Cursor integration (in Cursor chat):
# Use: ctx_status, ctx_list, ctx_note tools
```

## MCP Integration

### Project MCP Server

The included MCP server (`cursor_ctx_integration.py`) exposes 6 tools:

| Tool | Purpose | Parameters |
|------|---------|------------|
| `ctx_status` | Get current context status | None |
| `ctx_list` | List all contexts | None |
| `ctx_create` | Create new context | name, description |
| `ctx_switch` | Switch to context | name |
| `ctx_set_state` | Update context state | state |
| `ctx_note` | Add note to context | text |

### Configuration

The MCP server is configured in `.vscode/mcp.json`:

```json
{
  "mcpServers": {
    "ctx-tools": {
      "command": "python3",
      "args": ["/path/to/ctx-tools/cursor_ctx_integration.py"],
      "env": {
        "CTX_PROJECT": "your-project-name"
      }
    }
  }
}
```

## Cursor IDE Integration

### Available Tasks

Access via `Ctrl+Shift+P` → "Tasks: Run Task":

- **ctx: Show Status** - Display current context
- **ctx: Add Note** - Interactive note entry
- **ctx: Set State - [state]** - Quick state transitions
- **ctx: List Contexts** - Show all contexts
- **Install ctx-tools** - Reinstall/update
- **Run ctx tests** - Execute test suite

### Environment Variables

Set in `.vscode/settings.json`:

```json
{
  "terminal.integrated.env.linux": {
    "CTX_PROJECT": "your-project-name",
    "CTX_AUTO_ACTIVATE": "true"
  }
}
```

## Agent Workflow Patterns

### Pattern 1: Sprint Management Agent

```python
# Initialize sprint context
ctx create JIRA-123-feature --description "New API endpoint"
ctx set-state in-progress
ctx note "SERVICE: PaymentAPI | ENDPOINT: /api/v1/payments"
ctx note "BRANCH: feature/JIRA-123 | TARGET: dev-environment"

# Track implementation
ctx note "IMPL: Database schema - COMPLETE"
ctx note "IMPL: Service layer - IN_PROGRESS"
ctx note "TEST: Unit tests - 15/20 passing"

# Handoff to QA
ctx set-state in-review
ctx note "HANDOFF: PR #1234 ready for QA review"
```

### Pattern 2: Incident Response Agent

```python
# Incident detection
ctx create INC-2025-001-api-down --description "API outage"
ctx set-state blocked  # Using 🚫 emoji
ctx note "SEVERITY: P1 | SERVICE: payment-api"
ctx note "SYMPTOMS: 500 errors on /api/v1/process"

# Investigation
ctx note "CHECK: Database - HEALTHY"
ctx note "CHECK: External gateway - DEGRADED"
ctx note "ACTION: Enabled circuit breaker - SUCCESS"

# Resolution
ctx set-state completed
ctx note "RCA: Payment gateway provider database failover"
```

### Pattern 3: Development Context Agent

```python
# Feature development
ctx create feature-auth-system
ctx set-state in-progress
ctx note "ARCHITECTURE: JWT tokens + refresh mechanism"
ctx note "DEPENDENCIES: bcrypt, jsonwebtoken, redis"

# Technical decisions
ctx note "DECISION: Using RS256 for token signing"
ctx note "DECISION: 15min access token, 7day refresh token"

# Implementation tracking
ctx note "PROGRESS: User model complete"
ctx note "PROGRESS: Login endpoint 80% complete"
ctx note "NEXT: Implement token refresh logic"
```

## Memory Server Integration

### Synchronization Pattern

For advanced setups with external memory servers:

```python
# Bidirectional sync pattern
def sync_context_to_memory(context_name):
    context = ctx.get(context_name)
    
    # Create memory entity
    memory.create_entity(
        name=context.name,
        type="development_context",
        observations=context.notes
    )
    
    # Create relations
    for dependency in context.metadata.get('dependencies', []):
        memory.create_relation(
            from_entity=context.name,
            to_entity=dependency,
            relation_type="depends_on"
        )

# Usage in agent workflows
ctx create PROJECT-456
memory_sync(ctx.active_context)
ctx note "Started implementation"
memory.add_observation(ctx.active_context, "Implementation started")
```

### Event-Driven Updates

```python
# Hook into ctx events
class MemorySyncPlugin(Plugin):
    def on_note_added(self, context, note):
        memory.add_observation(context.name, note.text)
    
    def on_state_changed(self, context, old_state, new_state):
        memory.add_observation(
            context.name, 
            f"State changed: {old_state} → {new_state}"
        )
```

## Production Deployment

### Environment Setup

```bash
# Production environment variables
export CTX_STORAGE_TYPE=sqlite
export CTX_DB_PATH=/shared/contexts/production.db
export CTX_BACKUP_ENABLED=true
export CTX_BACKUP_INTERVAL=3600  # 1 hour
```

### Team Collaboration

```bash
# Shared context setup for teams
ctx export critical-incident > shared/contexts/critical-incident.json
# Team members can import:
ctx import shared/contexts/critical-incident.json

# Or use shared storage
export CTX_STORAGE_PATH=/shared/team-contexts/
```

### Agent Deployment

```yaml
# Docker compose example
services:
  ctx-agent:
    build: .
    environment:
      - CTX_PROJECT=production-system
      - CTX_STORAGE_TYPE=sqlite
      - CTX_DB_PATH=/data/contexts.db
    volumes:
      - ./contexts:/data
      - ./scripts:/app/scripts
```

## Troubleshooting

### Common Issues

**MCP Tools Not Available**
```bash
# Check MCP server status
ps aux | grep cursor_ctx_integration
# Restart Cursor IDE
# Check .vscode/mcp.json path is absolute
```

**Context Not Found**
```bash
# List all contexts including completed
ctx list --all
# Check active context
ctx status
```

**Performance Issues**
```bash
# Use SQLite for better performance
export CTX_STORAGE_TYPE=sqlite
# Clean up old contexts
ctx list --state completed | xargs ctx delete
```

**Installation Issues**
```bash
# Reinstall with verbose output
python3 install_ctx.py
# Check Python version
python3 --version  # Must be 3.7+
# Check dependencies
pip install -e .[dev] --verbose
```

### Debug Mode

```bash
# Enable debug logging
export CTX_DEBUG=true
ctx status  # Will show detailed debug info

# Check MCP server logs
tail -f ~/.cursor/logs/mcp.log
```

### Testing Integration

```bash
# Run comprehensive tests
python3 -m pytest tests/ -v

# Test MCP integration
curl -X POST http://localhost:3000/mcp/ctx-tools/ctx_status

# Test memory sync (if configured)
memory search "test context"
ctx notes | grep "test"
```

## Best Practices

### Agent Design

1. **State-Driven Logic**: Always check context state before taking action
2. **Atomic Notes**: One concept per note for better searchability  
3. **Consistent Tagging**: Use consistent prefixes (IMPL:, TEST:, ERROR:)
4. **Handoff Protocols**: Clear state transitions with handoff notes

### Performance

1. **Batch Operations**: Group multiple ctx operations when possible
2. **Selective Sync**: Only sync relevant contexts to memory servers
3. **Regular Cleanup**: Archive completed contexts periodically
4. **Index Management**: Use tags for efficient context filtering

### Security

1. **Sensitive Data**: Never store secrets in context notes
2. **Access Control**: Use shared storage with proper permissions
3. **Audit Trail**: Enable logging for production environments
4. **Backup Strategy**: Regular exports of critical contexts

## Advanced Patterns

### Multi-Agent Coordination

```python
# Agent handoff pattern
class DevAgent:
    def complete_implementation(self, context_name):
        ctx.set_state(context_name, "in-review")
        ctx.note(context_name, "HANDOFF: Ready for QA review")
        ctx.note(context_name, f"PR: #{self.pr_number}")
        
        # Signal QA agent
        memory.create_relation(context_name, "qa-queue", "ready_for")

class QAAgent:
    def pick_up_work(self):
        ready_contexts = memory.search_relations("ready_for qa-queue")
        for context in ready_contexts:
            ctx.switch(context)
            ctx.set_state("in-progress")
            ctx.note("QA: Started test execution")
```

### Context Inheritance

```python
# Parent-child context relationships
ctx create EPIC-100 --description "Payment system overhaul"
ctx create EPIC-100-auth --description "Authentication module" --parent EPIC-100
ctx create EPIC-100-api --description "API endpoints" --parent EPIC-100

# Inherit configuration from parent
ctx note EPIC-100 "CONFIG: payment_gateway_url=https://api.payment.com"
# Child contexts automatically inherit parent config
```

This guide provides the foundation for sophisticated agentic workflows with CTX. Start with basic patterns and gradually adopt advanced features as your team's needs evolve.