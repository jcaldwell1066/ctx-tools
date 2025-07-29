"""
CTX - A modular, extensible context management system
"""

__version__ = "2.0.0"
__author__ = "CTX Development Team"

from .core import ContextManager
from .models import Context, ContextState

__all__ = ["ContextManager", "Context", "ContextState"] 