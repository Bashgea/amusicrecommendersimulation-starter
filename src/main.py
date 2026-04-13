"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "energetic",
        "target_energy": 0.85,
        "target_acousticness": 0.10,
        "target_valence": 0.80,
        "target_danceability": 0.85,
        "target_speechiness": 0.08,
        "target_instrumentalness": 0.05,
        "target_liveness": 0.12,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "target_energy": 0.38,
        "target_acousticness": 0.78,
        "target_valence": 0.58,
        "target_danceability": 0.60,
        "target_speechiness": 0.03,
        "target_instrumentalness": 0.75,
        "target_liveness": 0.08,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "target_energy": 0.92,
        "target_acousticness": 0.08,
        "target_valence": 0.40,
        "target_danceability": 0.65,
        "target_speechiness": 0.07,
        "target_instrumentalness": 0.10,
        "target_liveness": 0.40,
    },
    "Sad Workout": {
        "genre": "any",
        "mood": "sad",
        "target_energy": 0.92,
        "target_acousticness": 0.10,
        "target_valence": 0.20,
        "target_danceability": 0.85,
        "target_speechiness": 0.05,
        "target_instrumentalness": 0.05,
        "target_liveness": 0.10,
    },
    "Talking Silence": {
        "genre": "ambient",
        "mood": "chill",
        "target_energy": 0.30,
        "target_acousticness": 0.90,
        "target_valence": 0.60,
        "target_danceability": 0.40,
        "target_speechiness": 0.95,
        "target_instrumentalness": 0.95,
        "target_liveness": 0.10,
    },
    "Country Fan": {
        "genre": "country",
        "mood": "uplifting",
        "target_energy": 0.60,
        "target_acousticness": 0.70,
        "target_valence": 0.85,
        "target_danceability": 0.70,
        "target_speechiness": 0.10,
        "target_instrumentalness": 0.20,
        "target_liveness": 0.35,
    },
    "Perfection Seeker": {
        "genre": "pop",
        "mood": "energetic",
        "target_energy": 1.0,
        "target_acousticness": 1.0,
        "target_valence": 1.0,
        "target_danceability": 1.0,
        "target_speechiness": 1.0,
        "target_instrumentalness": 1.0,
        "target_liveness": 1.0,
    },
    "Lofi-Shaped Pop Fan": {
        "genre": "pop",
        "mood": "chill",
        "target_energy": 0.38,
        "target_acousticness": 0.78,
        "target_valence": 0.58,
        "target_danceability": 0.60,
        "target_speechiness": 0.03,
        "target_instrumentalness": 0.75,
        "target_liveness": 0.08,
    },
    "Middle of the Road": {
        "genre": "indie pop",
        "mood": "happy",
        "target_energy": 0.50,
        "target_acousticness": 0.50,
        "target_valence": 0.50,
        "target_danceability": 0.50,
        "target_speechiness": 0.50,
        "target_instrumentalness": 0.50,
        "target_liveness": 0.50,
    },
}


def print_recommendations(label: str, user_prefs: dict, songs: list) -> None:
    """Runs the recommender for one profile and prints a formatted result block."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 60)
    print(f"  PROFILE: {label}")
    print(f"  Genre: {user_prefs['genre'].upper()}  |  Mood: {user_prefs['mood'].upper()}")
    print("=" * 60)

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print()
        print(f"  #{rank}  {song['title']}  |  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Score: {score:.2f} / 8.10")
        print()

        bonuses  = [r for r in reasons if "match" in r]
        numerics = [r for r in reasons if "match" not in r]

        print("       Match bonuses:")
        for r in bonuses:
            print(f"         {r}")

        print("       Numeric similarity:")
        for r in numerics:
            print(f"         {r}")

        print()
        print("  " + "-" * 56)

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, user_prefs in PROFILES.items():
        print_recommendations(label, user_prefs, songs)


if __name__ == "__main__":
    main()
