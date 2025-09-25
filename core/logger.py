"""
Purpose: Configure and provide a rotating logger for the cron job script.

This module ensures professional logging practices by:
- Using RotatingFileHandler to avoid oversized log files
- Logging to both file and console
- Providing a central reusable logger across the project
"""

import logging
from logging.handlers import RotatingFileHandler
import os
import yaml


def get_logger(name: str = __name__, config_path: str = "config/config.yaml") -> logging.Logger:
    """
    Returns a logger instance configured with rotating file handler and console handler.

    Args:
        name (str): Name of the logger (default: __name__).
        config_path (str): Path to the YAML configuration file.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if logger already has handlers
    if logger.hasHandlers():
        return logger

    try:
        # Load logging configuration from YAML file
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        log_config = config.get("logging", {})

        log_level = getattr(logging, log_config.get("level", "INFO").upper())
        log_file = log_config.get("file", "logs/app.log")
        max_bytes = log_config.get("max_bytes", 1048576)
        backup_count = log_config.get("backup_count", 5)

        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Formatter for log messages
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Rotating file handler
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.setLevel(log_level)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    except FileNotFoundError:
        # Fallback basic logger if config file is missing
        logging.basicConfig(level=logging.INFO)
        logger.warning("Config file not found. Using default logging settings.")

    return logger
