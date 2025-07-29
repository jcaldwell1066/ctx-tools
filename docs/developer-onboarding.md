# Developer Onboarding Guide

Welcome to the **CTX** project! This guide provides new developers with a quick overview of the tool, its purpose, and how both AI agents and human team members can leverage it to share context.

## Project Purpose

CTX is a modular command-line system for managing development contexts. It helps you:

- Create and switch between multiple work contexts (e.g., tasks or tickets)
- Track status with easy-to-read emoji indicators
- Record timestamped notes and metadata
- Extend functionality through a plugin architecture

All context data lives under `~/.ctx/` using JSON or SQLite storage. This allows local experimentation without impacting shared repositories.

## Why Context Matters

During a project, developers and AI assistants often juggle several tasks at once. CTX organizes the details of each task into a single "context":

1. **Context Name** – a unique identifier such as `PROJECT-123`
2. **State** – current status (active, in-progress, blocked, etc.)
3. **Notes** – chronological log of decisions, commands, or results

By keeping these pieces in one place, human developers and automated agents can rapidly understand the history and next steps for any work item.

## Basic Workflow

```bash
# Create a new context
ctx create PROJECT-123 --description "Implement new API"

# Switch to it and add a note
ctx switch PROJECT-123
ctx note "Initial scaffolding complete"

# Update state when progress changes
ctx set-state in-progress
```

Check `README.md` for a comprehensive list of commands.

## Sharing Context Between Humans and AI

CTX contexts are stored as files under `~/.ctx/`. When multiple users or agents need access, you can:

1. **Export/Import** – use `ctx export` and `ctx import` to share context JSON files across systems.
2. **Shared Storage** – point the storage location to a shared folder or database so all agents read and write to the same dataset.
3. **Memory Integrations** – advanced setups (see `docs/agent-prompts/agentic-integration-guide.md`) synchronize context notes with an external memory server for long-term knowledge.

This flexibility allows AI assistants to log observations while human developers track implementation steps – everyone sees the same history and status.

## Additional Resources

- `README.md` – full feature overview and command reference
- `contexts/README.md` – explanation of local context files
- `docs/agent-prompts/` – example prompts for integrating CTX with various AI agent roles

Happy hacking!
