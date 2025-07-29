"""
Command-line interface for ctx
"""

import click
import sys
import os
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from . import __version__
from .core import ContextManager
from .models import ContextState
from .formatters import (
    format_context_list,
    format_context_status,
    format_notes,
    format_stack,
    format_search_results,
)


# Create context manager instance
_ctx_manager = None


def get_ctx_manager() -> ContextManager:
    """Get or create the context manager instance"""
    global _ctx_manager
    if _ctx_manager is None:
        env_path = os.environ.get("CTX_STORAGE_PATH")
        if env_path:
            _ctx_manager = ContextManager(storage_path=Path(env_path))
        else:
            _ctx_manager = ContextManager()
    return _ctx_manager


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version")
@click.pass_context
def cli(ctx, version):
    """CTX - Context Management System

    A modular, extensible tool for managing development contexts,
    tracking work states, and organizing project information.
    """
    if version:
        click.echo(f"ctx version {__version__}")
        ctx.exit()

    # Debug: Show what Click thinks the subcommand is
    # print(f"DEBUG: invoked_subcommand = {ctx.invoked_subcommand}")

    # If no subcommand, show status
    if ctx.invoked_subcommand is None:
        ctx.invoke(status)


# Context lifecycle commands


@cli.command()
@click.argument("name")
@click.option("--description", "-d", help="Context description")
@click.option("--tags", "-t", multiple=True, help="Context tags")
def create(name: str, description: str, tags: tuple):
    """Create a new context"""
    print(
        f"DEBUG: create() called with name='{name}', description='{description}', tags={tags}"
    )
    manager = get_ctx_manager()

    try:
        context = manager.create(
            name=name, description=description or "", tags=list(tags)
        )
        click.echo(f"✅ Created context: {name}")

        # Auto-switch to new context
        click.echo(f"🔄 Switched to: {name} {context.emoji}")
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)


@cli.command(name="list")
@click.option("--all", "-a", is_flag=True, help="Show all contexts including completed")
@click.option("--state", "-s", help="Filter by state")
@click.option("--tag", help="Filter by tag")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["table", "simple", "json"]),
    default="table",
    help="Output format",
)
def list_contexts(all: bool, state: str, tag: str, format: str):
    """List all contexts"""
    print(
        f"DEBUG: list() called with all={all}, state='{state}', tag='{tag}', format='{format}'"
    )
    manager = get_ctx_manager()

    contexts = manager.list()

    # Apply filters
    if not all:
        # Hide completed/cancelled by default
        contexts = [
            c
            for c in contexts
            if c.state not in [ContextState.COMPLETED, ContextState.CANCELLED]
        ]

    if state:
        try:
            state_enum = ContextState.from_string(state)
            contexts = [c for c in contexts if c.state == state_enum]
        except:
            click.echo(f"❌ Invalid state: {state}", err=True)
            sys.exit(1)

    if tag:
        contexts = [c for c in contexts if tag in c.tags]

    if not contexts:
        click.echo("No contexts found.")
        return

    # Format and display
    output = format_context_list(contexts, manager.data.get("active"), format)
    click.echo(output)


@cli.command()
@click.argument("name")
def switch(name: str):
    """Switch to a different context"""
    manager = get_ctx_manager()

    try:
        context = manager.switch(name)
        click.echo(f"🔄 Switched to: {name} {context.emoji}")
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("name", required=False)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed information")
def status(name: Optional[str], verbose: bool):
    """Show context status (current if no name given)"""
    manager = get_ctx_manager()

    if name:
        context = manager.get(name)
        if not context:
            click.echo(f"❌ Context '{name}' not found", err=True)
            sys.exit(1)
    else:
        context = manager.get_active()
        if not context:
            click.echo("❌ No active context. Create one with: ctx create <name>")
            sys.exit(1)

    # Get plugin status info
    plugin_info = manager.plugin_manager.get_status_info(context)

    output = format_context_status(
        context,
        is_active=(context.name == manager.data.get("active")),
        verbose=verbose,
        plugin_info=plugin_info,
    )
    click.echo(output)


@cli.command()
@click.argument("name")
@click.confirmation_option(prompt="Are you sure you want to delete this context?")
def delete(name: str):
    """Delete a context"""
    manager = get_ctx_manager()

    try:
        manager.delete(name)
        click.echo(f"🗑️  Deleted context: {name}")
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)


# State management commands


