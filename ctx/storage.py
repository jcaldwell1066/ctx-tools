"""
Storage backends for context data
"""

import json
import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional


class Storage(ABC):
    """Abstract base class for storage backends"""
    
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """Load data from storage"""
        pass
    
    @abstractmethod
    def save(self, data: Dict[str, Any]):
        """Save data to storage"""
        pass
    
    @abstractmethod
    def exists(self) -> bool:
        """Check if storage exists"""
        pass


class JsonStorage(Storage):
    """JSON file storage backend"""
    
    def __init__(self, path: Path):
        self.path = path
    
    def load(self) -> Dict[str, Any]:
        """Load data from JSON file"""
        if not self.exists():
            return {}
        
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save(self, data: Dict[str, Any]):
        """Save data to JSON file"""
        # Ensure parent directory exists
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def exists(self) -> bool:
        """Check if JSON file exists"""
        return self.path.exists()


class SqliteStorage(Storage):
    """SQLite storage backend"""
    
    def __init__(self, path: Path):
        self.path = path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS contexts (
                    name TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS update_timestamp
                AFTER UPDATE ON contexts
                BEGIN
                    UPDATE contexts SET updated_at = CURRENT_TIMESTAMP
                    WHERE name = NEW.name;
                END
            """)
    
    def load(self) -> Dict[str, Any]:
        """Load data from SQLite database"""
        data = {"contexts": {}, "active": None, "stack": {"stack": [], "max_size": 10}}
        
        with sqlite3.connect(self.path) as conn:
            # Load contexts
            cursor = conn.execute("SELECT name, data FROM contexts")
            for name, context_data in cursor.fetchall():
                data["contexts"][name] = json.loads(context_data)
            
            # Load metadata
            cursor = conn.execute("SELECT key, value FROM metadata")
            for key, value in cursor.fetchall():
                if key == "active":
                    data["active"] = value if value != "null" else None
                elif key == "stack":
                    data["stack"] = json.loads(value)
        
        return data
    
    def save(self, data: Dict[str, Any]):
        """Save data to SQLite database"""
        with sqlite3.connect(self.path) as conn:
            # Save contexts
            for name, context_data in data.get("contexts", {}).items():
                conn.execute(
                    "INSERT OR REPLACE INTO contexts (name, data) VALUES (?, ?)",
                    (name, json.dumps(context_data))
                )
            
            # Delete removed contexts
            existing_names = [row[0] for row in 
                            conn.execute("SELECT name FROM contexts").fetchall()]
            for name in existing_names:
                if name not in data.get("contexts", {}):
                    conn.execute("DELETE FROM contexts WHERE name = ?", (name,))
            
            # Save metadata
            conn.execute(
                "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
                ("active", data.get("active") if data.get("active") else "null")
            )
            
            conn.execute(
                "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
                ("stack", json.dumps(data.get("stack", {"stack": [], "max_size": 10})))
            )
            
            conn.commit()
    
    def exists(self) -> bool:
        """Check if database exists"""
        return self.path.exists() 