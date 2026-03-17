import winreg
import subprocess
import ctypes
from typing import Optional, List

def get_registry_value(key: str, value: str) -> Optional[str]:
    """Retrieve a value from the Windows registry.

    Args:
        key (str): The registry key path.
        value (str): The value name.

    Returns:
        Optional[str]: The value associated with the name, or None if not found.
    """
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as registry_key:
            return winreg.QueryValueEx(registry_key, value)[0]
    except FileNotFoundError:
        print(f"Registry key {key} or value {value} not found.")
        return None
    except Exception as e:
        print(f"Error accessing registry: {e}")
        return None

def list_running_processes() -> List[str]:
    """List all currently running processes.

    Returns:
        List[str]: A list of names of running processes.
    """
    try:
        output = subprocess.check_output(["tasklist"], text=True)
        processes = [line.split()[0] for line in output.splitlines()[3:] if line]
        return processes
    except subprocess.CalledProcessError as e:
        print(f"Error listing processes: {e}")
        return []

def kill_process(name: str) -> bool:
    """Kill a running process by name.

    Args:
        name (str): The name of the process to kill.

    Returns:
        bool: True if the process was killed successfully, False otherwise.
    """
    try:
        subprocess.run(["taskkill", "/F", "/IM", name], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error killing process {name}: {e}")
        return False

def is_admin() -> bool:
    """Check if the current user has administrative privileges.

    Returns:
        bool: True if the user is an administrator, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

def run_as_admin(cmd: str) -> int:
    """Run a command as an administrator.

    Args:
        cmd (str): The command to run.

    Returns:
        int: The exit code of the command.
    """
    try:
        result = subprocess.run(["runas", "/user:Administrator", cmd], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error running command as admin: {e}")
        return e.returncode
