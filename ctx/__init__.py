"""
CTX - Context Management System

A modular, extensible tool for managing development contexts.
"""

__version__ = "2.0.1"
__author__ = "CTX Development Team"

from .core import ContextManager
from .models import Context, ContextState

__all__ = ["ContextManager", "Context", "ContextState"] 