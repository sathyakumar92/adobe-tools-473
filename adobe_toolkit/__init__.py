"""
Adobe Audition for Windows Toolkit - Python automation and utilities

A comprehensive toolkit for working with Adobe Audition for Windows files and automation.
"""
from .client import AdobeAuditionClient
from .processor import AdobeAuditionProcessor
from .metadata import AdobeAuditionMetadataReader
from .batch import BatchProcessor
from .exporter import DataExporter

__version__ = "0.1.0"
__author__ = "Open Source Community"

__all__ = [
    "AdobeAuditionClient",
    "AdobeAuditionProcessor",
    "AdobeAuditionMetadataReader",
    "BatchProcessor",
    "DataExporter",
]
