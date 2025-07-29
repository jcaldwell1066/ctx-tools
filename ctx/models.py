"""
Core data models for the context management system
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
import json


class ContextState(Enum):
    """Standard context states with emoji representations"""
    ACTIVE = ("active", "🔵")
    IN_PROGRESS = ("in-progress", "💻") 
    ON_HOLD = ("on-hold", "⏸️")
    IN_REVIEW = ("in-review", "👀")
    BLOCKED = ("blocked", "🚫")
    PENDING = ("pending", "⏳")
    COMPLETED = ("completed", "✅")
    CANCELLED = ("cancelled", "❌")
    CUSTOM = ("custom", "🔸")
    
    def __init__(self, value, emoji):
        self._value_ = value
        self.emoji = emoji
    
    @classmethod
    def from_string(cls, value: str) -> 'ContextState':
        """Get state from string value"""
        for state in cls:
            if state.value == value:
                return state
        return cls.CUSTOM


@dataclass
class Note:
    """A timestamped note"""
    timestamp: datetime
    text: str
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "text": self.text,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Note':
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            text=data["text"],
            tags=data.get("tags", [])
        )


@dataclass
class Context:
    """Core context model"""
    name: str
    description: str = ""
    state: ContextState = ContextState.ACTIVE
    custom_emoji: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    notes: List[Note] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    # Plugin-specific data storage
    plugin_data: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    @property
    def emoji(self) -> str:
        """Get the emoji for current state"""
        if self.custom_emoji:
            return self.custom_emoji
        return self.state.emoji
    
    @property
    def note_count(self) -> int:
        """Get count of notes"""
        return len(self.notes)
    
    def add_note(self, text: str, tags: List[str] = None) -> Note:
        """Add a new note to the context"""
        note = Note(
            timestamp=datetime.now(),
            text=text,
            tags=tags or []
        )
        self.notes.append(note)
        self.updated_at = datetime.now()
        return note
    
    def get_recent_notes(self, count: int = 5) -> List[Note]:
        """Get the most recent notes"""
        return self.notes[-count:] if self.notes else []
    
    def set_state(self, state: ContextState, custom_emoji: str = None):
        """Update the context state"""
        self.state = state
        if custom_emoji:
            self.custom_emoji = custom_emoji
        elif state != ContextState.CUSTOM:
            self.custom_emoji = None
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "description": self.description,
            "state": self.state.value,
            "custom_emoji": self.custom_emoji,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "notes": [note.to_dict() for note in self.notes],
            "metadata": self.metadata,
            "tags": self.tags,
            "plugin_data": self.plugin_data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Context':
        """Create context from dictionary"""
        context = cls(
            name=data["name"],
            description=data.get("description", ""),
            state=ContextState.from_string(data.get("state", "active")),
            custom_emoji=data.get("custom_emoji"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            notes=[Note.from_dict(n) for n in data.get("notes", [])],
            metadata=data.get("metadata", {}),
            tags=data.get("tags", []),
            plugin_data=data.get("plugin_data", {})
        )
        return context


@dataclass 
class ContextStack:
    """Manages a stack of contexts for push/pop operations"""
    stack: List[str] = field(default_factory=list)
    max_size: int = 10
    
    def push(self, context_name: str):
        """Push a context onto the stack"""
        if context_name in self.stack:
            self.stack.remove(context_name)
        self.stack.append(context_name)
        if len(self.stack) > self.max_size:
            self.stack.pop(0)
    
    def pop(self) -> Optional[str]:
        """Pop the most recent context"""
        return self.stack.pop() if self.stack else None
    
    def peek(self) -> Optional[str]:
        """Peek at the most recent context without removing"""
        return self.stack[-1] if self.stack else None
    
    def clear(self):
        """Clear the stack"""
        self.stack.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "stack": self.stack,
            "max_size": self.max_size
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextStack':
        return cls(
            stack=data.get("stack", []),
            max_size=data.get("max_size", 10)
        ) 