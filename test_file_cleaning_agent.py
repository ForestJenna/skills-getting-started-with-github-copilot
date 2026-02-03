"""
Tests for the File Cleaning Agent
"""

import pytest
import tempfile
import os
from pathlib import Path
from src.file_cleaning_agent import FileCleaningAgent


class TestFileCleaningAgent:
    """Test cases for the FileCleaningAgent class."""
    
    def test_initialization_default_patterns(self):
        """Test agent initializes with default patterns."""
        agent = FileCleaningAgent()
        assert agent.patterns == ["test"]
    
    def test_initialization_custom_patterns(self):
        """Test agent initializes with custom patterns."""
        agent = FileCleaningAgent(patterns=["temp", "backup"])
        assert agent.patterns == ["temp", "backup"]
    
    def test_scan_nonexistent_directory(self):
        """Test scanning a directory that doesn't exist."""
        agent = FileCleaningAgent()
        results = agent.scan_directory("/nonexistent/path")
        
        assert "error" in results
        assert "does not exist" in results["error"]
        assert results["suggestions"] == []
    
    def test_scan_file_instead_of_directory(self, tmp_path):
        """Test scanning a file instead of a directory."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        agent = FileCleaningAgent()
        results = agent.scan_directory(str(test_file))
        
        assert "error" in results
        assert "not a directory" in results["error"]
    
    def test_scan_empty_directory(self, tmp_path):
        """Test scanning an empty directory."""
        agent = FileCleaningAgent()
        results = agent.scan_directory(str(tmp_path))
        
        assert results["suggestions"] == []
        assert results["summary"]["total_files_scanned"] == 0
        assert results["summary"]["files_suggested"] == 0
    
    def test_scan_directory_with_test_files(self, tmp_path):
        """Test scanning a directory with files containing 'test' in the name."""
        # Create test files
        (tmp_path / "test.txt").write_text("content")
        (tmp_path / "test_file.py").write_text("content")
        (tmp_path / "normal_file.py").write_text("content")
        
        agent = FileCleaningAgent()
        results = agent.scan_directory(str(tmp_path))
        
        assert results["summary"]["total_files_scanned"] == 3
        assert results["summary"]["files_suggested"] == 2
        assert len(results["suggestions"]) == 2
        
        # Check that test files are suggested
        suggestions_str = " ".join(results["suggestions"])
        assert "test.txt" in suggestions_str
        assert "test_file.py" in suggestions_str
        assert "normal_file.py" not in suggestions_str
    
    def test_scan_directory_recursive(self, tmp_path):
        """Test recursive scanning of subdirectories."""
        # Create nested structure
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "test_top.txt").write_text("content")
        (subdir / "test_nested.txt").write_text("content")
        (tmp_path / "normal.txt").write_text("content")
        
        agent = FileCleaningAgent()
        results = agent.scan_directory(str(tmp_path), recursive=True)
        
        assert results["summary"]["total_files_scanned"] == 3
        assert results["summary"]["files_suggested"] == 2
        
        suggestions_str = " ".join(results["suggestions"])
        assert "test_top.txt" in suggestions_str
        assert "test_nested.txt" in suggestions_str
    
    def test_scan_directory_non_recursive(self, tmp_path):
        """Test non-recursive scanning."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "test_top.txt").write_text("content")
        (subdir / "test_nested.txt").write_text("content")
        
        agent = FileCleaningAgent()
        results = agent.scan_directory(str(tmp_path), recursive=False)
        
        assert results["summary"]["total_files_scanned"] == 1
        assert results["summary"]["files_suggested"] == 1
        assert "test_top.txt" in results["suggestions"][0]
    
    def test_custom_patterns(self, tmp_path):
        """Test scanning with custom patterns."""
        (tmp_path / "backup.txt").write_text("content")
        (tmp_path / "temp.log").write_text("content")
        (tmp_path / "normal.txt").write_text("content")
        
        agent = FileCleaningAgent(patterns=["backup", "temp"])
        results = agent.scan_directory(str(tmp_path))
        
        assert results["summary"]["files_suggested"] == 2
        suggestions_str = " ".join(results["suggestions"])
        assert "backup.txt" in suggestions_str
        assert "temp.log" in suggestions_str
        assert "normal.txt" not in suggestions_str
    
    def test_case_insensitive_matching(self, tmp_path):
        """Test that pattern matching is case-insensitive."""
        (tmp_path / "TEST.txt").write_text("content")
        (tmp_path / "Test.py").write_text("content")
        (tmp_path / "testing.log").write_text("content")
        
        agent = FileCleaningAgent(patterns=["test"])
        results = agent.scan_directory(str(tmp_path))
        
        assert results["summary"]["files_suggested"] == 3
    
    def test_format_report_with_suggestions(self, tmp_path):
        """Test report formatting with suggestions."""
        (tmp_path / "test.txt").write_text("content")
        
        agent = FileCleaningAgent()
        results = agent.scan_directory(str(tmp_path))
        report = agent.format_report(results)
        
        assert "FILE CLEANING AGENT REPORT" in report
        assert "Total files scanned: 1" in report
        assert "Files suggested for deletion: 1" in report
        assert "test.txt" in report
    
    def test_format_report_no_suggestions(self, tmp_path):
        """Test report formatting with no suggestions."""
        (tmp_path / "normal.txt").write_text("content")
        
        agent = FileCleaningAgent()
        results = agent.scan_directory(str(tmp_path))
        report = agent.format_report(results)
        
        assert "No files suggested for deletion" in report
    
    def test_format_report_with_error(self):
        """Test report formatting with error."""
        agent = FileCleaningAgent()
        results = agent.scan_directory("/nonexistent/path")
        report = agent.format_report(results)
        
        assert "Error:" in report
        assert "does not exist" in report
