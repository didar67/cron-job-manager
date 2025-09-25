"""
Purpose: Command-line argument parsing for cron job management.

Responsibilities:
- Define and parse CLI arguments for cron job operations
- Provide dry-run, interactive, and tagging options
- Ensure user input is collected in a consistent and professional way
- Keep this file focused only on argument parsing (no execution logic)
"""

import argparse
import sys

def parse_args(args=None):
    """
    Parse CLI arguments for the cron job management script.

    Args:
        args (list, optional): List of arguments to parse. Defaults to sys.argv[1:].

    Returns:
        argparse.Namespace: Parsed command-line arguments containing user input.

    Example:
        >>> args = parse_args()
        >>> args.add
        True
        >>> args.schedule
        '0 5 * * *'
    """
    # Helpful examples shown at the bottom of --help output
    epilog_text = (
        "Example usage:\n"
        "  python main.py --add --schedule '0 5 * * *' --command '/path/to/script.sh' --tag 'backup'\n"
        "  python main.py --list\n"
        "  python main.py --remove --id <JOB_UUID>\n"
        "\n"
        "Additional options:\n"
        "  --dry-run       Simulate the operation without applying changes\n"
        "  --interactive   Run in interactive step-by-step input mode"
    )

    # Main parser with description and epilog for better CLI UX
    parser = argparse.ArgumentParser(
        description="Cron Job Management CLI",
        epilog=epilog_text,
        formatter_class=argparse.RawTextHelpFormatter
    )

    # User must choose exactly one action: add, list, or remove
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--add",
        action="store_true",
        help="Add a new cron job"
    )
    group.add_argument(
        "--list",
        action="store_true",
        help="List all cron jobs added by this script"
    )
    group.add_argument(
        "--remove",
        action="store_true",
        help="Remove a cron job by its UUID"
    )

    # Extra arguments (only required for specific actions)
    parser.add_argument(
        "--schedule",
        type=str,
        help="Cron schedule (e.g., '0 5 * * *') [Required for --add]"
    )
    parser.add_argument(
        "--command",
        type=str,
        help="Command to execute [Required for --add]"
    )
    parser.add_argument(
        "--id",
        type=str,
        help="UUID of the job to remove [Required for --remove]"
    )
    parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag/comment for the job"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the operation without applying changes"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode for step-by-step input"
    )

    # Parse the arguments and return them to the caller (main.py)
    parsed_args = parser.parse_args(args if args is not None else sys.argv[1:])
    return parsed_args
