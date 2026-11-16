"""
Command line runner for the Music Recommender Simulation.

Runs the recommender with multiple user profiles to evaluate
how different preferences affect recommendation rankings.
"""

from src.recommender import load_songs, recommend_songs

from src.reliability import validate_preferences, reliability_summary

def print_recommendations(profile_name, user_prefs, songs):
    """Print the top five recommendations for one user profile."""

    print("\n" + "=" * 65)
    print(f"PROFILE: {profile_name}")
    print("=" * 65)

    recommendations = recommend_songs(user_prefs, songs, k=5)
    # Validate user preferences before evaluating recommendations
    is_valid, warnings = validate_preferences(user_prefs)

    if warnings:
        print("\nReliability Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    # Evaluate recommendation reliability
    summary = reliability_summary(recommendations)

    print("\nRELIABILITY CHECK")
    print(f"Status: {summary['status']}")
    print(f"Confidence: {summary['confidence']}")

    if "top_score" in summary:
        print(f"Top recommendation score: {summary['top_score']}")

    print(f"Note: {summary['message']}")

    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec

        print(f"\n{index}. {song['title']} - {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"   Score: {score:.2f}")
        print(f"   Because: {explanation}")


def main():
    songs = load_songs("data/songs.csv")

    print(f"Loaded songs: {len(songs)}")

    profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.85,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.35,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.90,
            "likes_acoustic": False,
        },
    }

    for profile_name, preferences in profiles.items():
        print_recommendations(profile_name, preferences, songs)


if __name__ == "__main__":
    main()