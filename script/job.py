"""
Purpose: JobManager handles adding, listing, removing, and validating cron jobs.

Responsibilities:
- Interact with CronExecutor for safe cron management
- Provide robust validation for schedule and command
- Support dry-run mode
- Provide interactive mode for user input
- Maintain recruiter-standard logging and docstrings
"""

import logging
import os
from typing import Optional, List, Dict
from script.executor import CronExecutor
from script.utils import validate_cron_expression, command_exists


class JobManager:
    """
    High-level interface to manage cron jobs safely.
    """

    def __init__(self, logger: logging.Logger):
        """
        Initialize JobManager with a logger and CronExecutor.

        Args:
            logger (logging.Logger): Logger instance
        """
        self.logger = logger
        self.executor = CronExecutor(logger)

    def add_job(self, schedule: str, command: str, dry_run: bool = False, interactive: bool = False, tag: Optional[str] = None):
        """
        Add a new cron job with validation and optional dry-run mode.

        Args:
            schedule (str): Cron schedule string
            command (str): Command to execute
            dry_run (bool): If True, only simulate addition
            interactive (bool): If True, ask user for input step by step
            tag (str): Optional tag/comment for the job
        """
        try:
            if interactive:
                schedule = input("Enter cron schedule (e.g., '0 5 * * *'): ") or schedule
                command = input("Enter command to execute: ") or command
                tag = input("Enter optional tag/comment: ") or tag

            # Validate schedule and command
            if not validate_cron_expression(schedule):
                raise ValueError(f"Invalid cron schedule: {schedule}")
            if not command_exists(command):
                raise ValueError(f"Command does not exist or is not executable: {command}")

            if dry_run:
                self.logger.info("[Dry-Run] Would add job: %s -> %s", schedule, command)
                print(f"[Dry-Run] Job not actually added: {schedule} -> {command}")
                return

            job_id = self.executor.add(schedule=schedule, command=command, comment=tag)
            self.logger.info("Job added successfully with ID: %s", job_id)
            print(f"Job added successfully with ID: {job_id}")

        except Exception as e:
            self.logger.exception("Failed to add job: %s", e)
            print(f"Error adding job: {e}")

    def list_jobs(self) ->  List[Dict[str, str]] :
        """
        List all jobs added by this script.

        Returns:
            list[dict]: List of jobs (schedule, command, comment)
        """
        try:
            jobs = self.executor.list_all()
            if not jobs:
                print("No cron jobs found.")
            return jobs
        except Exception as e:
            self.logger.exception("Failed to list jobs: %s", e)
            print(f"Error listing jobs: {e}")
            return []

    def remove_job(self, job_id: str, dry_run: bool = False):
        """
        Remove a job by its UUID.

        Args:
            job_id (str): UUID of the job to remove
            dry_run (bool): If True, only simulate removal
        """
        try:
            if dry_run:
                self.logger.info("[Dry-Run] Would remove job ID: %s", job_id)
                print(f"[Dry-Run] Job not actually removed: {job_id}")
                return

            self.executor.remove(job_id=job_id)
            self.logger.info("Job removed successfully: %s", job_id)
            print(f"Job removed successfully: {job_id}")

        except Exception as e:
            self.logger.exception("Failed to remove job: %s", e)
            print(f"Error removing job: {e}")
            