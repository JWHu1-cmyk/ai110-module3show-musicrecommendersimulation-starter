# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder recommends 5 songs from a small catalog based on a user's preferred genre, mood, energy level, valence, danceability, and acoustic preference. It is designed for classroom exploration of content-based recommendation systems.

**Intended use:** Educational demonstration of how content-based filtering works. Students and instructors can use it to explore how weight tuning, feature selection, and profile design affect recommendation quality.

**Non-intended use:** This system should not be used to make real music recommendations for actual listeners. It has no feedback loop, no collaborative filtering, no understanding of lyrics or cultural context, and only 20 songs. Using it as a real product would create severe filter bubbles and exclude listeners whose tastes fall outside the narrow catalog. It should also not be used to draw conclusions about real listener behavior — the profiles and scores are synthetic.

---

## 3. How the Model Works

The system takes a user's taste profile (favorite genre, mood, energy target, etc.) and compares it against every song in the catalog. Each song receives a numeric score based on how well it matches the user's preferences:

- If the song's genre matches the user's favorite, it earns the most points (this is the strongest signal).
- A mood match earns the second-highest bonus.
- For energy, valence, and danceability, the system measures how close the song's value is to the user's target — the closer, the more points.
- An acoustic preference acts as a bonus or penalty depending on whether the user likes acoustic music and how acoustic the song actually is.

All points are added together into a final score. The songs are sorted from highest to lowest score, and the top 5 are returned as recommendations. Each recommendation includes a plain-language explanation of which features contributed to its score.

---

## 4. Data

The catalog contains **20 songs** in `data/songs.csv`. The original starter file had 10 songs; 10 additional songs were added to diversify genre and mood coverage.

**Genres represented (12):** pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, electronic, folk, hip-hop, classical, reggae, metal, country

**Moods represented (10):** happy, chill, intense, relaxed, moody, focused, romantic, energetic, peaceful, sad, melancholic

**Gaps:** The catalog skews toward Western music and English-language artists. Genres like Latin, Afrobeat, K-pop, and Bollywood are entirely absent. The mood labels are subjective and were assigned by one person, which means they reflect a single cultural perspective on what "happy" or "intense" sounds like.

---

## 5. Strengths

- **Transparent and explainable.** Every recommendation comes with a list of reasons. A user can see exactly why "Sunrise City" scored 5.94 — genre match, mood match, high energy similarity, etc.
- **Strong differentiation for clear profiles.** The Pop Listener gets pop songs, the Lofi Studier gets lofi songs, and the Rock Fan gets rock songs. The system does not confuse these three archetypes.
- **Graceful fallback for missing genres.** When a user prefers a genre not in the catalog (e.g., "k-pop"), the system still returns reasonable results by relying on mood and continuous feature matches instead of returning nothing.

---

## 6. Limitations and Bias

The system's genre weight (+2.0) is so dominant that a genre match alone can outweigh a perfect mood and energy fit from another genre. During the weight-shift experiment (halving genre to +1.0, doubling energy to +2.0), the Pop Listener's top 5 reshuffled significantly — "Rooftop Lights" (indie pop/happy) jumped from #4 to #2 because its energy similarity became more valuable than "Gym Hero's" genre match. This showed that the original weights create a strong genre bubble: users are unlikely to discover great songs outside their stated genre even when those songs match every other preference perfectly.

The system also treats categorical features as exact-match-only. "Indie pop" and "pop" share zero credit, and "chill" vs. "relaxed" are treated as completely different moods despite being semantically similar. This penalizes songs that are near-matches. Additionally, the system has no notion of time, context, or listening history — a user who wants "chill" at midnight and "intense" at the gym cannot be served by a single static profile. Finally, the small 20-song catalog means some genres (classical, folk, metal) have only one representative, making the ranking trivially determined by the catalog size rather than the algorithm's intelligence.

---

## 7. Evaluation

Six user profiles were tested — three standard and three adversarial edge cases:

