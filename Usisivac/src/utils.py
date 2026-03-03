import os
import logging
import sys
from pathlib import Path
from datetime import timedelta
from typing import Dict, Any, Optional
import subprocess

def setup_logging(level=logging.INFO):
    """Setup basic logging configuration."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )

def get_file_stats(file_path: Path) -> Dict[str, Any]:
    """Get basic file statistics."""
    stats = os.stat(file_path)
    return {
        "size": stats.st_size,
        "modified": stats.st_mtime,
        "created": stats.st_ctime
    }

def get_file_content(file_path: Path) -> str:
    """Read file content safely."""
    try:
        return file_path.read_text(encoding='utf-8')
    except Exception as e:
        return ""

def get_git_diff(target: str, git_ref: str) -> Dict[str, str]:
    """Get git diff for changed files (placeholder)."""
    # Simply listing files in the directory as a placeholder
    # Real git integration would use subprocess run
    return {}

def format_duration(duration: timedelta) -> str:
    """Format duration for human readability."""
    seconds = int(duration.total_seconds())
    if seconds < 60:
        return f"{seconds}s"
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}m {seconds}s"

import sys
