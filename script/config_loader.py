"""
Purpose: Load YAML configuration for Cron Job Manager.
"""

import yaml
import os
from typing import Optional

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.yaml")


def load_config(config_path: Optional[str] = None) -> dict:
    """
    Load configuration from YAML file.

    Args:
        config_path (str, optional): Path to YAML config. Defaults to None.

    Returns:
        dict: Configuration dictionary.

    Raises:
        FileNotFoundError: If YAML file does not exist.
        yaml.YAMLError: If YAML file is invalid.
    """
    path = config_path or CONFIG_FILE
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with open(path, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML: {e}")

    return config or {}
