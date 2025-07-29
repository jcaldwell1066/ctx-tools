"""
Plugin system for extending context functionality
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Type
import importlib
import pkgutil
from pathlib import Path

from .models import Context, ContextState, Note


class Plugin(ABC):
    """Base class for all plugins"""
    
    name: str = "base_plugin"
    description: str = "Base plugin class"
    version: str = "1.0.0"
    
    def __init__(self):
        """Initialize plugin"""
        pass
    
    @abstractmethod
    def get_commands(self) -> Dict[str, Any]:
        """Get plugin-specific commands
        
        Returns:
            Dictionary mapping command names to handler functions
        """
        pass
    
    def on_context_created(self, context: Context):
        """Called when a new context is created"""
        pass
    
    def on_context_switched(self, context: Context):
        """Called when switching to a context"""
        pass
    
    def on_context_deleted(self, context: Context):
        """Called when a context is deleted"""
        pass
    
    def on_context_imported(self, context: Context):
        """Called when a context is imported"""
        pass
    
    def on_state_changed(self, context: Context, new_state: ContextState):
        """Called when context state changes"""
        pass
    
    def on_note_added(self, context: Context, note: Note):
        """Called when a note is added"""
        pass
    
    def get_status_info(self, context: Context) -> Optional[str]:
        """Get plugin-specific status information
        
        Returns:
            Status string or None
        """
        return None
    
    def get_ps1_info(self, context: Context) -> Optional[str]:
        """Get plugin-specific PS1 prompt information
        
        Returns:
            PS1 string or None
        """
        return None


class PluginManager:
    """Manages plugin loading and lifecycle"""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self._load_builtin_plugins()
        self._load_external_plugins()
    
    def _load_builtin_plugins(self):
        """Load built-in plugins"""
        # We'll add built-in plugins later
        pass
    
    def _load_external_plugins(self):
        """Load external plugins from plugins directory"""
        plugin_dirs = [
            Path.home() / ".ctx" / "plugins",
            Path(__file__).parent.parent / "plugins"
        ]
        
        for plugin_dir in plugin_dirs:
            if not plugin_dir.exists():
                continue
            
            # Add plugin directory to path
            import sys
            if str(plugin_dir) not in sys.path:
                sys.path.insert(0, str(plugin_dir))
            
            # Load all Python modules in plugin directory
            for finder, name, ispkg in pkgutil.iter_modules([str(plugin_dir)]):
                try:
                    module = importlib.import_module(name)
                    
                    # Find Plugin subclasses in module
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            issubclass(attr, Plugin) and 
                            attr is not Plugin):
                            # Instantiate and register plugin
                            plugin = attr()
                            self.register(plugin)
                except Exception as e:
                    print(f"Failed to load plugin {name}: {e}")
    
    def register(self, plugin: Plugin):
        """Register a plugin
        
        Args:
            plugin: Plugin instance to register
        """
        self.plugins[plugin.name] = plugin
    
    def unregister(self, name: str):
        """Unregister a plugin
        
        Args:
            name: Plugin name to unregister
        """
        if name in self.plugins:
            del self.plugins[name]
    
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get a plugin by name
        
        Args:
            name: Plugin name
            
        Returns:
            Plugin instance or None
        """
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[Plugin]:
        """List all registered plugins
        
        Returns:
            List of plugin instances
        """
        return list(self.plugins.values())
    
    def get_all_commands(self) -> Dict[str, Dict[str, Any]]:
        """Get commands from all plugins
        
        Returns:
            Dictionary mapping plugin names to their commands
        """
        commands = {}
        for name, plugin in self.plugins.items():
            plugin_commands = plugin.get_commands()
            if plugin_commands:
                commands[name] = plugin_commands
        return commands
    
    # Event propagation methods
    
    def on_context_created(self, context: Context):
        """Notify all plugins of context creation"""
        for plugin in self.plugins.values():
            try:
                plugin.on_context_created(context)
            except Exception as e:
                print(f"Plugin {plugin.name} error in on_context_created: {e}")
    
    def on_context_switched(self, context: Context):
        """Notify all plugins of context switch"""
        for plugin in self.plugins.values():
            try:
                plugin.on_context_switched(context)
            except Exception as e:
                print(f"Plugin {plugin.name} error in on_context_switched: {e}")
    
    def on_context_deleted(self, context: Context):
        """Notify all plugins of context deletion"""
        for plugin in self.plugins.values():
            try:
                plugin.on_context_deleted(context)
            except Exception as e:
                print(f"Plugin {plugin.name} error in on_context_deleted: {e}")
    
    def on_context_imported(self, context: Context):
        """Notify all plugins of context import"""
        for plugin in self.plugins.values():
            try:
                plugin.on_context_imported(context)
            except Exception as e:
                print(f"Plugin {plugin.name} error in on_context_imported: {e}")
    
    def on_state_changed(self, context: Context, new_state: ContextState):
        """Notify all plugins of state change"""
        for plugin in self.plugins.values():
            try:
                plugin.on_state_changed(context, new_state)
            except Exception as e:
                print(f"Plugin {plugin.name} error in on_state_changed: {e}")
    
    def on_note_added(self, context: Context, note: Note):
        """Notify all plugins of note addition"""
        for plugin in self.plugins.values():
            try:
                plugin.on_note_added(context, note)
            except Exception as e:
                print(f"Plugin {plugin.name} error in on_note_added: {e}")
    
    def get_status_info(self, context: Context) -> List[str]:
        """Get status information from all plugins
        
        Returns:
            List of status strings from plugins
        """
        info = []
        for plugin in self.plugins.values():
            try:
                plugin_info = plugin.get_status_info(context)
                if plugin_info:
                    info.append(plugin_info)
            except Exception as e:
                print(f"Plugin {plugin.name} error in get_status_info: {e}")
        return info
    
    def get_ps1_info(self, context: Context) -> List[str]:
        """Get PS1 information from all plugins
        
        Returns:
            List of PS1 strings from plugins
        """
        info = []
        for plugin in self.plugins.values():
            try:
                plugin_info = plugin.get_ps1_info(context)
                if plugin_info:
                    info.append(plugin_info)
            except Exception as e:
                print(f"Plugin {plugin.name} error in get_ps1_info: {e}")
        return info 