| Profile | Purpose | Top Result | Matched Expectations? |
|---------|---------|------------|-----------------------|
| Upbeat Pop Listener | Baseline pop/happy | Sunrise City (5.94) | Yes — pop/happy, highest energy similarity |
| Chill Lofi Studier | Baseline lofi/chill | Library Rain (6.38) | Yes — near-perfect match on all features |
| Intense Rock Fan | Baseline rock/intense | Storm Runner (5.97) | Yes — only rock/intense song in catalog |
| High-Energy Sad | Conflicting preferences | Rainy Window (5.32) | Partially — genre+mood match won despite terrible energy fit (0.30 similarity) |
| K-Pop Fan | Missing genre | Sunrise City (3.81) | Yes — fell back to mood+continuous features gracefully |
| Middle-of-the-Road | Bland preferences | Sunrise City (3.83) | Mixed — scores were compressed (3.25–3.83), hard to differentiate |

**Surprise:** The High-Energy Sad profile exposed a real flaw. "Rainy Window" (classical/sad, energy 0.20) won despite the user wanting energy 0.90 — the genre+mood bonus (+3.5) overwhelmed the energy penalty. In a real system, this would feel like a bad recommendation: the user asked for intense energy and got the quietest song in the catalog.

**Weight-shift experiment:** Halving genre (2.0 → 1.0) and doubling energy (1.0 → 2.0) made the system more sensitive to energy and less locked into genre bubbles. For the Middle-of-the-Road profile, lofi/chill songs overtook pop songs in the top 3 because their energy was closer to the 0.50 target. The experiment showed the recommendations were *different* but not necessarily *more accurate* — it depends on whether you believe genre identity or energy feel matters more to a listener.

---

## 8. Future Work

- **Fuzzy categorical matching.** Treat "indie pop" as partially matching "pop," and "chill" as partially matching "relaxed," using a similarity lookup table or embedding distance.
- **Context-aware profiles.** Allow a user to have multiple profiles (e.g., "gym mode" vs. "study mode") instead of a single static preference set.
- **Diversity injection.** After selecting the top k, swap in one song from an underrepresented genre to help users discover new music and avoid filter bubbles.
- **Larger catalog.** Scale to 100+ songs so that ranking quality depends on the algorithm rather than catalog sparsity.
- **Feedback learning.** Track which recommendations the user accepts or skips and adjust weights over time.

---

## 9. Personal Reflection

**Biggest learning moment:** Building this system made it clear how much power sits in the weight choices. Changing a single number (genre from 2.0 to 1.0) reshuffled entire ranking lists — and neither version was objectively "right." This is the core tension in recommender systems: the weights encode a value judgment about what matters, and that judgment is made by the developer, not the user. The moment I ran the weight-shift experiment and saw "Drop the Bass" (an electronic track) appear in the Rock Fan's top 5, it clicked that every recommendation system is an opinion about taste disguised as math.

**How AI tools helped and where I double-checked:** AI was useful for generating the initial batch of diverse songs for the CSV (ensuring I covered genres like reggae, classical, and metal that I might not have thought to include). It also helped draft the scoring weight rationale and suggest adversarial profiles. However, I had to double-check the math — when the AI suggested weight values, I verified them by running all six profiles and manually confirming the rankings made intuitive sense. The High-Energy Sad edge case was something I had to reason through myself: the AI did not flag that genre+mood dominance would override a terrible energy fit until I ran the numbers.

**What surprised me about simple algorithms:** The most surprising thing was how convincing a weighted sum can feel. When the Pop Listener gets "Sunrise City" at 5.94 with reasons like "genre match, mood match, energy similarity 0.98," it genuinely feels like the system "understands" the user's taste. But it is just addition. There is no understanding — only arithmetic that happens to align with human intuition when the weights are tuned well. The illusion breaks the moment you feed in a contradictory profile (High-Energy Sad) and the system confidently recommends the quietest song in the catalog.

**What I would try next:** If I extended this project, I would add fuzzy matching for categorical features so that "indie pop" gets partial credit against "pop" and "chill" partially matches "relaxed." I would also build a simple feedback loop where the user can thumbs-up or thumbs-down a recommendation, and the system adjusts its weights accordingly over time. Finally, I would add a diversity constraint that forces at least one song from a genre the user has never heard into the top 5 — breaking the filter bubble by design rather than hoping the weights do it naturally.
