# CTX - Context Management System

A modular, extensible command-line tool for managing development contexts, tracking work states, and organizing project information.

## Features

- **Context Management**: Create, switch, and manage multiple work contexts
- **State Tracking**: Track context states with visual indicators (emojis)
- **Note Taking**: Add timestamped notes to contexts with optional tags
- **Stack Operations**: Push/pop contexts for quick switching
- **Plugin System**: Extend functionality with custom plugins
- **PS1 Integration**: Display context info in your shell prompt
- **Search & Filter**: Find contexts by name, content, state, or tags
- **Import/Export**: Share contexts between systems
- **🤖 AI Agent Integration**: Full MCP support for Cursor IDE and agent workflows

## Developer Onboarding

New contributors can read [`docs/developer-onboarding.md`](docs/developer-onboarding.md) for a concise introduction to CTX and how humans and AI agents share context.

## Quick Start

```bash
# Install CTX tools
python3 install_ctx.py

# Create a new context
ctx create my-project --description "Working on new feature"

# Add a note
ctx note "Started implementing user authentication"

# Update state
ctx set-state in-progress

# Show current context status
ctx status
```

## 🤖 AI Agent & Cursor Integration

For comprehensive setup with AI agents, Cursor IDE, and MCP integration, see:

**[📖 Comprehensive Agentic Integration Guide](docs/AGENTIC_INTEGRATION.md)**

This guide covers:
- Cursor IDE integration with MCP tools
- Agent workflow patterns (sprint management, incident response, development)
- Memory server synchronization
- Production deployment patterns
- Multi-agent coordination

### Quick Integration Test

```bash
# Test agentic integration
ctx create test-integration --description "Testing AI agent setup"
ctx set-state in-progress
ctx note "Integration test: MCP tools working"

# In Cursor chat, use: ctx_status, ctx_list, ctx_note
```

## Core Commands

### Context Lifecycle

```bash
# Create a new context
ctx create <name> [--description TEXT] [--tags TAG1 TAG2]

# List contexts (active/on-hold by default)
ctx list [--all] [--state STATE] [--tag TAG]

# Switch to a context
ctx switch <name>
# Alias: ctx sw <name>

# Show context status
ctx status [name]
# Alias: ctx st

# Delete a context
ctx delete <name>
```

### State Management

```bash
# Show available states
ctx set-state

# Set context state
ctx set-state active|in-progress|on-hold|in-review|blocked|pending|completed|cancelled

# Set custom state with emoji
ctx set-state custom --emoji 🚀
```

### Note Management

```bash
# Add a note to active context
ctx note "Your note text" [--tags bug feature]
# Alias: ctx n "Quick note"

# Show notes
ctx notes [--limit 10] [--reverse]

# Clear all notes
ctx clear-notes
```

### Stack Operations

```bash
# Push current context and switch
ctx push other-context

# Pop previous context
ctx pop

# View stack
ctx stack
```

### Search and Filter

```bash
# Search contexts by name, description, or notes
ctx search "payment"

# List contexts by state
ctx list --state in-progress

# List contexts by tag
ctx list --tag backend
```

### Import/Export

```bash
# Export context to file
ctx export my-project --output my-project.json

# Import context from file
ctx import my-project.json [--overwrite]
```

## PS1 Integration

Add context info to your shell prompt:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PS1='$(ctx ps1) \u@\h:\w\$ '

# Custom format
export PS1='[$(ctx ps1 --format "{name}|{state}|{notes}")] \$ '
```

## Plugin System

CTX supports plugins to extend functionality. Plugins can:
- Add new commands
- React to context events
- Provide custom status information
- Integrate with external tools

### Example: Sprint Plugin

The included sprint plugin adds agile development features:

```bash
# Context for a JIRA ticket automatically gets sprint tracking
ctx create PROJECT-123 --description "Implement new API endpoint"

# Update sprint phase
ctx set-state in-progress  # Automatically updates sprint phase

# The sprint plugin tracks:
# - Sprint phases (new → refinement → development → review → qa → production)
# - JIRA integration
# - Pull request tracking
# - Test results
# - Phase history
```

### Creating Custom Plugins

Create a Python file in `~/.ctx/plugins/`:

```python
from ctx.plugins import Plugin
from ctx.models import Context

