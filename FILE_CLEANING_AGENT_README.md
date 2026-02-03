# File Cleaning Agent

A Python utility that scans directories and suggests files to delete based on configurable patterns.

## Features

- Scans directories for files matching specific patterns (e.g., "test", "temp", "backup")
- Supports recursive and non-recursive directory scanning
- Case-insensitive pattern matching
- Customizable deletion patterns
- Detailed reporting of scan results

## Installation

No additional dependencies required beyond Python standard library.

## Usage

### Command Line Interface

Basic usage with default pattern ("test"):

```bash
python src/file_cleaning_agent.py /path/to/directory
```

Scan with custom patterns:

```bash
python src/file_cleaning_agent.py /path/to/directory --patterns test temp backup
```

Scan without recursing into subdirectories:

```bash
python src/file_cleaning_agent.py /path/to/directory --no-recursive
```

### Python API

```python
from src.file_cleaning_agent import FileCleaningAgent

# Create agent with default pattern
agent = FileCleaningAgent()

# Or with custom patterns
agent = FileCleaningAgent(patterns=["test", "temp", "backup"])

# Scan directory
results = agent.scan_directory("/path/to/directory", recursive=True)

# Format and print report
report = agent.format_report(results)
print(report)
```

## Examples

### Example 1: Find all test files

```bash
python src/file_cleaning_agent.py /home/user/project
```

Output:
```
============================================================
FILE CLEANING AGENT REPORT
============================================================
Total files scanned: 50
Files suggested for deletion: 5

Suggested files to delete:
------------------------------------------------------------
  - /home/user/project/test_app.py
  - /home/user/project/test_utils.py
  - /home/user/project/pytest.ini
  - /home/user/project/tests/test_integration.py
  - /home/user/project/tests/test_unit.py
============================================================
```

### Example 2: Find temporary and backup files

```bash
python src/file_cleaning_agent.py /home/user/documents --patterns temp backup old
```

### Example 3: Scan only top-level directory

```bash
python src/file_cleaning_agent.py /home/user/project --no-recursive
```

## API Reference

### FileCleaningAgent Class

#### `__init__(patterns=None)`

Initialize the file cleaning agent.

**Parameters:**
- `patterns` (List[str], optional): List of patterns to match. Defaults to `["test"]`.

#### `scan_directory(path, recursive=True)`

Scan a directory and suggest files to delete.

**Parameters:**
- `path` (str): Directory path to scan
- `recursive` (bool): Whether to scan subdirectories. Defaults to `True`.

**Returns:**
- Dict with keys:
  - `suggestions` (List[str]): List of file paths suggested for deletion
  - `summary` (Dict): Contains `total_files_scanned` and `files_suggested` counts
  - `error` (str, optional): Error message if scan failed

#### `format_report(scan_results)`

Format scan results into a readable report.

**Parameters:**
- `scan_results` (Dict): Results from `scan_directory()` method

**Returns:**
- str: Formatted report

## Running Tests

```bash
python -m pytest test_file_cleaning_agent.py -v
```

## Notes

- Pattern matching is case-insensitive
- Patterns match against filenames only (not full paths)
- The agent only suggests deletions - it does not actually delete any files
- Always review suggestions before deleting any files

## Safety

This tool **only suggests** files for deletion. It does not modify or delete any files automatically. You must manually review and delete files based on the suggestions.
