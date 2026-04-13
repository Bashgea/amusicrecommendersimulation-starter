# Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeMatch 1.0**

A content-based music recommender that scores songs against a listener's taste profile and returns the closest matches.

---

## 2. Intended Use

VibeMatch is designed for classroom exploration of how recommender systems work. It is not intended for real users or production use.

**Designed for:**
- Students learning how scoring and ranking algorithms work
- Experimenting with how different feature weights change recommendations
- Understanding what "content-based filtering" means in practice

**Not designed for:**
- Making real music recommendations to real people
- Handling large catalogs (it scores every song one by one — slow at scale)
- Personalizing over time (it has no memory of what you liked or skipped)
- Users whose taste doesn't fit neatly into a single genre or mood

---

## 3. How the Model Works

Each song in the catalog has 10 descriptors: genre, mood, energy, acousticness, valence, danceability, speechiness, instrumentalness, and liveness. You can think of these like a nutrition label for a song — numbers that describe what it sounds like rather than what it is.

The user provides a taste profile — a set of target values for those same descriptors. For example: "I want pop songs, energetic mood, high energy, low acoustic sound."

The system then reads every song in the catalog and asks: how close is this song to what the user described? It awards points in two ways:

1. **Bonus points for exact category matches** — if the song's genre matches the user's preferred genre, it earns +2.0 points. A mood match earns +1.5 points.
2. **Similarity points for numeric features** — for energy, acousticness, valence, and four other numeric features, the system measures the gap between the song's value and the user's target. A small gap earns almost full points; a large gap earns close to zero. Each feature has its own weight based on how useful it is for separating songs.

Every song gets a total score (max 8.1). All 18 songs are ranked from highest to lowest and the top 5 are shown with a breakdown of why each song scored the way it did.

---

## 4. Data

The catalog contains **18 songs** stored in `data/songs.csv`. Each song has 13 columns: an ID, title, artist name, and 10 audio features.

**Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, hip-hop, metal, r&b, folk, electronic, reggae, blues (15 genres total)

**Moods represented:** happy, chill, intense, focused, moody, relaxed, dreamy, energetic, angry, romantic, sad, nostalgic, uplifting, melancholic (14 moods total)

**How the data was built:** 10 songs came with the starter project. 8 more were generated to fill in missing genres and moods. All numeric feature values were assigned manually to be internally consistent (e.g., a metal song gets high energy and low acousticness), not measured from actual audio.

**What is missing:**
- No hip-hop, country, or Latin genres beyond one song each
- No songs with lyrics data or language information
- No popularity signals (plays, skips, saves)
- No songs that represent mixed or blended genres
- The catalog is far too small to serve users with niche or underrepresented tastes

---

## 5. Strengths

The system works best when the user's genre and mood are well-represented in the catalog and their numeric preferences are consistent with what that genre actually sounds like.

- **Chill Lofi profile** produced near-perfect scores (7.94/8.10) because lofi has 3 catalog entries and all their features closely matched the profile targets.
- **Deep Intense Rock** correctly identified Storm Runner as a near-perfect match (7.97/8.10) because genre, mood, and all numeric features aligned.
- The **reasons list** printed with each recommendation makes the scoring transparent — you can see exactly which features helped or hurt each song, which most real recommenders do not show.
- The system never crashes on an unusual profile — it always returns something, even if the results are low confidence.

---

## 6. Limitations and Bias

**Numeric weights can silently override genre preference.** The seven numeric similarity scores combine for a maximum of 4.6 points, while the genre bonus is only +2.0. This means a song in the wrong genre but with near-perfect numeric alignment will consistently outscore a correct-genre song with average numeric fit. The "Lofi-Shaped Pop Fan" experiment confirmed this: lofi songs ranked #1 and #2 for a user who explicitly asked for pop, because their numeric advantage (5.94) beat the pop genre bonus (4.80).

**Most genres have only one song in the catalog.** Users who prefer metal, blues, folk, reggae, classical, or 8 other genres will always get at most one true genre match in their top 5. The remaining slots are filled with numerically similar songs from unrelated genres — the system structurally cannot serve these users well.

**Mood labels are brittle.** Moods like "intense" and "energetic" or "sad" and "melancholic" feel almost the same to a listener but score as complete misses (+0.0 each). A user who wants "energetic" will never get mood credit for an "intense" song even though they would probably enjoy it.

**The system creates a filter bubble around high-energy profiles.** Energy has the highest numeric weight (1.2x) and the widest range in the catalog (0.22 to 0.97). This causes high-energy preferences to dominate rankings even when other preferences point in a different direction.