@cli.command("set-state")
@click.argument("state", required=False)
@click.option("--emoji", "-e", help="Custom emoji (for custom state)")
@click.option("--context", "-c", help="Context name (default: active)")
def set_state(state: Optional[str], emoji: str, context: str):
    """Set context state

    Available states:
    - active (🔵)
    - in-progress (💻)
    - on-hold (⏸️)
    - in-review (👀)
    - blocked (🚫)
    - pending (⏳)
    - completed (✅)
    - cancelled (❌)
    - custom (with --emoji)
    """
    manager = get_ctx_manager()

    # Show available states if no state given
    if not state:
        click.echo("Available states:")
        for s in ContextState:
            click.echo(f"  {s.value:<15} {s.emoji}")
        return

    # Get context
    ctx_name = context or manager.data.get("active")
    if not ctx_name:
        click.echo("❌ No active context", err=True)
        sys.exit(1)

    # Parse state
    if state == "custom" and not emoji:
        click.echo("❌ Custom state requires --emoji", err=True)
        sys.exit(1)

    try:
        state_enum = ContextState.from_string(state)
        manager.set_state(ctx_name, state_enum, emoji)

        ctx = manager.get(ctx_name)
        click.echo(f"✅ Updated state: {ctx.emoji} {state}")
    except Exception as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)


# Note management commands


@cli.command("note")
@click.argument("text", nargs=-1, required=True)
@click.option("--tags", "-t", multiple=True, help="Note tags")
@click.option("--context", "-c", help="Context name (default: active)")
def add_note(text: tuple, tags: tuple, context: str):
    """Add a note to context"""
    manager = get_ctx_manager()

    # Get context
    ctx_name = context or manager.data.get("active")
    if not ctx_name:
        click.echo("❌ No active context", err=True)
        sys.exit(1)

    # Join text arguments
    note_text = " ".join(text)

    try:
        manager.add_note(ctx_name, note_text, list(tags))
        click.echo(f"📝 Note added to '{ctx_name}'")
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)


@cli.command("show-notes")
@click.option("--context", "-c", help="Context name (default: active)")
@click.option("--limit", "-n", type=int, help="Limit number of notes shown")
@click.option("--reverse", "-r", is_flag=True, help="Show oldest first")
def show_notes(context: str, limit: int, reverse: bool):
    """Show context notes"""
    manager = get_ctx_manager()

    # Get context
    ctx_name = context or manager.data.get("active")
    if not ctx_name:
        click.echo("❌ No active context", err=True)
        sys.exit(1)

    ctx = manager.get(ctx_name)
    if not ctx:
        click.echo(f"❌ Context '{ctx_name}' not found", err=True)
        sys.exit(1)

    if not ctx.notes:
        click.echo(f"No notes in context '{ctx_name}'")
        return

    note_list = ctx.notes
    if not reverse:
        # Use slicing instead of reversed() to avoid Click recursion bug
        note_list = note_list[::-1]

    if limit:
        note_list = note_list[:limit]

    output = format_notes(note_list, ctx_name)
    click.echo(output)


@cli.command("notes")
@click.option("--context", "-c", help="Context name (default: active)")
@click.option("--limit", "-n", type=int, help="Limit number of notes shown")
@click.option("--reverse", "-r", is_flag=True, help="Show oldest first")
def notes(context: str, limit: int, reverse: bool):
    """Alias for show-notes"""
    ctx = click.get_current_context()
    ctx.invoke(show_notes, context=context, limit=limit, reverse=reverse)


@cli.command("clear-notes")
@click.option("--context", "-c", help="Context name (default: active)")
@click.confirmation_option(prompt="Clear all notes?")
def clear_notes(context: str):
    """Clear all notes from context"""
    manager = get_ctx_manager()

    ctx_name = context or manager.data.get("active")
    if not ctx_name:
        click.echo("❌ No active context", err=True)
        sys.exit(1)

    try:
        manager.clear_notes(ctx_name)
        click.echo(f"🗑️  Notes cleared for '{ctx_name}'")
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)


# Stack operations


@cli.command()
@click.argument("name")
def push(name: str):
    """Push current context and switch to another"""
    manager = get_ctx_manager()

    try:
        current = manager.get_active()
        manager.push(name)

        if current:
            click.echo(f"📚 Pushed '{current.name}' to stack")
        click.echo(f"🔄 Switched to: {name}")
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)


@cli.command()
def pop():
    """Pop and switch to previous context"""
    manager = get_ctx_manager()

    context = manager.pop()
    if context:
        click.echo(f"🔄 Popped and switched to: {context.name} {context.emoji}")
    else:
        click.echo("❌ Context stack is empty")


@cli.command()
def stack():
    """Show context stack"""
    manager = get_ctx_manager()

    stack_names = manager.peek_stack()
    if not stack_names:
        click.echo("Context stack is empty")
        return

    output = format_stack(stack_names)
    click.echo(output)


