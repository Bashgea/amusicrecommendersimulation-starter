# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python -m src.main

# Run all tests
pytest

# Run a single test
pytest tests/test_recommender.py::test_recommend_returns_songs_sorted_by_score
```

## Architecture

This is a Python music recommender simulation with two parallel interfaces in `src/recommender.py`:

**OOP interface** (used by tests):
- `Song` — dataclass with fields: `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`
- `UserProfile` — dataclass with fields: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`
- `Recommender` — takes a list of `Song` objects; exposes `recommend(user, k)` → `List[Song]` and `explain_recommendation(user, song)` → `str`

**Functional interface** (used by `src/main.py`):
- `load_songs(csv_path)` → `List[Dict]` — loads from `data/songs.csv`
- `recommend_songs(user_prefs, songs, k)` → `List[Tuple[Dict, float, str]]` — returns `(song_dict, score, explanation)` tuples

`src/main.py` calls the functional interface with a hardcoded example `user_prefs` dict (`genre`, `mood`, `energy` keys) and prints the top-k results.

Tests import via `src.recommender` (package path); `src/main.py` imports directly from `recommender` (run as a module with `-m src.main` so `src/` is the package root).

The song catalog is `data/songs.csv` (10 songs with genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop).
