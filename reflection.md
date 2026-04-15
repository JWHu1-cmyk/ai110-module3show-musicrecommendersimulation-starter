# Reflection: Profile Comparisons

## Pop Listener vs. Lofi Studier

These two profiles sit at opposite ends of the energy spectrum (0.80 vs. 0.35) and have opposite acoustic preferences (False vs. True). Their top-5 lists share zero songs in common. The Pop Listener's results are dominated by upbeat, danceable tracks with low acousticness (Sunrise City, Gym Hero), while the Lofi Studier's list is entirely acoustic-leaning, low-energy songs (Library Rain, Midnight Coding). This confirms that the combination of genre match, energy similarity, and the acoustic modifier is sufficient to fully separate these two user archetypes. The system correctly treats them as distinct taste profiles rather than blending them.

## Pop Listener vs. Intense Rock Fan

Both profiles target high energy (0.80 vs. 0.92) and both dislike acoustic music, yet their top-5 lists diverge sharply. The Pop Listener gets happy, high-valence songs (Sunrise City at valence 0.84), while the Rock Fan gets dark, low-valence tracks (Storm Runner at valence 0.48). This separation is driven by the genre and mood categorical matches — without them, these two profiles would converge on the same high-energy songs. "Gym Hero" (pop/intense) appears in both lists but at different ranks (#2 for Pop, #4 for Rock), which makes sense: it shares genre with one and mood with the other.

## Lofi Studier vs. High-Energy Sad (Edge Case)

The Lofi Studier wants low energy (0.35) and gets it — Library Rain (0.35 energy) scores 6.38 with near-perfect similarity across all features. The High-Energy Sad profile also targets acoustic music but wants high energy (0.90). Despite this, the system recommends "Rainy Window" (energy 0.20) as the top pick because genre+mood match (+3.5) overwhelms the poor energy similarity (0.30). This comparison exposes a critical flaw: the system cannot distinguish between "I want quiet acoustic music" and "I want loud acoustic music" when genre and mood dominate the score. A real user with the High-Energy Sad profile would likely prefer something like a dramatic orchestral piece, not a quiet piano track.

## K-Pop Fan (Edge Case) vs. Pop Listener

The K-Pop Fan and Pop Listener both want happy, high-energy, non-acoustic music. The key difference: "k-pop" matches no genre in the catalog, so the K-Pop Fan never receives the +2.0 genre bonus. As a result, their top score is only 3.81 (vs. the Pop Listener's 5.94). Despite the lower scores, the K-Pop Fan's top-5 list is still reasonable — it surfaces happy songs with good energy and danceability matches (Sunrise City, Island Breeze, Rooftop Lights). This shows the continuous features provide a meaningful fallback when categorical matches fail, though the compressed score range (3.47–3.81) means the system has low confidence in differentiating among the top results.

## Middle-of-the-Road (Edge Case) vs. All Others

The Middle-of-the-Road profile (energy 0.50, valence 0.50, danceability 0.50) produces the most compressed score range of any profile: 3.25 to 3.83. Compare this to the Lofi Studier's range of 2.81 to 6.38 — a spread of 3.57 points. The bland profile's 0.58-point spread means the system has almost no ability to rank songs meaningfully. Every mid-tempo, mid-energy song scores about the same. This reveals that recommender systems need strong user signals to produce strong rankings. When a user's preferences are ambiguous, the algorithm cannot compensate — it simply returns a flat, unconvincing list. In a real product, this is exactly where collaborative filtering (what do similar users like?) would fill the gap that content-based scoring cannot.

## Weight-Shift Experiment: Original vs. Modified Weights

When genre was halved (2.0 → 1.0) and energy was doubled (1.0 → 2.0), three notable shifts occurred. First, for the Pop Listener, "Rooftop Lights" (indie pop/happy) jumped from #4 to #2 — its energy similarity (0.96) became more valuable than the genre match that previously favored "Gym Hero." Second, for the Rock Fan, "Drop the Bass" (electronic/energetic) entered the top 5 for the first time — its energy (0.95) is close to the target (0.92), and with doubled energy weight, that similarity alone was enough to push it past songs with better mood matches. Third, for the Middle-of-the-Road profile, lofi/chill songs overtook pop songs in the top 3 because their energy values (0.35–0.42) were closer to the 0.50 target than the pop songs' energy (0.82–0.93). The experiment demonstrates that weight tuning is not a neutral technical decision — it encodes a philosophical choice about whether genre identity or acoustic feel should define a listener's taste.
