"""
Utility modules for Adobe Audition for Windows toolkit
"""
from .detection import find_installation, is_installed, get_version
from .windows import get_registry_value, is_admin

__all__ = ["find_installation", "is_installed", "get_version", "get_registry_value", "is_admin"]
