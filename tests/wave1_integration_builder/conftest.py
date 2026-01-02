"""
Pytest configuration for Wave 1 Integration Builder tests.
"""

import pytest
import sys
from pathlib import Path

# Add foreman directory to path
repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))
