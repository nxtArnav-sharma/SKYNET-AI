"""
System tools — time, environment info, shell commands, etc.
"""

import datetime
import platform
import subprocess
import os

def register(mcp):

    @mcp.tool()
    def system_status() -> dict:
        """Return basic information about the host system."""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
            "time": datetime.datetime.now().isoformat(),
        }

    @mcp.tool()
    def execute_command(command: str) -> str:
        """Execute a shell command and return its output."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return str(e)

    @mcp.tool()
    def file_access(path: str, action: str, content: str = None) -> str:
        """Read or write a file. action must be 'read' or 'write'."""
        try:
            if action == 'read':
                with open(path, 'r') as f:
                    return f.read()
            elif action == 'write':
                with open(path, 'w') as f:
                    f.write(content)
                return f"File {path} written successfully."
        except Exception as e:
            return str(e)
