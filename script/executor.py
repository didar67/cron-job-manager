"""
Purpose: Manage cron jobs safely using python-crontab.

Responsibilities:
- Add, remove, and list cron jobs safely
- Handle permission and subprocess errors gracefully
- Use UUID for unique job identification
- Log all operations with detailed messages
"""

import logging
import uuid
from typing import Optional, List, Dict
from crontab import CronTab
from pathlib import Path


class CronExecutor:
    """
    Handles direct interaction with system cron using python-crontab.
    """

    def __init__(self, logger: logging.Logger):
        """
        Initialize CronExecutor with a logger.

        Args:
            logger (logging.Logger): Logger instance for detailed logging
        """
        self.logger = logger
        try:
            self.cron = CronTab(user=True)  # current user
            
        except PermissionError:
            self.logger.error("Permission denied: Cannot access user crontab. Try running with sudo.")
            raise

    def add(self, schedule: str, command: str, comment: Optional[str] = None) -> str:
        """
        Add a new cron job with UUID comment.

        Args:
            schedule (str): Cron schedule string
            command (str): Command to execute
            comment (str): Optional custom comment/tag

        Returns:
            str: UUID of the job added

        Raises:
            ValueError: if schedule or command invalid
        """
        job_id = str(uuid.uuid4())
        job_comment = comment or f"cron_job_script_{job_id}"

        try:
            job = self.cron.new(command=command, comment=job_comment)
            job.setall(schedule)
            self.cron.write()
            self.logger.info("Cron job added successfully: %s -> %s", schedule, command)
            return job_id
        
        except ValueError as ve:
            self.logger.error("Failed to add job: Invalid schedule or command. %s", ve)
            raise
        except PermissionError:
            self.logger.error("Failed to add job: You do not have permission to modify crontab.")
            raise
        except Exception as e:
            self.logger.exception("Unexpected error while adding cron job: %s", e)
            raise

    def list_all(self) -> List[Dict[str, str]] :
        """
        List all cron jobs added by this script.

        Returns:
            list[dict]: List of job details (schedule, command, comment)
        """
        jobs = []
        try:
            for job in self.cron:
                if job.comment and "cron_job_script" in job.comment:
                    jobs.append({
                        "schedule": job.slices.render(),
                        "command": job.command,
                        "comment": job.comment
                    })
        
        except Exception as e:
            self.logger.exception("Unexpected error while listing jobs: %s", e)
        return jobs

    def remove(self, job_id: str):
        """
        Remove a cron job by its UUID (from comment).

        Args:
            job_id (str): UUID of the job to remove

        Raises:
            ValueError: if job_id not found
        """
        try:
            jobs_to_remove = [job for job in self.cron if job.comment and job_id in job.comment]
            if not jobs_to_remove:
                msg = f"No job found with ID {job_id}"
                self.logger.error(msg)
                raise ValueError(msg)
            for job in jobs_to_remove:
                self.cron.remove(job)
            self.cron.write()
            self.logger.info("Cron job(s) with ID %s removed successfully.", job_id)
        except PermissionError:
            self.logger.error("Failed to remove job: Permission denied.")
            raise
        except Exception as e:
            self.logger.exception("Unexpected error while removing cron job: %s", e)
            raise
        