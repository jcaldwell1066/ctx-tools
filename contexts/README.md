# Contexts Directory

This directory stores context files managed by the CTX tool. Context files are JSON files that contain:

- Context metadata (name, description, created date)
- State tracking (pending, in-progress, completed, etc.)
- Notes and documentation
- Plugin-specific data (e.g., sprint tracking, deployment info)

## File Structure

- `*.json` - Context data files (automatically created by CTX)
- `*.md` - Optional markdown documentation for contexts
- `example-*.md` - Example context documentation templates

## Example Files

The `example-project-sprint.md` file demonstrates how to document a sprint context with:
- Sprint overview and status
- Technical details and configuration
- Testing methodology
- Acceptance criteria
- Handoff information

## Usage

Context files are automatically created and managed by the CTX tool:

```bash
# Create a new context (creates a .json file)
ctx create PROJECT-123 --description "New feature"

# Add notes to a context
ctx note "Implementation details..."

# The JSON files are managed by CTX - do not edit directly
```

## .gitignore

User-specific context JSON files are ignored by git to prevent accidental commits of private data. Only example files and documentation are tracked.