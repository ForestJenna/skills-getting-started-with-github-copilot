"""
File Cleaning Agent

A utility that scans a directory path and suggests files to delete based on 
configurable patterns. For example, it can identify files with "test" in their name.
"""

import os
from pathlib import Path
from typing import List, Dict


class FileCleaningAgent:
    """Agent that scans directories and suggests files to delete."""
    
    def __init__(self, patterns: List[str] = None):
        """
        Initialize the file cleaning agent.
        
        Args:
            patterns: List of patterns to match for deletion suggestions.
                     Defaults to ["test"] if not provided.
        """
        self.patterns = patterns if patterns is not None else ["test"]
    
    def scan_directory(self, path: str, recursive: bool = True) -> Dict[str, List[str]]:
        """
        Scan a directory and suggest files to delete.
        
        Args:
            path: The directory path to scan
            recursive: Whether to scan subdirectories recursively
            
        Returns:
            Dictionary with 'suggestions' and 'summary' keys containing
            file paths suggested for deletion and a summary count.
        """
        target_path = Path(path)
        
        if not target_path.exists():
            return {
                "error": f"Path does not exist: {path}",
                "suggestions": [],
                "summary": {"total_files_scanned": 0, "files_suggested": 0}
            }
        
        if not target_path.is_dir():
            return {
                "error": f"Path is not a directory: {path}",
                "suggestions": [],
                "summary": {"total_files_scanned": 0, "files_suggested": 0}
            }
        
        suggestions = []
        total_files = 0
        
        # Scan files
        if recursive:
            files = target_path.rglob("*")
        else:
            files = target_path.glob("*")
        
        for file_path in files:
            if file_path.is_file():
                total_files += 1
                if self._should_suggest_deletion(file_path):
                    suggestions.append(str(file_path))
        
        return {
            "suggestions": suggestions,
            "summary": {
                "total_files_scanned": total_files,
                "files_suggested": len(suggestions)
            }
        }
    
    def _should_suggest_deletion(self, file_path: Path) -> bool:
        """
        Determine if a file should be suggested for deletion.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if the file matches deletion patterns, False otherwise
        """
        file_name = file_path.name.lower()
        
        for pattern in self.patterns:
            pattern_lower = pattern.lower()
            if pattern_lower in file_name:
                return True
        
        return False
    
    def format_report(self, scan_results: Dict) -> str:
        """
        Format scan results into a readable report.
        
        Args:
            scan_results: Results from scan_directory method
            
        Returns:
            Formatted string report
        """
        if "error" in scan_results:
            return f"Error: {scan_results['error']}"
        
        report_lines = [
            "=" * 60,
            "FILE CLEANING AGENT REPORT",
            "=" * 60,
            f"Total files scanned: {scan_results['summary']['total_files_scanned']}",
            f"Files suggested for deletion: {scan_results['summary']['files_suggested']}",
            "",
        ]
        
        if scan_results['suggestions']:
            report_lines.append("Suggested files to delete:")
            report_lines.append("-" * 60)
            for suggestion in scan_results['suggestions']:
                report_lines.append(f"  - {suggestion}")
        else:
            report_lines.append("No files suggested for deletion.")
        
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)


def main():
    """CLI entry point for the file cleaning agent."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="File Cleaning Agent - Suggests files to delete based on patterns"
    )
    parser.add_argument(
        "path",
        help="Directory path to scan (absolute or relative path)"
    )
    parser.add_argument(
        "--patterns",
        nargs="+",
        default=["test"],
        help="Patterns to match for deletion suggestions (default: test)"
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Don't scan subdirectories recursively"
    )
    
    args = parser.parse_args()
    
    agent = FileCleaningAgent(patterns=args.patterns)
    results = agent.scan_directory(args.path, recursive=not args.no_recursive)
    report = agent.format_report(results)
    
    print(report)


if __name__ == "__main__":
    main()
