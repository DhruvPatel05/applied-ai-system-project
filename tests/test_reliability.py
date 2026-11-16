from src.reliability import (
    validate_preferences,
    confidence_label,
    reliability_summary,
)


def test_valid_preferences():
    preferences = {
        "mood": "happy",
        "genre": "pop",
        "energy": 0.8,
    }

    is_valid, warnings = validate_preferences(preferences)

    assert is_valid is True
    assert warnings == []


def test_invalid_energy():
    preferences = {
        "mood": "happy",
        "genre": "pop",
        "energy": 1.5,
    }

    is_valid, warnings = validate_preferences(preferences)

    assert is_valid is False
    assert "Energy must be between 0 and 1." in warnings


def test_unknown_preferences():
    preferences = {
        "mood": "super-excited",
        "genre": "space-music",
        "energy": 0.5,
    }

    is_valid, warnings = validate_preferences(preferences)

    assert is_valid is False
    assert len(warnings) == 2


def test_confidence_levels():
    assert confidence_label(3.0) == "High"
    assert confidence_label(2.0) == "Medium"
    assert confidence_label(1.0) == "Low"


def test_reliability_summary():
    recommendations = [
        (
            {"title": "Test Song", "artist": "Test Artist"},
            4.25,
            "genre match",
        )
    ]

    summary = reliability_summary(recommendations)

    assert summary["status"] == "Success"
    assert summary["confidence"] == "High"
    assert summary["top_score"] == 4.25


def test_empty_recommendations():
    summary = reliability_summary([])

    assert summary["status"] == "No recommendations"
    assert summary["confidence"] == "Low"