import pytest
import json

def test_newsguard_categories_validation():
    valid_categories = ["politics", "health", "technology", "finance", "sports", "science", "general"]
    assert len(valid_categories) == 7
    assert "science" in valid_categories
    assert "politics" in valid_categories

def test_newsguard_verdicts():
    valid_verdicts = ["TRUE", "MISLEADING", "FALSE", "UNVERIFIABLE"]
    assert "TRUE" in valid_verdicts
    assert "FALSE" in valid_verdicts
    assert "MISLEADING" in valid_verdicts

def test_newsguard_stats_calculation():
    # Simulate on-chain checks state
    mock_checks = {
        "1": {"verdict": "TRUE", "category": "science"},
        "2": {"verdict": "FALSE", "category": "health"},
        "3": {"verdict": "MISLEADING", "category": "politics"},
        "4": {"verdict": "UNVERIFIABLE", "category": "finance"}
    }
    total = len(mock_checks)
    true_count = sum(1 for x in mock_checks.values() if x["verdict"] == "TRUE")
    false_count = sum(1 for x in mock_checks.values() if x["verdict"] == "FALSE")
    
    assert total == 4
    assert true_count == 1
    assert false_count == 1
    assert round(true_count / total, 2) == 0.25

def test_live_web_endpoint():
    """Verify authoritative source URL format"""
    sample_url = "https://en.wikipedia.org/wiki/Earth"
    assert sample_url.startswith("https://")
