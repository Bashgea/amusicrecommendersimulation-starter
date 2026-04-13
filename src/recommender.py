from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """Dataclass holding a song's metadata and audio features used for scoring."""
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
    speechiness: float
    instrumentalness: float
    liveness: float

@dataclass
class UserProfile:
    """Dataclass storing a listener's taste preferences used to score songs."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """OOP interface for ranking songs against a UserProfile; used by the test suite."""

    def __init__(self, songs: List[Song]):
        """Stores the song catalog that will be ranked on every recommend() call."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k songs best matching the user's taste profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable string explaining why this song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv and returns a list of dicts with all numeric fields cast to float."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["energy"]           = float(row["energy"])
            row["tempo_bpm"]        = float(row["tempo_bpm"])
            row["valence"]          = float(row["valence"])
            row["danceability"]     = float(row["danceability"])
            row["acousticness"]     = float(row["acousticness"])
            row["speechiness"]      = float(row["speechiness"])
            row["instrumentalness"] = float(row["instrumentalness"])
            row["liveness"]         = float(row["liveness"])
            songs.append(row)
    return songs


def _score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song against the user profile and returns (total_score, reason_list)."""
    score = 0.0
    reasons = []

    # --- Categorical matches (binary: full points or nothing) ---
    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre match (+2.0)")
    else:
        reasons.append(f"genre mismatch - song={song['genre']}, wanted={user_prefs.get('genre')} (+0.0)")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.5
        reasons.append(f"mood match (+1.5)")
    else:
        reasons.append(f"mood mismatch - song={song['mood']}, wanted={user_prefs.get('mood')} (+0.0)")

    # --- Numeric similarity: weight * (1 - |target - actual|) ---
    # A perfect match scores the full weight; maximum distance scores 0.
    numeric_features = [
        ("target_energy",           "energy",           1.2),
        ("target_acousticness",     "acousticness",     1.0),
        ("target_valence",          "valence",          0.6),
        ("target_danceability",     "danceability",     0.6),
        ("target_instrumentalness", "instrumentalness", 0.5),
        ("target_speechiness",      "speechiness",      0.4),
        ("target_liveness",         "liveness",         0.3),
    ]

    for pref_key, song_key, weight in numeric_features:
        if pref_key in user_prefs:
            similarity = 1.0 - abs(user_prefs[pref_key] - song[song_key])
            points = weight * similarity
            score += points
            reasons.append(
                f"{song_key}: song={song[song_key]:.2f}, target={user_prefs[pref_key]:.2f}, "
                f"similarity={similarity:.2f} -> +{points:.2f} (weight={weight})"
            )

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Scores every song, sorts by score descending, and returns the top-k as (song, score, reasons) tuples."""
    # Score every song: produces [(score, reasons, song), ...]
    scored = [
        (score, reasons, song)
        for song in songs
        for score, reasons in [_score_song(user_prefs, song)]
    ]

    # Sort by score descending — sorted() returns a NEW list, songs is unchanged
    ranked = sorted(scored, key=lambda entry: entry[0], reverse=True)

    # Return the top k as (song, score, reasons) tuples
    return [(song, score, reasons) for score, reasons, song in ranked[:k]]
