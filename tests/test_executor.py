"""
Purpose: Unit tests for the Executor class (cron job management).

Covers:
- add
- list_all
- remove

Strategy:
- Mock python-crontab CronTab object
- Verify correct job creation, listing, and removal
- Ensure error handling (PermissionError, CronTabError, ValueError)
"""

import pytest
from unittest.mock import MagicMock, patch
from script.executor import CronExecutor
from crontab import CronTab


class TestCronExecutor:
    """Unit tests for Executor methods."""

    @patch("core.executor.CronTab")
    def test_add_job_success(self, mock_crontab):
        """Should add a job and return UUID successfully."""
        mock_cron = MagicMock()
        mock_crontab.return_value = mock_cron

        # Mock job object
        mock_job = MagicMock()
        mock_cron.new.return_value = mock_job

        executor = CronExecutor(logger=MagicMock())
        job_id = executor.add("0 * * * *", "echo 'hello'")

        assert job_id is not None
        mock_cron.new.assert_called_once_with(command="echo 'hello'")
        mock_job.setall.assert_called_once_with("0 * * * *")
        mock_cron.write.assert_called_once()

    @patch("core.executor.CronTab")
    def test_add_job_permission_error(self, mock_crontab):
        """Should raise PermissionError when crontab write fails."""
        mock_cron = MagicMock()
        mock_crontab.return_value = mock_cron
        mock_cron.new.side_effect = PermissionError("No permission")

        executor = CronExecutor(logger=MagicMock())
        with pytest.raises(PermissionError):
            executor.add("0 * * * *", "echo 'fail'")

    @patch("core.executor.CronTab")
    def test_list_all_with_tagged_jobs(self, mock_crontab):
        """Should list only jobs containing unique tag."""
        mock_cron = MagicMock()
        mock_crontab.return_value = mock_cron

        # Mock jobs
        job1 = MagicMock()
        job1.command = "echo 'job1'"
        job1.slices = "0 * * * *"
        job1.comment = "CRONJOB_SCRIPT:1234"

        job2 = MagicMock()
        job2.command = "echo 'job2'"
        job2.slices = "*/5 * * * *"
        job2.comment = ""

        mock_cron.__iter__.return_value = [job1, job2]

        executor = CronExecutor(logger=MagicMock())
        jobs = executor.list_all()

        assert len(jobs) == 1
        assert jobs[0]["command"] == "echo 'job1'"

    @patch("core.executor.CronTab")
    def test_remove_job_success(self, mock_crontab):
        """Should remove a job successfully when ID matches."""
        mock_cron = MagicMock()
        mock_crontab.return_value = mock_cron

        # Mock job with matching ID
        job = MagicMock()
        job.comment = "CRONJOB_SCRIPT:abcd1234"
        mock_cron.__iter__.return_value = [job]

        executor = CronExecutor(logger=MagicMock())
        result = executor.remove("abcd1234")

        assert result is True
        mock_cron.remove.assert_called_once_with(job)
        mock_cron.write.assert_called_once()

    @patch("core.executor.CronTab")
    def test_remove_job_not_found(self, mock_crontab):
        """Should raise ValueError if no job matches given ID."""
        mock_cron = MagicMock()
        mock_crontab.return_value = mock_cron
        mock_cron.__iter__.return_value = []

        executor = CronExecutor(logger=MagicMock())
        with pytest.raises(ValueError):
            executor.remove("nonexistent")
            