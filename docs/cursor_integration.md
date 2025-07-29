# Cursor Integration with CTX

This document describes how to integrate the CTX context management system with Cursor IDE for enhanced development workflow.

## Configuration Levels

### 1. User-Level Configuration (`~/.cursor/`)

**Main MCP Configuration**: `~/.cursor/mcp.json`
- Contains global MCP servers available across all projects
- Includes database connections, memory servers, filesystem access
- Current servers: mysql_*, memory, filesystem, sequential-thinking

### 2. Project-Level Configuration (`.vscode/`)

**Settings**: `.vscode/settings.json`
- Python interpreter configuration
- Terminal integration with CTX_PROJECT environment variable
- File exclusions and workspace customization
- CTX-specific color customizations

**Tasks**: `.vscode/tasks.json`
- Quick access to ctx commands via Command Palette (Ctrl+Shift+P)
- Available tasks:
  - `ctx: Show Status` - Display current context status
  - `ctx: Add Note` - Add note with interactive prompt
  - `ctx: Set State - [state]` - Quick state transitions
  - `ctx: List Contexts` - Show all contexts
  - `Install ctx-tools` - Reinstall ctx tools
  - `Run ctx tests` - Execute test suite

**MCP Integration**: `.vscode/mcp.json`
- Project-specific MCP server for ctx integration
- Exposes ctx functionality as MCP tools within Cursor

## MCP Tools Available in Cursor

When the ctx MCP server is active, you can use these tools in your Cursor chat:

### Context Management
- `ctx_status` - Get current context status
- `ctx_list` - List all contexts  
- `ctx_create` - Create new context
- `ctx_switch` - Switch to different context

### State Management
- `ctx_set_state` - Change context state
  - States: active, in-progress, on-hold, in-review, blocked, pending, completed, cancelled

### Note Taking
- `ctx_note` - Add note to current context

## Usage Examples

### In Cursor Chat
```
Can you check the current ctx status?
→ Uses ctx_status tool automatically

Add a note: "Implemented user authentication"
→ Uses ctx_note tool with the text

Set context state to in-review
→ Uses ctx_set_state tool with "in-review"
```

### Via Command Palette (Ctrl+Shift+P)
```
Tasks: Run Task → ctx: Show Status
Tasks: Run Task → ctx: Add Note
Tasks: Run Task → ctx: Set State - In Progress
```

### Via Terminal Integration
- PS1 prompt shows current context: `[ctx-tools-dev 💻]`
- Environment variable `CTX_PROJECT` set to current context
- All ctx commands available in integrated terminal

## Setup Instructions

### 1. Copy Project Configuration
```bash
# Copy .vscode/ directory to your project
cp -r /path/to/ctx-tools/.vscode/ ./

# Update paths in .vscode/mcp.json to point to your project
```

### 2. Global MCP Integration
Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "ctx-global": {
      "command": "python3",
      "args": ["/path/to/ctx-tools/cursor_ctx_integration.py"],
      "env": {
        "PATH": "/home/user/.local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

### 3. Terminal Setup
Add to your shell profile (`.bashrc`, `.zshrc`):
```bash
# Auto-activate ctx context based on directory
if [[ -n "$CTX_AUTO_ACTIVATE" && -n "$CTX_PROJECT" ]]; then
    ctx switch "$CTX_PROJECT" 2>/dev/null || true
fi

# Custom PS1 with ctx integration
if command -v ctx >/dev/null 2>&1; then
    PS1="[\$(ctx ps1 2>/dev/null || echo 'no-ctx')] $PS1"
fi
```

## Benefits

### For Developers
- **Context Awareness**: Cursor knows which context you're working in
- **Quick Actions**: Fast access to ctx commands via tasks and MCP tools
- **Visual Feedback**: PS1 prompt and status bar show current context state
- **Note Integration**: Add development notes without leaving the editor

### For Teams
- **Consistent Workflow**: Standardized ctx integration across projects
- **Documentation**: Context states and notes provide project history
- **Handoffs**: Easy context switching for code reviews and collaboration

### For Projects
- **Automated Tracking**: Development phases tracked automatically
- **State Management**: Clear progression through development lifecycle
- **Integration**: Works with existing VSCode/Cursor extensions

## Troubleshooting

### MCP Server Not Loading
```bash
# Test the MCP server directly
python3 cursor_ctx_integration.py
# Should wait for JSON-RPC input

# Check if ctx command is available
which ctx
ctx --version
```

### Tasks Not Appearing
- Reload Cursor window (Ctrl+Shift+P → "Developer: Reload Window")
- Check `.vscode/tasks.json` syntax
- Ensure ctx is in PATH

### PS1 Integration Issues
```bash
# Test ctx ps1 command
ctx ps1

# Check environment variables
echo $CTX_PROJECT
echo $CTX_AUTO_ACTIVATE
```

## Advanced Configuration

### Custom State Emojis
Modify the ctx configuration to use custom emojis for different project types:
- 🚀 for new features
- 🐛 for bug fixes  
- 📝 for documentation
- 🔧 for maintenance

### Project Templates
Create project-specific `.vscode/` templates for different types of development:
- Python projects
- Web applications
- Documentation projects
- DevOps/Infrastructure

### CI/CD Integration
Use ctx state information in build pipelines:
```bash
# In CI script
CURRENT_STATE=$(ctx status --format=json | jq -r '.state')
if [[ "$CURRENT_STATE" == "in-review" ]]; then
    echo "Running additional review checks..."
fi
```