# Search and filter


@cli.command()
@click.argument("query")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["simple", "detailed"]),
    default="simple",
    help="Output format",
)
def search(query: str, format: str):
    """Search contexts by name, description, or notes"""
    manager = get_ctx_manager()

    results = manager.search(query)
    if not results:
        click.echo(f"No contexts found matching '{query}'")
        return

    output = format_search_results(results, query, format)
    click.echo(output)


# Import/Export


@cli.command()
@click.argument("name")
@click.option(
    "--output", "-o", type=click.Path(), help="Output file (default: <name>.json)"
)
def export(name: str, output: str):
    """Export a context to file"""
    manager = get_ctx_manager()

    try:
        data = manager.export_context(name)

        # Determine output file
        if not output:
            output = f"{name}.json"

        # Write to file
        import json

        with open(output, "w") as f:
            json.dump(data, f, indent=2)

        click.echo(f"✅ Exported context '{name}' to {output}")
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)


@cli.command("import")
@click.argument("file", type=click.Path(exists=True))
@click.option("--overwrite", is_flag=True, help="Overwrite if exists")
def import_context(file: str, overwrite: bool):
    """Import a context from file"""
    manager = get_ctx_manager()

    try:
        import json

        with open(file, "r") as f:
            data = json.load(f)

        manager.import_context(data, overwrite)
        click.echo(f"✅ Imported context '{data['name']}' from {file}")
    except Exception as e:
        click.echo(f"❌ Import failed: {e}", err=True)
        sys.exit(1)


# PS1 integration


@cli.command()
@click.option("--format", "-f", default="{name} {emoji}", help="PS1 format string")
def ps1(format: str):
    """Get PS1 prompt info"""
    manager = get_ctx_manager()

    context = manager.get_active()
    if not context:
        return

    # Get plugin PS1 info
    plugin_info = manager.plugin_manager.get_ps1_info(context)

    # Format PS1
    ps1 = format.format(
        name=context.name[:15] + "..." if len(context.name) > 18 else context.name,
        emoji=context.emoji,
        state=context.state.value,
        notes=str(context.note_count),
    )

    # Add plugin info
    if plugin_info:
        ps1 += " " + " ".join(plugin_info)

    click.echo(ps1, nl=False)


# Plugin management


@cli.group()
def plugin():
    """Plugin management commands"""
    pass


@plugin.command("list")
def plugin_list():
    """List installed plugins"""
    manager = get_ctx_manager()

    plugins = manager.plugin_manager.list_plugins()
    if not plugins:
        click.echo("No plugins installed")
        return

    click.echo("Installed plugins:")
    for p in plugins:
        click.echo(f"  {p.name:<20} {p.version:<10} {p.description}")


@plugin.command("commands")
def plugin_commands():
    """Show plugin commands"""
    manager = get_ctx_manager()

    all_commands = manager.plugin_manager.get_all_commands()
    if not all_commands:
        click.echo("No plugin commands available")
        return

    for plugin_name, commands in all_commands.items():
        click.echo(f"\n{plugin_name}:")
        for cmd_name, cmd_info in commands.items():
            click.echo(f"  {cmd_name:<20} {cmd_info.get('help', '')}")


# Clean aliases for common operations (no duplicates)
@cli.command("sw")
@click.argument("name")
def sw(name: str):
    """Switch to a different context (alias for switch)"""
    ctx = click.get_current_context()
    ctx.invoke(switch, name=name)


@cli.command("ls")
@click.option("--all", "-a", is_flag=True, help="Show all contexts including completed")
@click.option("--state", "-s", help="Filter by state")
@click.option("--tag", help="Filter by tag")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["table", "simple", "json"]),
    default="table",
    help="Output format",
)
def ls(all: bool, state: str, tag: str, format: str):
    """List all contexts (alias for list)"""
    ctx = click.get_current_context()
    ctx.invoke(list_contexts, all=all, state=state, tag=tag, format=format)


@cli.command("st")
@click.argument("name", required=False)
def st(name: str):
    """Show context status (alias for status)"""
    ctx = click.get_current_context()
    ctx.invoke(status, name=name)


@cli.command("n")
@click.argument("text", nargs=-1, required=True)
@click.option("--tags", "-t", multiple=True, help="Note tags")
@click.option("--context", "-c", help="Context name (default: active)")
def n(text: tuple, tags: tuple, context: str):
    """Add a note to context (alias for note)"""
    ctx = click.get_current_context()
    ctx.invoke(add_note, text=text, tags=tags, context=context)


if __name__ == "__main__":
    cli()
