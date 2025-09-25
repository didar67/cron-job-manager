"""
Purpose: Unit tests for logging functionality.
"""

import logging
import pytest
from core.logger import get_logger


def test_logger_creation():
    """Logger should be created with correct name and level."""
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"
    # Check default level is INFO or lower
    assert logger.level <= logging.INFO

def test_logger_logging(capsys):
    """Test logger writes to console."""
    logger = get_logger("console_logger")
    logger.info("Test message")
    captured = capsys.readouterr()
    assert "Test message" in captured.out
    