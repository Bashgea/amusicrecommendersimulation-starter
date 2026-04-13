"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile — describes a listener who enjoys upbeat, electronic-leaning
    # pop with high energy and very little acoustic or live feel.
    user_prefs = {
        # Categorical preferences (hard-match signals)
        "genre": "pop",
        "mood": "energetic",

        # Tier-1 numeric targets (high discriminating power)
        "target_energy": 0.85,          # wants high-energy tracks
        "target_acousticness": 0.10,    # prefers produced/electronic sound over acoustic

        # Tier-2 numeric targets (fine-grained ranking)
        "target_valence": 0.80,         # upbeat, positive-sounding tracks
        "target_danceability": 0.85,    # highly danceable
        "target_speechiness": 0.08,     # minimal spoken word / rap
        "target_instrumentalness": 0.05, # vocal-forward songs preferred
        "target_liveness": 0.12,        # studio recordings over live feel
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 60)
    print("  MUSIC RECOMMENDER - TOP 5 PICKS FOR YOU")
    print(f"  Profile: {user_prefs['genre'].upper()} / {user_prefs['mood'].upper()}")
    print("=" * 60)

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print()
        print(f"  #{rank}  {song['title']}  |  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Score: {score:.2f} / 8.10")
        print()

        # Separate match bonuses from numeric breakdown for readability
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


if __name__ == "__main__":
    main()
