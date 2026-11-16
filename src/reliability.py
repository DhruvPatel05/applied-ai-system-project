"""Reliability and safety checks for the AI Music Recommendation System."""

from typing import Dict, List, Tuple

VALID_MOODS = {"happy", "sad", "calm", "intense", "moody", "energetic"}
VALID_GENRES = {
    "pop", "rock", "indie", "electronic", "synthwave",
    "hip-hop", "jazz", "classical", "r&b"
}

def validate_preferences(preferences: Dict) -> Tuple[bool, List[str]]:
    """
    Validate user preferences before sending them to the recommender.
    Returns whether the input is valid and a list of warnings.
    """
    warnings = []

    if not isinstance(preferences, dict):
        return False, ["Preferences must be provided as a dictionary."]

    mood = preferences.get("mood")
    genre = preferences.get("genre")

    if mood and str(mood).lower() not in VALID_MOODS:
        warnings.append(
            f"Unknown mood '{mood}'. Recommendation quality may be lower."
        )

    if genre and str(genre).lower() not in VALID_GENRES:
        warnings.append(
            f"Unknown genre '{genre}'. Recommendation quality may be lower."
        )

    energy = preferences.get("energy")

    if energy is not None:
        try:
            energy = float(energy)
            if not 0 <= energy <= 1:
                warnings.append(
                    "Energy must be between 0 and 1."
                )
        except (TypeError, ValueError):
            warnings.append("Energy must be numeric.")

    return len(warnings) == 0, warnings


def confidence_label(score: float) -> str:
    """Convert a recommendation score into an interpretable confidence label."""

    if score >= 2.5:
        return "High"
    elif score >= 1.5:
        return "Medium"
    return "Low"


def reliability_summary(recommendations: List) -> Dict:
    """Create a reliability summary for recommendation results."""

    if not recommendations:
        return {
            "status": "No recommendations",
            "confidence": "Low",
            "message": "The system could not generate reliable recommendations."
        }

    # Each recommendation is: (song, score, explanation)
    top_score = float(recommendations[0][1])

    return {
        "status": "Success",
        "confidence": confidence_label(top_score),
        "top_score": round(top_score, 2),
        "message": (
            "Confidence is estimated from the recommendation matching score. "
            "It is not a probability of user satisfaction."
        )
    }