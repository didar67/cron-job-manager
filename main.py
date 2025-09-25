"""
Purpose: Entry point for the Cron Job Manager CLI tool with logging.

Responsibilities:
- Initialize and parse CLI arguments
- Initialize JobManager with logger
- Execute add/list/remove cron job operations based on user input
- Log all operations and errors professionally
"""

import sys
from script.cli import parse_args
from core.logger import get_logger
from script.job import JobManager


def main():
    """
    Main entry point for the Cron Job Manager CLI tool.

    Workflow:
    1. Parse CLI arguments using parse_args()
    2. Initialize JobManager with logger
    3. Execute operation based on CLI flags:
        - Add job (--add)
        - Remove job (--remove)
        - List jobs (--list)
    4. Handle errors and missing required arguments gracefully
    5. Log all actions and errors to console and file
    """
    # Initialize logger
    logger = get_logger("CronJobManager")

    # Parse command-line arguments
    args = parse_args()
    
    # Initialize JobManager instance with logger
    manager = JobManager(logger=logger)

    try:
        # Add a new cron job
        if args.add:
            if not args.schedule or not args.command:
                logger.error("Missing required --schedule or --command for adding a job")
                sys.exit(1)

            logger.info(f"Adding new cron job: '{args.command}' with schedule '{args.schedule}'")
            manager.add_job(
                schedule=args.schedule,
                command=args.command,
                dry_run=args.dry_run,
                interactive=args.interactive,
                tag=args.tag
            )
            logger.info("Cron job added successfully.")

        # Remove an existing cron job
        elif args.remove:
            if not args.id:
                logger.error("Missing required --id for removing a job")
                sys.exit(1)

            logger.info(f"Removing cron job with ID: {args.id}")
            manager.remove_job(
                job_id=args.id,
                dry_run=args.dry_run
            )
            logger.info("Cron job removed successfully.")

        # List all existing cron jobs
        elif args.list:
            jobs = manager.list_jobs()
            if jobs:
                logger.info(f"Listing {len(jobs)} cron jobs")
                print("\nScheduled Cron Jobs:")
                for job in jobs:
                    job_id = job.get('comment', 'N/A')
                    print(f"[{job_id}] {job['schedule']} -> {job['command']}")
            else:
                logger.info("No cron jobs found")
                print("No cron jobs found.")

        # Handle unknown operation
        else:
            logger.error("Unknown operation. Use --add, --remove, or --list.")
            sys.exit(1)

    except Exception as e:
        logger.exception(f"Error executing operation: {e}")
        sys.exit(1)


# Entry point check
if __name__ == "__main__":
    main()
    