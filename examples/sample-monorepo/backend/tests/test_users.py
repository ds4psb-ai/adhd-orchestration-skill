"""Minimal test suite for the sample monorepo."""
import sys
from pathlib import Path

# Allow running from backend/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.user_service import get_user


def test_get_user_returns_dict():
    result = get_user(1)
    assert isinstance(result, dict)
    assert result["id"] == 1


def test_get_user_has_name():
    result = get_user(42)
    assert "name" in result
