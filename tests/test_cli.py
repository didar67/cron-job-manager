"""
Purpose: Unit tests for the CLI argument parser of the cron job script.
"""

import unittest
from script.cli import parse_args


class TestCLI(unittest.TestCase):
    """
    Unit tests for CLI parser.
    """

    def test_add_job_arguments(self):
        """Test parsing CLI arguments for adding a job."""
        args = parse_args([
            "--add",
            "--schedule", "0 5 * * *",
            "--command", "python3 backup.py"
        ])
        self.assertTrue(args.add)
        self.assertEqual(args.schedule, "0 5 * * *")
        self.assertEqual(args.command, "python3 backup.py")

    def test_remove_job_arguments(self):
        """Test parsing CLI arguments for removing a job."""
        args = parse_args([
            "--remove",
            "--id", "123"
        ])
        self.assertTrue(args.remove)
        self.assertEqual(args.id, "123")

    def test_list_jobs_argument(self):
        """Test parsing CLI arguments for listing jobs."""
        args = parse_args(["--list"])
        self.assertTrue(args.list)

    def test_dry_run_argument(self):
        """Test parsing with dry-run flag."""
        args = parse_args([
            "--add",
            "--schedule", "0 12 * * *",
            "--command", "echo 'Hello World'",
            "--dry-run"
        ])
        self.assertTrue(args.dry_run)

    def test_missing_required_args_for_add(self):
        """Test missing required arguments for add should raise SystemExit."""
        with self.assertRaises(SystemExit):
            parse_args(["--add"])


if __name__ == "__main__":
    unittest.main()
    