class MyPlugin(Plugin):
    name = "my_plugin"
    description = "My custom plugin"
    version = "1.0.0"

    def get_commands(self):
        return {
            "my-command": {
                "help": "Do something custom",
                "handler": self.my_handler
            }
        }

    def on_context_created(self, context: Context):
        # React to context creation
        context.add_note(f"Initialized by {self.name}")

    def my_handler(self, context: Context, **kwargs):
        return "Command executed!"
```

## Architecture

```
ctx/
├── core.py          # Main context manager
├── models.py        # Data models (Context, Note, etc.)
├── storage.py       # Storage backends (JSON, SQLite)
├── plugins.py       # Plugin system
├── cli.py           # CLI interface (Click)
└── formatters.py    # Output formatting

plugins/
└── sprint.py        # Example sprint management plugin
```

## Data Storage

By default, CTX stores data in `~/.ctx/`:
- `contexts.json` - All context data
- `plugins/` - Custom plugins

The storage layer supports both JSON (default) and SQLite backends.

## Migration from Old CTX

If you're using the previous version of ctx:

```bash
# Run the migration script
python migrate_old_ctx.py

# This will:
# - Convert old session files to new format
# - Preserve all notes and history
# - Map old states to new states
# - Maintain active context
```

## Advanced Usage

### Context Metadata

Store custom metadata with contexts:

```python
# Via API (for plugins)
manager.get("my-context").metadata["custom_field"] = "value"
```

### Multiple Storage Backends

```python
from ctx.core import ContextManager
from ctx.storage import SqliteStorage

# Use SQLite instead of JSON
manager = ContextManager()
manager.storage = SqliteStorage(Path.home() / ".ctx" / "contexts.db")
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black ctx/

# Type checking
mypy ctx/
```

## Architecture Benefits

### Extensibility
- Plugins can add domain-specific features without modifying core code
- Easy to share and distribute plugins
- Event-driven architecture for flexible integrations

### Performance
- Fast operations with simplified data model
- Efficient storage with SQLite option
- Minimal dependencies (only Click required)

### Maintainability
- Clear module boundaries with distinct responsibilities
- Type hints throughout for better IDE support
- Comprehensive docstrings and clean API
- Plugin isolation prevents conflicts

## Example Usage Patterns

### Development Workflow
```bash
# Create feature context
ctx create feature-auth --tags backend security

# Track progress
ctx note "Implemented user model"
ctx note "Added JWT tokens" --tags api
ctx set-state in-progress

# Quick switch for hotfix
ctx push hotfix-bug
# ... work on hotfix ...
ctx pop  # Back to feature-auth
```

### Sprint Management
```bash
# Sprint item auto-configured with plugin
ctx create PROJECT-123 --description "New API endpoint"

# Track sprint lifecycle
ctx set-state in-progress  # → Development phase
ctx note "PR #1090 created"
ctx set-state in-review    # → Review phase
ctx note "Review feedback addressed"
ctx set-state pending      # → QA handoff
```

### Context Organization
```bash
# List active work
ctx list

# Find specific contexts
ctx search payment

# Filter by state
ctx list --state in-progress

# Filter by tag
ctx list --tag backend
```

## Comparison with Old System

| Feature | Old CTX | New CTX |
|---------|---------|---------|
| Lines of Code | 900+ | ~600 |
| Dependencies | Multiple | Click only |
| Domain Coupling | Service-specific | Domain-agnostic |
| Plugin Support | No | Yes |
| Storage | Complex JSON | Simple JSON/SQLite |
| State Management | Complex workflow states | Simple states + plugins |
| Performance | Slower | Fast |

## Best Practices

1. **Use descriptive context names**: `feature-auth`, `bugfix-payment`, `JIRA-1234`
2. **Add notes frequently**: Track your progress and decisions
3. **Use tags**: Organize contexts by project, type, or priority
4. **Leverage plugins**: Extend CTX for your workflow
5. **Export important contexts**: Backup or share with team

## Troubleshooting

**Context not found**: Check with `ctx list --all` to see all contexts including completed ones.

**Plugin not loading**: Ensure plugin file is in `~/.ctx/plugins/` and has no syntax errors.

**PS1 not updating**: Make sure to use command substitution `$(ctx ps1)` not just `ctx ps1`.

## License

MIT License - see LICENSE file for details.
