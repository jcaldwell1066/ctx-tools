"""
Unit tests for ctx-tools models (Context, Note, ContextState)
"""

import pytest
from datetime import datetime, timedelta
from ctx.models import Context, Note, ContextState, ContextStack


class TestContextState:
    """Tests for ContextState enum"""
    
    def test_state_values(self):
        """Test that all states have correct values and emojis"""
        assert ContextState.ACTIVE.value == "active"
        assert ContextState.ACTIVE.emoji == "🔵"
        
        assert ContextState.IN_PROGRESS.value == "in-progress"
        assert ContextState.IN_PROGRESS.emoji == "💻"
        
        assert ContextState.COMPLETED.value == "completed"
        assert ContextState.COMPLETED.emoji == "✅"
    
    def test_from_string(self):
        """Test state creation from string"""
        assert ContextState.from_string("active") == ContextState.ACTIVE
        assert ContextState.from_string("in-progress") == ContextState.IN_PROGRESS
        assert ContextState.from_string("invalid") == ContextState.CUSTOM


class TestNote:
    """Tests for Note model"""
    
    def test_note_creation(self):
        """Test basic note creation"""
        text = "This is a test note"
        tags = ["test", "important"]
        note = Note(timestamp=datetime.now(), text=text, tags=tags)
        
        assert note.text == text
        assert note.tags == tags
        assert isinstance(note.timestamp, datetime)
    
    def test_note_to_dict(self):
        """Test note serialization to dict"""
        timestamp = datetime.now()
        note = Note(timestamp=timestamp, text="Test note", tags=["test"])
        
        data = note.to_dict()
        assert data["text"] == "Test note"
        assert data["tags"] == ["test"]
        assert data["timestamp"] == timestamp.isoformat()
    
    def test_note_from_dict(self):
        """Test note deserialization from dict"""
        timestamp = datetime.now()
        data = {
            "timestamp": timestamp.isoformat(),
            "text": "Test note",
            "tags": ["test", "important"]
        }
        
        note = Note.from_dict(data)
        assert note.text == "Test note"
        assert note.tags == ["test", "important"]
        assert note.timestamp == timestamp


