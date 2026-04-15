"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # --- User Taste Profiles ---
    # Each profile targets different corners of the catalog so the
    # recommender must actually differentiate between songs.

    # Profile A: upbeat pop listener — high energy, happy, non-acoustic
    profile_a = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "likes_acoustic": False,
        "target_danceability": 0.75,
        "target_valence": 0.80,
    }

    # Profile B: chill lofi studier — low energy, focused/chill, acoustic
    profile_b = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
        "target_danceability": 0.55,
        "target_valence": 0.60,
    }

    # Profile C: intense rock fan — very high energy, intense, non-acoustic
    profile_c = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "likes_acoustic": False,
        "target_danceability": 0.65,
        "target_valence": 0.45,
    }

    # --- Edge-Case / Adversarial Profiles ---

    # Conflicting: high energy but sad mood — can the system handle the tension?
    profile_d = {
        "favorite_genre": "classical",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "likes_acoustic": True,
        "target_danceability": 0.80,
        "target_valence": 0.20,
    }

    # Non-existent genre — nothing in the catalog matches "k-pop"
    profile_e = {
        "favorite_genre": "k-pop",
        "favorite_mood": "happy",
        "target_energy": 0.70,
        "likes_acoustic": False,
        "target_danceability": 0.85,
        "target_valence": 0.90,
    }

    # Middle-of-the-road — all preferences at 0.5, no strong signal
    profile_f = {
        "favorite_genre": "pop",
        "favorite_mood": "chill",
        "target_energy": 0.50,
        "likes_acoustic": False,
        "target_danceability": 0.50,
        "target_valence": 0.50,
    }

    profiles = {
        "Upbeat Pop Listener": profile_a,
        "Chill Lofi Studier": profile_b,
        "Intense Rock Fan": profile_c,
        "EDGE: High-Energy Sad (conflicting)": profile_d,
        "EDGE: K-Pop Fan (missing genre)": profile_e,
        "EDGE: Middle-of-the-Road (no strong signal)": profile_f,
    }

    for name, prefs in profiles.items():
        print(f"\n{'='*50}")
        print(f"Profile: {name}")
        print(f"  genre={prefs['favorite_genre']}, mood={prefs['favorite_mood']}, "
              f"energy={prefs['target_energy']}, acoustic={prefs['likes_acoustic']}, "
              f"danceability={prefs['target_danceability']}, valence={prefs['target_valence']}")
        print(f"{'='*50}")

        recommendations = recommend_songs(prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for rec in recommendations:
            song, score, explanation = rec
            print(f"  {song['title']} - Score: {score:.2f}")
            print(f"  Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