**Every user is treated as a single fixed point.** The same person might want chill lofi while studying and intense metal while working out — the system has no way to represent that. It assumes taste is one static snapshot forever.

---

## 7. Evaluation

Nine user profiles were tested: three realistic listener types and six adversarial profiles designed to break the scoring logic.

| Profile | What it tested |
|---|---|
| High-Energy Pop | Baseline — well-represented genre with clear numeric preferences |
| Chill Lofi | Whether catalog depth (3 songs) helps scores |
| Deep Intense Rock | Single-song genre — whether the +2.0 bonus is enough |
| Sad Workout | Conflicting preferences — high energy + sad mood |
| Talking Silence | Paradox — high speechiness AND high instrumentalness |
| Country Fan | Ghost genre — no country songs in catalog |
| Perfection Seeker | All targets at 1.0 — impossible to satisfy |
| Lofi-Shaped Pop Fan | Genre says pop, but numerics all match lofi |
| Middle of the Road | All numeric targets at 0.5 — no strong numeric preference |

**What was surprising:**

The Lofi-Shaped Pop Fan result was the biggest surprise. Setting `"genre": "pop"` was not enough — the system ignored the stated genre and surfaced lofi songs because their numeric similarity was stronger. This shows that genre preference alone cannot reliably control the output.

The Middle of the Road profile collapsed into a one-song recommendation: Rooftop Lights scored 6.76 while #2 dropped to 4.50. With neutral numerics, the two categorical bonuses decide everything and one song runs away with the ranking.

The Sad Workout profile produced the lowest max score of any test (4.23/8.10). No song could satisfy both high energy and sad mood at the same time, so every result felt like a compromise.

---

## 8. Future Work

**Add a minimum score threshold.** If no song scores above a certain level (say, 4.0 out of 8.1), the system should tell the user their profile doesn't match the catalog well rather than returning a confident-looking but low-quality list.

**Group similar moods together.** "Intense" and "energetic" should count as a partial match, not a total miss. A simple mood similarity table (e.g., intense is 50% similar to energetic) would make the scoring much more realistic without adding complexity.

**Add a diversity rule.** Songs like Gym Hero appear in almost every top-5 because they score well across many profiles. A real recommender would cap how often any single song appears and push lower-ranked but different songs into the results.

---

## 9. Personal Reflection

**Biggest learning moment**

The clearest moment was running the Lofi-Shaped Pop Fan profile and watching the system ignore the genre I explicitly set. I had assumed that saying `"genre": "pop"` would act like a hard filter — only pop songs, end of story. Instead the numeric similarity for lofi songs was strong enough to push past the genre bonus entirely. That was the moment the whole project clicked: a recommender does not "understand" your preferences, it just adds up numbers. If your numbers point in two different directions, the bigger number wins every time, silently.

**Working with Python and AI tools**

Honestly, Python was the hardest part of this project. I could read the code and understand what it was doing most of the time, especially when I asked the AI to explain a specific line or walk me through a function. But there is a difference between understanding code when you read it and being able to write it from scratch. I felt that gap most when something broke — I could see that something was wrong, but I was slow at knowing exactly where to look or what to change without help.

The AI tools were genuinely useful for moving fast: generating the scoring logic, formatting the output, expanding the CSV. But I learned to double-check them on anything that involved the actual data. A few times the AI generated feature values or weights that looked reasonable but did not match the logic I had already built. Reading the output carefully and running the code myself was what caught those moments — the AI gave me a starting point, not a finished answer.

If I had spent more time practicing Python basics before starting — writing small functions from scratch, debugging independently — I think I would have moved faster and leaned on the AI less for the mechanical parts. That is the thing I would change about how I approached this.

**What surprised me about simple algorithms**

I expected a rule-based system with hand-tuned weights to feel obviously fake. It does not. When the Chill Lofi profile returned Library Rain and Midnight Coding at the top with near-perfect scores, and the Deep Intense Rock profile returned Storm Runner as a nearly perfect match, the results genuinely felt like a real recommendation. The system does not know anything about music — it just measures distance between numbers — but that is enough to produce output that feels intentional. That made me think differently about apps like Spotify. The "magic" in their recommendations probably starts from the same place: features, weights, and distance. The scale is different but the idea is not.

**What I would try next**

I would want to build a version where the user profile updates based on feedback. Right now the profile is fixed — you set it once and it never changes. A real improvement would be: if a user clicks "I liked this song," the system nudges the profile slightly toward that song's features. After enough likes and skips, the profile would start to reflect actual behavior instead of a static guess. That is the gap between a rule-based system like this one and a real learning recommender, and I now understand exactly where that line is.