class TestContext:
    """Tests for Context model"""
    
    def test_context_creation(self):
        """Test basic context creation"""
        context = Context(
            name="test-context",
            description="A test context",
            tags=["test", "demo"]
        )
        
        assert context.name == "test-context"
        assert context.description == "A test context"
        assert context.state == ContextState.ACTIVE
        assert context.tags == ["test", "demo"]
        assert context.notes == []
        assert isinstance(context.created_at, datetime)
        assert isinstance(context.updated_at, datetime)
    
    def test_context_emoji(self):
        """Test context emoji property"""
        context = Context(name="test", state=ContextState.IN_PROGRESS)
        assert context.emoji == "💻"
        
        # Test custom emoji
        context.custom_emoji = "🎯"
        assert context.emoji == "🎯"
    
    def test_add_note(self):
        """Test adding notes to context"""
        context = Context(name="test")
        
        # Add first note
        note1 = context.add_note("First note", ["tag1"])
        assert len(context.notes) == 1
        assert note1.text == "First note"
        assert note1.tags == ["tag1"]
        
        # Add second note
        note2 = context.add_note("Second note")
        assert len(context.notes) == 2
        assert note2.text == "Second note"
        assert note2.tags == []
    
    def test_note_count(self):
        """Test note count property"""
        context = Context(name="test")
        assert context.note_count == 0
        
        context.add_note("Note 1")
        assert context.note_count == 1
        
        context.add_note("Note 2")
        assert context.note_count == 2
    
    def test_get_recent_notes(self):
        """Test getting recent notes"""
        context = Context(name="test")
        
        # Add multiple notes
        for i in range(10):
            context.add_note(f"Note {i+1}")
        
        # Get recent notes (default 5)
        recent = context.get_recent_notes()
        assert len(recent) == 5
        assert recent[-1].text == "Note 10"  # Most recent
        assert recent[0].text == "Note 6"    # 5th most recent
        
        # Get specific count
        recent_3 = context.get_recent_notes(3)
        assert len(recent_3) == 3
        assert recent_3[-1].text == "Note 10"
    
    def test_set_state(self):
        """Test state changes"""
        context = Context(name="test")
        original_updated = context.updated_at
        
        # Small delay to ensure timestamp change
        import time
        time.sleep(0.01)
        
        context.set_state(ContextState.IN_PROGRESS)
        assert context.state == ContextState.IN_PROGRESS
        assert context.updated_at > original_updated
        assert context.custom_emoji is None
        
        # Test custom state with emoji
        context.set_state(ContextState.CUSTOM, "🎯")
        assert context.state == ContextState.CUSTOM
        assert context.custom_emoji == "🎯"
        assert context.emoji == "🎯"
    
    def test_context_serialization(self):
        """Test context to_dict and from_dict"""
        original = Context(
            name="test-context",
            description="Test description",
            state=ContextState.IN_PROGRESS,
            tags=["test", "demo"]
        )
        original.add_note("Test note", ["important"])
        
        # Serialize
        data = original.to_dict()
        assert data["name"] == "test-context"
        assert data["description"] == "Test description"
        assert data["state"] == "in-progress"
        assert data["tags"] == ["test", "demo"]
        assert len(data["notes"]) == 1
        
        # Deserialize
        restored = Context.from_dict(data)
        assert restored.name == original.name
        assert restored.description == original.description
        assert restored.state == original.state
        assert restored.tags == original.tags
        assert len(restored.notes) == 1
        assert restored.notes[0].text == "Test note"


class TestContextStack:
    """Tests for ContextStack"""
    
    def test_stack_creation(self):
        """Test stack creation"""
        stack = ContextStack()
        assert stack.stack == []
        assert stack.max_size == 10
        
        stack_custom = ContextStack(max_size=5)
        assert stack_custom.max_size == 5
    
    def test_push_pop(self):
        """Test push and pop operations"""
        stack = ContextStack()
        
        # Push items
        stack.push("context-1")
        stack.push("context-2")
        assert stack.stack == ["context-1", "context-2"]
        
        # Pop items
        assert stack.pop() == "context-2"
        assert stack.pop() == "context-1"
        assert stack.pop() is None  # Empty stack
    
    def test_peek(self):
        """Test peek operation"""
        stack = ContextStack()
        assert stack.peek() is None
        
        stack.push("context-1")
        assert stack.peek() == "context-1"
        
        stack.push("context-2")
        assert stack.peek() == "context-2"
        
        # Peek doesn't modify stack
        assert len(stack.stack) == 2
    
    def test_max_size_enforcement(self):
        """Test that stack respects max_size"""
        stack = ContextStack(max_size=3)
        
        # Fill beyond max size
        for i in range(5):
            stack.push(f"context-{i}")
        
        # Should only keep last 3
        assert len(stack.stack) == 3
        assert stack.stack == ["context-2", "context-3", "context-4"]
    
    def test_duplicate_removal(self):
        """Test that pushing duplicate removes old entry"""
        stack = ContextStack()
        
        stack.push("context-1")
        stack.push("context-2")
        stack.push("context-1")  # Should move to end
        
        assert stack.stack == ["context-2", "context-1"]
    
    def test_stack_serialization(self):
        """Test stack to_dict and from_dict"""
        stack = ContextStack(max_size=5)
        stack.push("context-1")
        stack.push("context-2")
        
        data = stack.to_dict()
        assert data["stack"] == ["context-1", "context-2"]
        assert data["max_size"] == 5
        
        restored = ContextStack.from_dict(data)
        assert restored.stack == stack.stack
        assert restored.max_size == stack.max_size