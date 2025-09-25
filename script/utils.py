"""
Purpose: Helper functions for cron job management.

Responsibilities:
- Validate cron expressions
- Check command existence in PATH
- Provide safe file writing with logging
- Professional docstrings and comments
"""

import logging
import shutil
from typing import Optional
from pathlib import Path
from crontab import CronTab


def validate_cron_expression(expression: str) -> bool:
    """
    Validate a cron schedule string.

    Args:
        expression (str): Cron schedule (e.g., '0 5 * * *')

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        test_cron = CronTab(expression)
        return True
    except (ValueError):
        return False


def command_exists(command: str) -> bool:
    """
    Check if a command exists in the system PATH.

    Args:
        command (str): Command to check (full path or command name)

    Returns:
        bool: True if command exists and executable, False otherwise
    """
    cmd_path = shutil.which(command)
    return cmd_path is not None


def safe_write_file(file_path: str, content: str, logger: Optional[logging.Logger] = None):
    """
    Write content to a file safely, creating directories if needed.

    Args:
        file_path (str): Path to the file
        content (str): Content to write
        logger (logging.Logger): Optional logger for logging info
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        if logger:
            logger.info("Successfully wrote to file: %s", file_path)
    except PermissionError:
        msg = f"Permission denied: Cannot write to file {file_path}"
        if logger:
            logger.error(msg)
        raise
    except Exception as e:
        msg = f"Unexpected error writing to file {file_path}: {e}"
        if logger:
            logger.exception(msg)
        raise
    