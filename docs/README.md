# Cron Job Management Script

![CI](https://img.shields.io/badge/CI-Pending-blue)
![Test Coverage](https://img.shields.io/badge/Coverage-Pending-yellow)

## Overview

This project provides a **professional, recruiter-standard Python script** to manage cron jobs safely.
It supports adding, listing, and removing cron jobs with **UUID-based identification**, dry-run, interactive mode, and job tagging.

Key Features:

* Safe cron job management using `python-crontab`
* Unique job identification via UUID
* Dry-run mode for simulation
* Interactive mode for step-by-step input
* Logging and error handling
* Job tagging for better organization
* Professional CLI with help and epilog

## Project Structure

``` 
CronJobManager/
│
├── config/
│   └── config.yaml              # YAML configuration file
│
├── core/
│   ├── __init__.py              # Marks directory as a package
│   └── logger.py                # Centralized logging utility
│
├── script/
│   ├── __init__.py              # Marks directory as a package
│   ├── cli.py                   # CLI argument parser
│   ├── job.py                   # Cron job operations
│   ├── executor.py              # Safe command execution
│   ├── utils.py                 # Helper utilities (validation, file ops)
│   └── config_loader.py         # YAML config loader
│
├── tests/
│   ├── test_cli.py              # Unit tests for CLI
│   ├── test_job.py              # Unit tests for job operations
│   ├── test_executor.py         # Unit tests for executor
│   ├── test_utils.py            # Unit tests for utilities
│   ├── test_config_loader.py    # Unit tests for config loader
│   └── test_logger.py           # Unit tests for logger
│
├── docs/
│   └── README.md                # Project documentation
│
├── main.py                      # Entry point for CLI
├── requirements.txt             # Production dependencies
├── dev-requirements.txt         # Development dependencies
├── .pre-commit-config.yaml      # Pre-commit hooks configuration
├── .gitignore                   # Git ignored files/folders
└── LICENSE                      # Project license
```


## Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_folder>
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Add a Job

```bash
python main.py --add --schedule "0 5 * * *" --command "/path/to/script.sh" --tag "backup"
```

### Dry-Run Example

```bash
python main.py --add --schedule "0 5 * * *" --command "/path/to/script.sh" --dry-run
```

### Interactive Mode

```bash
python main.py --add --interactive
```

### List Jobs

```bash
python main.py --list
```

### Remove a Job

```bash
python main.py --remove --id <JOB_UUID>
```

## Configuration

Cron jobs can optionally have a tag/comment for easier management. UUID ensures unique identification even if cron lines change.

## Logging

All operations are logged using a professional logging system. Check `file_organizer.log` or configured log path for details.

## Contributing

* Follow PEP8 code style
* Add unit tests for any new functionality
* Maintain professional docstrings and comments

## Future Enhancements

* Email notifications on job success/failure
* CI/CD integration (GitHub Actions)
* Advanced job categorization via tags


### ✅ Key Highlights

1. **Badges included** → CI / Coverage placeholders
2. **Professional overview** → recruiter-friendly
3. **Installation & Usage** → step-by-step commands
4. **Dry-run & interactive mode explained**
5. **Logging & job tagging documented**
6. **Folder structure visualized with ASCII tree**
7. **Future enhancement section** → shows project maturity
