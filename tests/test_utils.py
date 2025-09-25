"""
Purpose: Unit tests for utility functions used in the cron job script.

Covers:
- validate_cron_expression
- command_exists

Test Strategy:
- Valid and invalid cron expressions
- Command existence check using unittest.mock
"""

import pytest
from unittest.mock import patch
from script.utils import validate_cron_expression, command_exists


class TestValidateCronExpression:
    """Tests for validate_cron_expression."""

    def test_valid_expressions(self):
        """Should return True for valid cron expressions."""
        valid_expressions = [
            "0 * * * *",       # Run at minute 0 every hour
            "*/5 * * * *",     # Every 5 minutes
            "30 8 * * 1-5",    # 08:30 on weekdays
        ]
        for expr in valid_expressions:
            assert validate_cron_expression(expr) is True

    def test_invalid_expressions(self):
        """Should return False for invalid cron expressions."""
        invalid_expressions = [
            "100 * * * *",     # Invalid minute
            "abc * * * *",     # Non-numeric
            "* *",             # Too few fields
            "*/5 * * * * * *", # Too many fields
        ]
        for expr in invalid_expressions:
            assert validate_cron_expression(expr) is False


class TestCommandExists:
    """Tests for command_exists."""

    @patch("shutil.which", return_value="/bin/ls")
    def test_command_exists_true(self, mock_which):
        """Should return True if command is found."""
        assert command_exists("ls") is True
        mock_which.assert_called_once_with("ls")

    @patch("shutil.which", return_value=None)
    def test_command_exists_false(self, mock_which):
        """Should return False if command is not found."""
        assert command_exists("fakecmd") is False
        mock_which.assert_called_once_with("fakecmd")
        