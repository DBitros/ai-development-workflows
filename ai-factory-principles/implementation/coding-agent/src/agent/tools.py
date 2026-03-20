"""
Core tool implementations for the coding agent.

Provides file operations, shell execution, and search capabilities.
"""

import os
import subprocess
import signal
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional


class ToolRegistry:
    """Registry of available tools for the agent."""

    def __init__(self):
        self.tools = {}

    def register(self, name: str, description: str, parameters: Dict[str, Any], executor):
        """Register a tool."""
        self.tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "executor": executor
        }

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a tool by name."""
        return self.tools.get(name)

    def definitions(self) -> list:
        """Get all tool definitions for LLM."""
        return [
            {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"]
            }
            for t in self.tools.values()
        ]


# ============================================================================
# Core Tool Implementations
# ============================================================================

async def read_file_tool(args: Dict[str, Any], session: Any) -> str:
    """
    Read a file with line numbers.

    Args:
        file_path: Absolute path to file
        offset: Line number to start from (optional)
        limit: Max lines to read (optional, default 2000)
    """
    file_path = args["file_path"]
    offset = args.get("offset", 1)
    limit = args.get("limit", 2000)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Apply offset and limit
        start = max(0, offset - 1)
        end = min(len(lines), start + limit)
        selected_lines = lines[start:end]

        # Add line numbers
        numbered = []
        for i, line in enumerate(selected_lines, start=offset):
            numbered.append(f"{i:6}→{line.rstrip()}")

        return "\n".join(numbered)

    except FileNotFoundError:
        return f"Error: File not found: {file_path}"
    except PermissionError:
        return f"Error: Permission denied: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


async def write_file_tool(args: Dict[str, Any], session: Any) -> str:
    """
    Write content to a file.

    Args:
        file_path: Absolute path to file
        content: Content to write
    """
    file_path = args["file_path"]
    content = args["content"]

    try:
        # Create parent directories if needed
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        byte_count = len(content.encode('utf-8'))
        return f"Successfully wrote {byte_count} bytes to {file_path}"

    except PermissionError:
        return f"Error: Permission denied: {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


async def edit_file_tool(args: Dict[str, Any], session: Any) -> str:
    """
    Search and replace in a file (Anthropic native format).

    Args:
        file_path: Absolute path to file
        old_string: Exact text to find
        new_string: Replacement text
        replace_all: Replace all occurrences (default: false)
    """
    file_path = args["file_path"]
    old_string = args["old_string"]
    new_string = args["new_string"]
    replace_all = args.get("replace_all", False)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if old_string exists
        if old_string not in content:
            return f"Error: old_string not found in {file_path}"

        # Check uniqueness if not replace_all
        if not replace_all:
            count = content.count(old_string)
            if count > 1:
                return (
                    f"Error: old_string appears {count} times in {file_path}. "
                    f"Either provide more context to make it unique or set replace_all=true"
                )

        # Perform replacement
        if replace_all:
            new_content = content.replace(old_string, new_string)
            replaced_count = content.count(old_string)
        else:
            new_content = content.replace(old_string, new_string, 1)
            replaced_count = 1

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return f"Successfully replaced {replaced_count} occurrence(s) in {file_path}"

    except FileNotFoundError:
        return f"Error: File not found: {file_path}"
    except Exception as e:
        return f"Error editing file: {str(e)}"


async def shell_tool(args: Dict[str, Any], session: Any) -> str:
    """
    Execute a shell command.

    Args:
        command: Command to execute
        timeout_ms: Timeout in milliseconds (optional)
        description: Human-readable description (optional)
    """
    command = args["command"]
    timeout_ms = args.get("timeout_ms", session.config.default_command_timeout_ms)
    timeout_sec = min(timeout_ms / 1000, session.config.max_command_timeout_ms / 1000)

    try:
        # Execute command with timeout
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=session.working_directory,
            preexec_fn=os.setsid  # Create process group for clean killability
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout_sec
            )

            output = []
            if stdout:
                output.append(stdout.decode('utf-8', errors='replace'))
            if stderr:
                output.append(stderr.decode('utf-8', errors='replace'))

            combined = "\n".join(output)

            if process.returncode == 0:
                return combined or "[Command completed successfully with no output]"
            else:
                return f"[Exit code {process.returncode}]\n{combined}"

        except asyncio.TimeoutError:
            # Kill process group
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                await asyncio.sleep(2)
                if process.returncode is None:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except:
                pass

            return (
                f"[ERROR: Command timed out after {timeout_sec}s. "
                "Partial output is shown above. "
                "You can retry with a longer timeout by setting timeout_ms parameter.]"
            )

    except Exception as e:
        return f"Error executing command: {str(e)}"


async def grep_tool(args: Dict[str, Any], session: Any) -> str:
    """
    Search file contents by pattern.

    Args:
        pattern: Regex pattern to search for
        path: Directory or file to search (optional)
        case_insensitive: Case-insensitive search (optional)
        max_results: Max results to return (optional, default 100)
    """
    pattern = args["pattern"]
    path = args.get("path", session.working_directory)
    case_insensitive = args.get("case_insensitive", False)
    max_results = args.get("max_results", 100)

    # Build grep command
    cmd_parts = ["grep", "-r", "-n"]  # Recursive, line numbers
    if case_insensitive:
        cmd_parts.append("-i")
    cmd_parts.extend([pattern, path])

    cmd = " ".join(cmd_parts)

    # Execute using shell tool
    result = await shell_tool({"command": cmd}, session)

    # Limit results
    lines = result.split("\n")
    if len(lines) > max_results:
        limited = lines[:max_results]
        omitted = len(lines) - max_results
        limited.append(f"[... {omitted} more matches omitted ...]")
        return "\n".join(limited)

    return result


async def glob_tool(args: Dict[str, Any], session: Any) -> str:
    """
    Find files matching a glob pattern.

    Args:
        pattern: Glob pattern (e.g., "**/*.py")
        path: Base directory (optional)
    """
    pattern = args["pattern"]
    path = args.get("path", session.working_directory)

    # Use find command
    # TODO: Implement proper glob matching
    if "**" in pattern:
        # Recursive search
        ext = pattern.split("**/*.")[-1] if "**/*." in pattern else "*"
        cmd = f"find {path} -name '*.{ext}' -type f"
    else:
        cmd = f"find {path} -name '{pattern}' -type f"

    result = await shell_tool({"command": cmd}, session)
    return result


def create_standard_tools() -> ToolRegistry:
    """
    Create standard tool registry with core developer tools.

    Returns:
        ToolRegistry with read_file, write_file, edit_file, shell, grep, glob
    """
    registry = ToolRegistry()

    # read_file
    registry.register(
        name="read_file",
        description="Read a file from the filesystem with line numbers",
        parameters={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute path to the file"
                },
                "offset": {
                    "type": "integer",
                    "description": "Line number to start from (1-based)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Max lines to read (default: 2000)"
                }
            },
            "required": ["file_path"]
        },
        executor=read_file_tool
    )

    # write_file
    registry.register(
        name="write_file",
        description="Write content to a file, creating it if needed",
        parameters={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute path to the file"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write"
                }
            },
            "required": ["file_path", "content"]
        },
        executor=write_file_tool
    )

    # edit_file
    registry.register(
        name="edit_file",
        description="Replace exact string in a file (Anthropic native format)",
        parameters={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute path to the file"
                },
                "old_string": {
                    "type": "string",
                    "description": "Exact text to find"
                },
                "new_string": {
                    "type": "string",
                    "description": "Replacement text"
                },
                "replace_all": {
                    "type": "boolean",
                    "description": "Replace all occurrences (default: false)"
                }
            },
            "required": ["file_path", "old_string", "new_string"]
        },
        executor=edit_file_tool
    )

    # shell
    registry.register(
        name="shell",
        description="Execute a shell command with timeout",
        parameters={
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Command to execute"
                },
                "timeout_ms": {
                    "type": "integer",
                    "description": "Timeout in milliseconds"
                },
                "description": {
                    "type": "string",
                    "description": "Human-readable description"
                }
            },
            "required": ["command"]
        },
        executor=shell_tool
    )

    # grep
    registry.register(
        name="grep",
        description="Search file contents by regex pattern",
        parameters={
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Regex pattern to search for"
                },
                "path": {
                    "type": "string",
                    "description": "Directory or file to search"
                },
                "case_insensitive": {
                    "type": "boolean",
                    "description": "Case-insensitive search"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Max results to return (default: 100)"
                }
            },
            "required": ["pattern"]
        },
        executor=grep_tool
    )

    # glob
    registry.register(
        name="glob",
        description="Find files matching a glob pattern",
        parameters={
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern (e.g., '**/*.py')"
                },
                "path": {
                    "type": "string",
                    "description": "Base directory to search"
                }
            },
            "required": ["pattern"]
        },
        executor=glob_tool
    )

    return registry
