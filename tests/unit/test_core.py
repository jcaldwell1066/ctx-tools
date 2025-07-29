"""
Unit tests for ctx-tools core ContextManager
"""

import pytest
from pathlib import Path
from typing import Any, Dict

from ctx.core import ContextManager
from ctx.models import ContextState, Context, Note
from ctx.plugins import Plugin


@pytest.mark.unit
class TestContextManager:
    """Tests for ContextManager"""
    
    def test_manager_initialization(self, temp_storage_dir):
        """Test ContextManager initialization"""
        manager = ContextManager(storage_path=temp_storage_dir)
        
        assert manager.storage_path == temp_storage_dir
        assert "contexts" in manager.data
        assert "active" in manager.data
        assert "stack" in manager.data
        assert manager.data["active"] is None
        assert manager.data["contexts"] == {}
    
    def test_create_context(self, ctx_manager):
        """Test context creation"""
        context = ctx_manager.create(
            name="test-context",
            description="Test description",
            tags=["test", "demo"]
        )
        
        assert context.name == "test-context"
        assert context.description == "Test description"
        assert context.tags == ["test", "demo"]
        assert context.state == ContextState.ACTIVE
        
        # Check it's stored in manager
        assert "test-context" in ctx_manager.data["contexts"]
        assert ctx_manager.data["active"] == "test-context"
    
    def test_create_duplicate_context(self, ctx_manager):
        """Test that creating duplicate context raises error"""
        ctx_manager.create("test-context")
        
        with pytest.raises(ValueError, match="Context 'test-context' already exists"):
            ctx_manager.create("test-context")
    
    def test_get_context(self, populated_manager):
        """Test getting context by name"""
        context = populated_manager.get("context-1")
        
        assert context is not None
        assert context.name == "context-1"
        assert context.description == "First test context"
        
        # Test non-existent context
        assert populated_manager.get("non-existent") is None
    
    def test_get_active_context(self, populated_manager):
        """Test getting active context"""
        # Initially context-2 should be active (last created)
        active = populated_manager.get_active()
        assert active is not None
        assert active.name == "completed-context"  # Last created
        
        # Switch active context
        populated_manager.switch("context-1")
        active = populated_manager.get_active()
        assert active.name == "context-1"
    
    def test_list_contexts(self, populated_manager):
        """Test listing all contexts"""
        contexts = populated_manager.list()
        
        assert len(contexts) == 3
        context_names = [c.name for c in contexts]
        assert "context-1" in context_names
        assert "context-2" in context_names
        assert "completed-context" in context_names
        
        # Should be sorted by updated_at (most recent first)
        # context-1 should be first because notes were added to it last
        assert contexts[0].name == "context-1"  # Most recently updated (notes added)
    
    def test_switch_context(self, populated_manager):
        """Test switching between contexts"""
        # Switch to context-1
        context = populated_manager.switch("context-1")
        assert context.name == "context-1"
        assert populated_manager.data["active"] == "context-1"
        
        # Switch to context-2
        context = populated_manager.switch("context-2")
        assert context.name == "context-2"
        assert populated_manager.data["active"] == "context-2"
        
        # Check context-1 was added to stack
        stack = populated_manager.peek_stack()
        assert "context-1" in stack
    
    def test_switch_nonexistent_context(self, ctx_manager):
        """Test switching to non-existent context raises error"""
        with pytest.raises(ValueError, match="Context 'non-existent' not found"):
            ctx_manager.switch("non-existent")
    
    def test_delete_context(self, populated_manager):
        """Test deleting a context"""
        # Verify context exists
        assert populated_manager.get("context-1") is not None
        
        # Delete it
        populated_manager.delete("context-1")
        
        # Verify it's gone
        assert populated_manager.get("context-1") is None
        assert "context-1" not in populated_manager.data["contexts"]
    
    def test_delete_active_context(self, populated_manager):
        """Test deleting the active context"""
        # Switch to context-1 and delete it
        populated_manager.switch("context-1")
        assert populated_manager.data["active"] == "context-1"
        
        populated_manager.delete("context-1")
        
        # Active context should be updated
        assert populated_manager.data["active"] != "context-1"
        assert populated_manager.data["active"] is not None  # Should pick another context
    
    def test_delete_nonexistent_context(self, ctx_manager):
        """Test deleting non-existent context raises error"""
        with pytest.raises(ValueError, match="Context 'non-existent' not found"):
            ctx_manager.delete("non-existent")
    
    def test_set_state(self, populated_manager):
        """Test setting context state"""
        populated_manager.set_state("context-1", ContextState.IN_PROGRESS)
        
        context = populated_manager.get("context-1")
        assert context.state == ContextState.IN_PROGRESS
        assert context.emoji == "💻"
    
    def test_set_state_with_custom_emoji(self, populated_manager):
        """Test setting custom state with emoji"""
        populated_manager.set_state("context-1", ContextState.CUSTOM, "🎯")
        
        context = populated_manager.get("context-1")
        assert context.state == ContextState.CUSTOM
        assert context.custom_emoji == "🎯"
        assert context.emoji == "🎯"
    
    def test_set_state_nonexistent_context(self, ctx_manager):
        """Test setting state on non-existent context raises error"""
        with pytest.raises(ValueError, match="Context 'non-existent' not found"):
            ctx_manager.set_state("non-existent", ContextState.ACTIVE)
    
    def test_add_note(self, populated_manager):
        """Test adding notes to context"""
        populated_manager.add_note("context-1", "New test note", ["important"])
        
        context = populated_manager.get("context-1")
        # Should have 3 notes now (2 from fixture + 1 new)
        assert len(context.notes) == 3
        assert context.notes[-1].text == "New test note"
        assert context.notes[-1].tags == ["important"]
    
    def test_add_note_nonexistent_context(self, ctx_manager):
        """Test adding note to non-existent context raises error"""
        with pytest.raises(ValueError, match="Context 'non-existent' not found"):
            ctx_manager.add_note("non-existent", "Test note")
    
    def test_clear_notes(self, populated_manager):
        """Test clearing all notes from context"""
        # Verify context has notes
        context = populated_manager.get("context-1")
        assert len(context.notes) > 0
        
        # Clear notes
        populated_manager.clear_notes("context-1")
        
        # Verify notes are cleared
        context = populated_manager.get("context-1")
        assert len(context.notes) == 0
    
    def test_clear_notes_nonexistent_context(self, ctx_manager):
        """Test clearing notes on non-existent context raises error"""
        with pytest.raises(ValueError, match="Context 'non-existent' not found"):
            ctx_manager.clear_notes("non-existent")
    
    def test_push_pop_stack(self, populated_manager):
        """Test push/pop context stack operations"""
        # Initially on completed-context
        assert populated_manager.data["active"] == "completed-context"
        
        # Push to context-1 (should add completed-context to stack)
        populated_manager.push("context-1")
        assert populated_manager.data["active"] == "context-1"
        
        stack = populated_manager.peek_stack()
        assert "completed-context" in stack
        
        # Pop back
        context = populated_manager.pop()
        assert context.name == "completed-context"
        assert populated_manager.data["active"] == "completed-context"
    
    def test_pop_empty_stack(self, ctx_manager):
        """Test popping from empty stack returns None"""
        result = ctx_manager.pop()
        assert result is None
    
    def test_search_contexts(self, populated_manager):
        """Test searching contexts"""
        # Search by name
        results = populated_manager.search("context-1")
        assert len(results) == 1
        assert results[0].name == "context-1"
        
        # Search by description
        results = populated_manager.search("First test")
        assert len(results) == 1
        assert results[0].name == "context-1"
        
        # Search by tag
        results = populated_manager.search("demo")
        assert len(results) == 1
        assert results[0].name == "context-2"
        
        # Search by note content
        results = populated_manager.search("First note")
        assert len(results) == 1
        assert results[0].name == "context-1"
        
        # Case insensitive search
        results = populated_manager.search("FIRST")
        assert len(results) >= 1
    
    def test_filter_by_state(self, populated_manager):
        """Test filtering contexts by state"""
        # Filter active contexts
        active_contexts = populated_manager.filter_by_state(ContextState.ACTIVE)
        assert len(active_contexts) == 2  # context-1 and context-2
        
        # Filter completed contexts
        completed_contexts = populated_manager.filter_by_state(ContextState.COMPLETED)
        assert len(completed_contexts) == 1
        assert completed_contexts[0].name == "completed-context"
    
    def test_filter_by_tag(self, populated_manager):
        """Test filtering contexts by tag"""
        # Filter by "test" tag
        test_contexts = populated_manager.filter_by_tag("test")
        assert len(test_contexts) == 2  # context-1 and context-2
        
        # Filter by "demo" tag
        demo_contexts = populated_manager.filter_by_tag("demo")
        assert len(demo_contexts) == 1
        assert demo_contexts[0].name == "context-2"
    
    def test_export_import_context(self, populated_manager, temp_storage_dir):
        """Test context export and import"""
        # Export context
        data = populated_manager.export_context("context-1")
        
        assert data["name"] == "context-1"
        assert data["description"] == "First test context"
        assert len(data["notes"]) == 2
        
        # Create new manager and import
        new_manager = ContextManager(storage_path=temp_storage_dir / "new")
        new_manager.import_context(data)
        
        imported_context = new_manager.get("context-1")
        assert imported_context is not None
        assert imported_context.name == "context-1"
        assert imported_context.description == "First test context"
        assert len(imported_context.notes) == 2
    
    def test_export_nonexistent_context(self, ctx_manager):
        """Test exporting non-existent context raises error"""
        with pytest.raises(ValueError, match="Context 'non-existent' not found"):
            ctx_manager.export_context("non-existent")
    
    def test_import_duplicate_context(self, populated_manager):
        """Test importing duplicate context without overwrite raises error"""
        data = populated_manager.export_context("context-1")
        
        with pytest.raises(ValueError, match="Context 'context-1' already exists"):
            populated_manager.import_context(data, overwrite=False)
        
        # Should work with overwrite=True
        populated_manager.import_context(data, overwrite=True)
    
    def test_plugin_data_management(self, populated_manager):
        """Test plugin-specific data storage"""
        # Set plugin data
        plugin_data = {"branch": "feature-123", "pr_number": "456"}
        populated_manager.set_plugin_data("context-1", "sprint", plugin_data)
        
        # Get plugin data
        retrieved_data = populated_manager.get_plugin_data("context-1", "sprint")
        assert retrieved_data == plugin_data
        
        # Test non-existent plugin data
        assert populated_manager.get_plugin_data("context-1", "nonexistent") is None
        assert populated_manager.get_plugin_data("nonexistent", "sprint") is None
    
    def test_data_persistence(self, temp_storage_dir):
        """Test that data persists across manager instances"""
        # Create manager and add context
        manager1 = ContextManager(storage_path=temp_storage_dir)
        manager1.create("persistent-context", "Test persistence")
        manager1.add_note("persistent-context", "Test note")
        
        # Create new manager instance with same storage
        manager2 = ContextManager(storage_path=temp_storage_dir)
        
        # Verify data persists
        context = manager2.get("persistent-context")
        assert context is not None
        assert context.name == "persistent-context"
        assert context.description == "Test persistence"
        assert len(context.notes) == 1
        assert context.notes[0].text == "Test note"

    def test_plugin_modifications_persist(self, temp_storage_dir):
        """Ensure plugin hook modifications are saved"""

        class ModifyPlugin(Plugin):
            name = "modify"

            def get_commands(self) -> Dict[str, Any]:
                return {}

            def on_state_changed(self, context: Context, new_state: ContextState):
                context.metadata["state_changed"] = True

            def on_note_added(self, context: Context, note: Note):
                context.metadata["last_note"] = note.text

            def on_context_switched(self, context: Context):
                context.metadata["switched"] = True

        manager = ContextManager(storage_path=temp_storage_dir)
        manager.plugin_manager.register(ModifyPlugin())

        manager.create("hook-test")
        manager.add_note("hook-test", "initial")
        manager.set_state("hook-test", ContextState.IN_PROGRESS)
        manager.switch("hook-test")

        new_mgr = ContextManager(storage_path=temp_storage_dir)
        ctx = new_mgr.get("hook-test")

        assert ctx.metadata.get("state_changed") is True
        assert ctx.metadata.get("last_note") == "initial"
        assert ctx.metadata.get("switched") is True
