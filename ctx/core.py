"""
Core context manager implementation
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .models import Context, ContextState, ContextStack
from .storage import Storage, JsonStorage
from .plugins import PluginManager


class ContextManager:
    """Main context management class"""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize the context manager
        
        Args:
            storage_path: Path to storage directory (defaults to ~/.ctx)
        """
        self.storage_path = storage_path or Path.home() / ".ctx"
        self.storage_path.mkdir(exist_ok=True)
        
        # Initialize storage
        self.storage = JsonStorage(self.storage_path / "contexts.json")
        
        # Load data
        self.data = self.storage.load()
        self._ensure_data_structure()
        
        # Initialize plugin manager
        self.plugin_manager = PluginManager()
        
        # Context stack for push/pop operations
        self.stack = ContextStack.from_dict(self.data.get("stack", {}))
    
    def _ensure_data_structure(self):
        """Ensure data has required structure"""
        if "contexts" not in self.data:
            self.data["contexts"] = {}
        if "active" not in self.data:
            self.data["active"] = None
        if "stack" not in self.data:
            self.data["stack"] = {"stack": [], "max_size": 10}
    
    def _save(self):
        """Save current data to storage"""
        self.data["stack"] = self.stack.to_dict()
        self.storage.save(self.data)
    
    # Context lifecycle methods
    
    def create(self, name: str, description: str = "", 
               tags: List[str] = None, metadata: Dict[str, Any] = None) -> Context:
        """Create a new context
        
        Args:
            name: Context name (must be unique)
            description: Optional description
            tags: Optional list of tags
            metadata: Optional metadata dictionary
            
        Returns:
            Created context
            
        Raises:
            ValueError: If context already exists
        """
        if name in self.data["contexts"]:
            raise ValueError(f"Context '{name}' already exists")
        
        context = Context(
            name=name,
            description=description,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        # Allow plugins to initialize context
        self.plugin_manager.on_context_created(context)
        
        # Save context
        self.data["contexts"][name] = context.to_dict()
        self.data["active"] = name
        self._save()
        
        return context
    
    def get(self, name: str) -> Optional[Context]:
        """Get a context by name
        
        Args:
            name: Context name
            
        Returns:
            Context if found, None otherwise
        """
        if name not in self.data["contexts"]:
            return None
        
        context = Context.from_dict(self.data["contexts"][name])
        return context
    
    def list(self) -> List[Context]:
        """List all contexts
        
        Returns:
            List of all contexts
        """
        contexts = []
        for name in self.data["contexts"]:
            context = Context.from_dict(self.data["contexts"][name])
            contexts.append(context)
        return sorted(contexts, key=lambda c: c.updated_at, reverse=True)
    
    def switch(self, name: str) -> Context:
        """Switch to a different context
        
        Args:
            name: Context name to switch to
            
        Returns:
            The context switched to
            
        Raises:
            ValueError: If context doesn't exist
        """
        if name not in self.data["contexts"]:
            raise ValueError(f"Context '{name}' not found")
        
        # Save current context to stack if switching
        if self.data["active"] and self.data["active"] != name:
            self.stack.push(self.data["active"])
        
        self.data["active"] = name
        self._save()
        
        context = self.get(name)
        
        # Notify plugins
        self.plugin_manager.on_context_switched(context)
        
        return context
    
    def get_active(self) -> Optional[Context]:
        """Get the currently active context
        
        Returns:
            Active context or None
        """
        if not self.data["active"]:
            return None
        return self.get(self.data["active"])
    
    def delete(self, name: str):
        """Delete a context
        
        Args:
            name: Context name to delete
            
        Raises:
            ValueError: If context doesn't exist
        """
        if name not in self.data["contexts"]:
            raise ValueError(f"Context '{name}' not found")
        
        # Get context for plugin notification
        context = self.get(name)
        
        # Remove from data
        del self.data["contexts"][name]
        
        # Update active if needed
        if self.data["active"] == name:
            # Try to switch to previous context from stack
            prev = self.stack.pop()
            if prev and prev in self.data["contexts"]:
                self.data["active"] = prev
            else:
                # Otherwise pick first available
                self.data["active"] = next(iter(self.data["contexts"]), None)
        
        self._save()
        
        # Notify plugins
        self.plugin_manager.on_context_deleted(context)
    
    # Context state management
    
    def set_state(self, name: str, state: ContextState, custom_emoji: str = None):
        """Set context state
        
        Args:
            name: Context name
            state: New state
            custom_emoji: Optional custom emoji (for CUSTOM state)
        """
        context = self.get(name)
        if not context:
            raise ValueError(f"Context '{name}' not found")
        
        context.set_state(state, custom_emoji)
        self.data["contexts"][name] = context.to_dict()
        self._save()
        
        # Notify plugins
        self.plugin_manager.on_state_changed(context, state)
    
    # Note management
    
    def add_note(self, name: str, text: str, tags: List[str] = None):
        """Add a note to a context
        
        Args:
            name: Context name
            text: Note text
            tags: Optional note tags
        """
        context = self.get(name)
        if not context:
            raise ValueError(f"Context '{name}' not found")
        
        note = context.add_note(text, tags)
        self.data["contexts"][name] = context.to_dict()
        self._save()
        
        # Notify plugins
        self.plugin_manager.on_note_added(context, note)
    
    def clear_notes(self, name: str):
        """Clear all notes from a context
        
        Args:
            name: Context name
        """
        context = self.get(name)
        if not context:
            raise ValueError(f"Context '{name}' not found")
        
        context.notes.clear()
        context.updated_at = datetime.now()
        self.data["contexts"][name] = context.to_dict()
        self._save()
    
    # Stack operations
    
    def push(self, name: str):
        """Push current context and switch to new one
        
        Args:
            name: Context to switch to
        """
        self.switch(name)
    
    def pop(self) -> Optional[Context]:
        """Pop previous context from stack and switch to it
        
        Returns:
            Context switched to, or None if stack empty
        """
        prev = self.stack.pop()
        if prev and prev in self.data["contexts"]:
            return self.switch(prev)
        return None
    
    def peek_stack(self) -> List[str]:
        """Peek at the context stack
        
        Returns:
            List of context names in stack
        """
        return self.stack.stack.copy()
    
    # Search and filter
    
    def search(self, query: str) -> List[Context]:
        """Search contexts by name, description, or notes
        
        Args:
            query: Search query (case-insensitive)
            
        Returns:
            List of matching contexts
        """
        query_lower = query.lower()
        results = []
        
        for context in self.list():
            # Check name and description
            if (query_lower in context.name.lower() or 
                query_lower in context.description.lower()):
                results.append(context)
                continue
            
            # Check notes
            for note in context.notes:
                if query_lower in note.text.lower():
                    results.append(context)
                    break
            
            # Check tags
            for tag in context.tags:
                if query_lower in tag.lower():
                    results.append(context)
                    break
        
        return results
    
    def filter_by_state(self, state: ContextState) -> List[Context]:
        """Filter contexts by state
        
        Args:
            state: State to filter by
            
        Returns:
            List of contexts with given state
        """
        return [c for c in self.list() if c.state == state]
    
    def filter_by_tag(self, tag: str) -> List[Context]:
        """Filter contexts by tag
        
        Args:
            tag: Tag to filter by
            
        Returns:
            List of contexts with given tag
        """
        return [c for c in self.list() if tag in c.tags]
    
    # Plugin data management
    
    def set_plugin_data(self, context_name: str, plugin_name: str, data: Dict[str, Any]):
        """Set plugin-specific data for a context
        
        Args:
            context_name: Context name
            plugin_name: Plugin name
            data: Plugin data dictionary
        """
        context = self.get(context_name)
        if not context:
            raise ValueError(f"Context '{context_name}' not found")
        
        context.plugin_data[plugin_name] = data
        self.data["contexts"][context_name] = context.to_dict()
        self._save()
    
    def get_plugin_data(self, context_name: str, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Get plugin-specific data for a context
        
        Args:
            context_name: Context name
            plugin_name: Plugin name
            
        Returns:
            Plugin data or None
        """
        context = self.get(context_name)
        if not context:
            return None
        
        return context.plugin_data.get(plugin_name)
    
    # Import/Export
    
    def export_context(self, name: str) -> Dict[str, Any]:
        """Export a context as dictionary
        
        Args:
            name: Context name
            
        Returns:
            Context data dictionary
        """
        context = self.get(name)
        if not context:
            raise ValueError(f"Context '{name}' not found")
        
        return context.to_dict()
    
    def import_context(self, data: Dict[str, Any], overwrite: bool = False):
        """Import a context from dictionary
        
        Args:
            data: Context data dictionary
            overwrite: Whether to overwrite existing context
            
        Raises:
            ValueError: If context exists and overwrite=False
        """
        name = data["name"]
        
        if name in self.data["contexts"] and not overwrite:
            raise ValueError(f"Context '{name}' already exists")
        
        context = Context.from_dict(data)
        self.data["contexts"][name] = context.to_dict()
        self._save()
        
        # Notify plugins
        self.plugin_manager.on_context_imported(context) 