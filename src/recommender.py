import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its recommendation attributes."""

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's musical taste preferences."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Scores and ranks songs based on a user's preferences."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        score = 0.0

        # Genre is the strongest preference.
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0

        # Mood is also important.
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0

        # Reward songs whose energy is close to the user's target.
        energy_similarity = max(
            0.0,
            1.0 - abs(song.energy - user.target_energy)
        )
        score += energy_similarity

        # Small acoustic preference bonus.
        if user.likes_acoustic:
            score += song.acousticness
        else:
            score += 1.0 - song.acousticness

        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k songs ranked by preference score."""

        ranked_songs = sorted(
            self.songs,
            key=lambda song: self._score(user, song),
            reverse=True
        )

        return ranked_songs[:k]

    def explain_recommendation(
        self,
        user: UserProfile,
        song: Song
    ) -> str:
        """Explains why a song matches the user's preferences."""

        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append("genre matches your favorite")

        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append("mood matches your preference")

        energy_gap = abs(song.energy - user.target_energy)

        if energy_gap <= 0.2:
            reasons.append("energy is close to your target")

        if user.likes_acoustic and song.acousticness >= 0.5:
            reasons.append("matches your acoustic preference")

        if not user.likes_acoustic and song.acousticness < 0.5:
            reasons.append("matches your preference for less acoustic music")

        if not reasons:
            reasons.append("it is one of the closest overall matches")

        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Loads song data from a CSV file and converts numeric fields."""

    songs = []

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            song = dict(row)

            if "id" in song:
                song["id"] = int(song["id"])

            for field in [
                "energy",
                "tempo_bpm",
                "valence",
                "danceability",
                "acousticness"
            ]:
                if field in song:
                    song[field] = float(song[field])

            songs.append(song)

    return songs


def score_song(
    user_prefs: Dict,
    song: Dict
) -> Tuple[float, List[str]]:
    """Calculates a recommendation score and explanation reasons."""

    score = 0.0
    reasons = []

    favorite_genre = user_prefs.get("favorite_genre", "")
    favorite_mood = user_prefs.get("favorite_mood", "")
    target_energy = float(user_prefs.get("target_energy", 0.5))
    likes_acoustic = user_prefs.get("likes_acoustic", False)

    # Genre match
    if song["genre"].lower() == favorite_genre.lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match
    if song["mood"].lower() == favorite_mood.lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity
    energy_difference = abs(song["energy"] - target_energy)
    energy_score = max(0.0, 1.0 - energy_difference)

    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")

    # Acoustic preference
    acousticness = song.get("acousticness", 0.0)

    if likes_acoustic:
        acoustic_score = acousticness
        score += acoustic_score
        reasons.append(
            f"acoustic preference (+{acoustic_score:.2f})"
        )
    else:
        acoustic_score = 1.0 - acousticness
        score += acoustic_score
        reasons.append(
            f"less-acoustic preference (+{acoustic_score:.2f})"
        )

    return score, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Scores all songs and returns the top-k recommendations."""

    scored_songs = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)

        explanation = ", ".join(reasons)

        scored_songs.append(
            (song, score, explanation)
        )

    scored_songs.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return scored_songs[:k]