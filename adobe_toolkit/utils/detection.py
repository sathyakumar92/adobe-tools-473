from pathlib import Path
from typing import Optional
import subprocess
import os

def find_installation() -> Optional[Path]:
    """Find the installation directory of Adobe Audition on Windows.

    Returns:
        Optional[Path]: The path to the Adobe Audition installation directory, or None if not found.
    """
    common_paths = [
        Path("C:/Program Files/Adobe/Adobe Audition 2023"),
        Path("C:/Program Files (x86)/Adobe/Adobe Audition 2023"),
        Path("C:/Program Files/Adobe/Adobe Audition 2022"),
        Path("C:/Program Files (x86)/Adobe/Adobe Audition 2022"),
        Path("C:/Program Files/Adobe/Adobe Audition 2021"),
        Path("C:/Program Files (x86)/Adobe/Adobe Audition 2021")
    ]
    
    for path in common_paths:
        if path.exists() and path.is_dir():
            return path
    return None

def get_version() -> Optional[str]:
    """Get the version of Adobe Audition installed.

    Returns:
        Optional[str]: The version of Adobe Audition, or None if not found.
    """
    installation_path = find_installation()
    if installation_path:
        version_file = installation_path / "version.txt"
        if version_file.exists():
            with version_file.open('r') as file:
                return file.readline().strip()
    return None

def is_installed() -> bool:
    """Check if Adobe Audition is installed on the system.

    Returns:
        bool: True if Adobe Audition is installed, False otherwise.
    """
    return find_installation() is not None

def get_executable_path() -> Optional[Path]:
    """Get the path to the Adobe Audition executable.

    Returns:
        Optional[Path]: The path to the Adobe Audition executable, or None if not found.
    """
    installation_path = find_installation()
    if installation_path:
        executable_path = installation_path / "Audition.exe"
        if executable_path.exists():
            return executable_path
    return None

if __name__ == "__main__":
    if is_installed():
        print("Adobe Audition is installed.")
        print(f"Version: {get_version()}")
        print(f"Executable Path: {get_executable_path()}")
    else:
        print("Adobe Audition is not installed.")
