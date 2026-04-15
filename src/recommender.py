import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_danceability: float
    target_valence: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _song_to_dict(self, song: Song) -> Dict:
        return {
            "id": song.id, "title": song.title, "artist": song.artist,
            "genre": song.genre, "mood": song.mood, "energy": song.energy,
            "tempo_bpm": song.tempo_bpm, "valence": song.valence,
            "danceability": song.danceability, "acousticness": song.acousticness,
        }

    def _user_to_dict(self, user: UserProfile) -> Dict:
        return {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
            "target_danceability": user.target_danceability,
            "target_valence": user.target_valence,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        prefs = self._user_to_dict(user)
        scored = []
        for song in self.songs:
            total, _ = score_song(prefs, self._song_to_dict(song))
            scored.append((song, total))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        prefs = self._user_to_dict(user)
        _, reasons = score_song(prefs, self._song_to_dict(song))
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Algorithm Recipe
    ----------------
    Category 1 — Categorical matches (binary, high weight):
      +2.0  genre match          (strongest signal of taste)
      +1.5  mood match           (strong but more subjective)

    Category 2 — Continuous similarity (1 - |diff|, scaled):
      +1.0 * energy_similarity   (energy drives feel)
      +0.6 * valence_similarity  (positive vs. dark tone)
      +0.5 * danceability_sim    (body-movement feel)

    Category 3 — Boolean modifier:
      +0.8  if likes_acoustic and acousticness >= 0.6
      -0.4  if likes_acoustic and acousticness <  0.3
      +0.4  if NOT likes_acoustic and acousticness < 0.3

    Max theoretical score ≈ 6.4  (all matches + perfect similarity)
    """
    score = 0.0
    reasons: List[str] = []

    # --- Category 1: Categorical matches ---
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append(f"genre match ({song['genre']})")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.5
        reasons.append(f"mood match ({song['mood']})")

    # --- Category 2: Continuous similarity (1 - |diff|) ---
    energy_sim = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    score += 1.0 * energy_sim
    reasons.append(f"energy similarity {energy_sim:.2f}")

    valence_sim = 1.0 - abs(song["valence"] - user_prefs["target_valence"])
    score += 0.6 * valence_sim
    reasons.append(f"valence similarity {valence_sim:.2f}")

    dance_sim = 1.0 - abs(song["danceability"] - user_prefs["target_danceability"])
    score += 0.5 * dance_sim
    reasons.append(f"danceability similarity {dance_sim:.2f}")

    # --- Category 3: Acoustic preference modifier ---
    if user_prefs["likes_acoustic"]:
        if song["acousticness"] >= 0.6:
            score += 0.8
            reasons.append("acoustic preference bonus")
        elif song["acousticness"] < 0.3:
            score -= 0.4
            reasons.append("too electronic for acoustic taste")
    else:
        if song["acousticness"] < 0.3:
            score += 0.4
            reasons.append("non-acoustic preference bonus")

    return (round(score, 2), reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, sorts descending, returns the top k with explanations.
    """
    scored = []
    for song in songs:
        total, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, total, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
