"""
Output formatters for the CLI
"""

import json
from typing import List, Optional, Any
from datetime import datetime
from textwrap import dedent

from .models import Context, Note


def format_context_list(contexts: List[Context], active: Optional[str], 
                       format: str = 'table') -> str:
    """Format a list of contexts for display"""
    
    if format == 'json':
        data = []
        for ctx in contexts:
            data.append({
                'name': ctx.name,
                'state': ctx.state.value,
                'emoji': ctx.emoji,
                'updated': ctx.updated_at.isoformat(),
                'notes': ctx.note_count,
                'active': ctx.name == active
            })
        return json.dumps(data, indent=2)
    
    elif format == 'simple':
        lines = []
        for ctx in contexts:
            marker = " ← active" if ctx.name == active else ""
            lines.append(f"{ctx.name} {ctx.emoji}{marker}")
        return "\n".join(lines)
    
    else:  # table format
        # Calculate column widths
        name_width = max(len(ctx.name) for ctx in contexts) if contexts else 4
        name_width = max(name_width, 4)  # Minimum width
        
        # Header
        lines = [
            f"{'NAME':<{name_width}} {'STATE':<12} {'UPDATED':<20} {'NOTES':<7}",
            "-" * (name_width + 12 + 20 + 7 + 3)
        ]
        
        # Rows
        for ctx in contexts:
            marker = " ← active" if ctx.name == active else ""
            updated = ctx.updated_at.strftime("%Y-%m-%d %H:%M")
            state_display = f"{ctx.emoji} {ctx.state.value}"
            
            lines.append(
                f"{ctx.name:<{name_width}} {state_display:<12} "
                f"{updated:<20} {ctx.note_count:<7}{marker}"
            )
        
        return "\n".join(lines)


def format_context_status(context: Context, is_active: bool = False,
                         verbose: bool = False, 
                         plugin_info: List[str] = None) -> str:
    """Format detailed context status"""
    
    lines = []
    
    # Header
    active_marker = " (active)" if is_active else ""
    lines.append(f"Context: {context.name} {context.emoji}{active_marker}")
    
    if context.description:
        lines.append(f"Description: {context.description}")
    
    lines.append(f"State: {context.state.value}")
    lines.append(f"Created: {context.created_at.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Updated: {context.updated_at.strftime('%Y-%m-%d %H:%M')}")
    
    if context.tags:
        lines.append(f"Tags: {', '.join(context.tags)}")
    
    lines.append(f"Notes: {context.note_count}")
    
    # Plugin information
    if plugin_info:
        lines.append("")
        lines.append("Plugin Information:")
        for info in plugin_info:
            lines.append(f"  {info}")
    
    # Recent notes
    if context.notes:
        lines.append("")
        lines.append("Recent notes:")
        recent = context.get_recent_notes(3)
        for note in recent:
            note_time = note.timestamp.strftime("%H:%M")
            lines.append(f"  [{note_time}] {note.text}")
            if note.tags and verbose:
                lines.append(f"           Tags: {', '.join(note.tags)}")
    
    # Metadata in verbose mode
    if verbose and context.metadata:
        lines.append("")
        lines.append("Metadata:")
        for key, value in context.metadata.items():
            lines.append(f"  {key}: {value}")
    
    # Plugin data in verbose mode
    if verbose and context.plugin_data:
        lines.append("")
        lines.append("Plugin Data:")
        for plugin, data in context.plugin_data.items():
            lines.append(f"  {plugin}:")
            if isinstance(data, dict):
                for key, value in data.items():
                    lines.append(f"    {key}: {value}")
            else:
                lines.append(f"    {data}")
    
    return "\n".join(lines)


def format_notes(notes: List[Note], context_name: str) -> str:
    """Format a list of notes"""
    
    if not notes:
        return f"No notes in context '{context_name}'"
    
    lines = [f"Notes for '{context_name}':", "-" * 50]
    
    for note in notes:
        timestamp = note.timestamp.strftime("%Y-%m-%d %H:%M")
        lines.append(f"[{timestamp}] {note.text}")
        
        if note.tags:
            lines.append(f"  Tags: {', '.join(note.tags)}")
        
        lines.append("")  # Empty line between notes
    
    return "\n".join(lines)


def format_stack(stack: List[str]) -> str:
    """Format the context stack"""
    
    lines = ["Context Stack:", "-" * 20]
    
    for i, name in enumerate(reversed(stack)):
        position = len(stack) - i
        marker = "← top" if i == 0 else ""
        lines.append(f"{position}. {name} {marker}")
    
    return "\n".join(lines)


def format_search_results(results: List[Context], query: str, 
                         format: str = 'simple') -> str:
    """Format search results"""
    
    lines = [f"Found {len(results)} contexts matching '{query}':", ""]
    
    if format == 'detailed':
        for ctx in results:
            lines.append(f"{ctx.name} {ctx.emoji}")
            
            if ctx.description and query.lower() in ctx.description.lower():
                lines.append(f"  Description: {ctx.description}")
            
            # Show matching notes
            matching_notes = []
            for note in ctx.notes:
                if query.lower() in note.text.lower():
                    matching_notes.append(note)
            
            if matching_notes:
                lines.append("  Matching notes:")
                for note in matching_notes[:2]:  # Show max 2 notes
                    note_time = note.timestamp.strftime("%H:%M")
                    # Highlight the query in note text
                    text = note.text
                    if len(text) > 80:
                        # Find position of query and show context
                        pos = text.lower().find(query.lower())
                        start = max(0, pos - 20)
                        end = min(len(text), pos + len(query) + 60)
                        text = "..." + text[start:end] + "..."
                    
                    lines.append(f"    [{note_time}] {text}")
            
            lines.append("")  # Empty line between results
    
    else:  # simple format
        for ctx in results:
            updated = ctx.updated_at.strftime("%Y-%m-%d")
            lines.append(f"  {ctx.name:<30} {ctx.emoji} {updated}")
    
    return "\n".join(lines)


def format_plugin_list(plugins: List[Any]) -> str:
    """Format a list of plugins"""
    
    if not plugins:
        return "No plugins installed"
    
    lines = ["Installed Plugins:", "-" * 40]
    
    for plugin in plugins:
        lines.append(f"{plugin.name:<20} v{plugin.version:<10}")
        lines.append(f"  {plugin.description}")
        lines.append("")
    
    return "\n".join(lines) 