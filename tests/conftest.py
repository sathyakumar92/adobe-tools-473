"""Pytest configuration for Adobe Audition for Windows toolkit tests"""
import pytest
from pathlib import Path

@pytest.fixture
def sample_dir(tmp_path):
    """Create a temporary directory with sample files"""
    return tmp_path

@pytest.fixture
def sample_file(tmp_path):
    """Create a sample test file"""
    f = tmp_path / "sample.txt"
    f.write_text("Sample content for testing")
    return f
