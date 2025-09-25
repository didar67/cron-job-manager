"""
Purpose: Unit tests for config_loader module.
"""

import pytest
import os
from script import config_loader


def test_load_config_success(tmp_path):
    """Should load valid YAML config successfully."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("logging:\n  level: INFO\n")
    
    config = config_loader.load_config(str(config_file))
    assert config["logging"]["level"] == "INFO"


def test_load_config_file_not_found():
    """Should raise FileNotFoundError for missing file."""
    with pytest.raises(FileNotFoundError):
        config_loader.load_config("nonexistent.yaml")


def test_load_config_invalid_yaml(tmp_path):
    """Should raise ValueError for invalid YAML."""
    invalid_file = tmp_path / "invalid.yaml"
    invalid_file.write_text("logging: [unclosed list")
    with pytest.raises(ValueError):
        config_loader.load_config(str(invalid_file))
        