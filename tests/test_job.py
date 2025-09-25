"""
Purpose: Unit tests for JobManager class in cron job script.

This module tests:
- Adding a cron job
- Listing cron jobs
- Removing a cron job
- Error handling for executor failures
All tests use unittest.mock to avoid modifying real system crontab.
"""

import unittest
from unittest.mock import patch, MagicMock
import logging
from script.job import JobManager


class TestJobManager(unittest.TestCase):
    """Unit tests for JobManager class."""

    def setUp(self):
        """Initialize JobManager with a dummy logger before each test."""
        self.logger = logging.getLogger("TestJobManager")
        if not self.logger.hasHandlers():
            self.logger.addHandler(logging.NullHandler())
        self.job_manager = JobManager(self.logger)

    @patch("script.job.CronExecutor.add")
    def test_add_job_dry_run(self, mock_add):
        """Test adding a job in dry-run mode does not call executor.add."""
        schedule = "0 * * * *"
        command = "echo 'hello'"
        self.job_manager.add_job(schedule, command, dry_run=True)
        mock_add.assert_not_called()  # dry-run should not call system

    @patch("script.job.CronExecutor.add")
    def test_add_job_real(self, mock_add):
        """Test adding a job in real mode calls executor.add once."""
        schedule = "0 * * * *"
        command = "echo 'hello'"
        self.job_manager.add_job(schedule, command, dry_run=False)
        mock_add.assert_called_once_with(schedule=schedule, command=command, comment=None)

    @patch("script.job.CronExecutor.add", side_effect=Exception("Add failed"))
    def test_add_job_error(self, mock_add):
        """Test adding a job handles executor errors gracefully."""
        schedule = "0 * * * *"
        command = "echo 'fail'"
        with self.assertRaises(Exception):
            self.job_manager.add_job(schedule, command, dry_run=False)

    @patch("script.job.CronExecutor.list_all")
    def test_list_jobs(self, mock_list):
        """Test listing jobs returns the mocked list."""
        mock_list.return_value = [{"id": 1, "schedule": "* * * * *", "command": "echo hi"}]
        jobs = self.job_manager.list_jobs()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["command"], "echo hi")

    @patch("script.job.CronExecutor.remove")
    def test_remove_job_dry_run(self, mock_remove):
        """Test removing a job in dry-run mode does not call executor.remove."""
        self.job_manager.remove_job("1", dry_run=True)
        mock_remove.assert_not_called()

    @patch("script.job.CronExecutor.remove")
    def test_remove_job_real(self, mock_remove):
        """Test removing a job in real mode calls executor.remove once."""
        self.job_manager.remove_job("1", dry_run=False)
        mock_remove.assert_called_once_with(job_id="1")

    @patch("script.job.CronExecutor.remove", side_effect=ValueError("Job not found"))
    def test_remove_job_error(self, mock_remove):
        """Test removing a non-existent job raises ValueError."""
        with self.assertRaises(ValueError):
            self.job_manager.remove_job("999", dry_run=False)


if __name__ == "__main__":
    unittest.main()
    