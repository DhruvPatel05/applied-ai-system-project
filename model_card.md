# 🎧 Model Card: VibeMatch Reliable AI Music Recommendation System

## 1. Model Name

**VibeMatch 2.0 — Reliable AI Music Recommendation System**

VibeMatch is a content-based music recommendation system that ranks songs according to user preferences and provides explanations, input validation, and a reliability assessment for its recommendations.

This version evolves my original Music Recommender Simulation by adding a dedicated reliability layer.

---

## 2. Intended Use

VibeMatch is designed to recommend songs from a small music catalog based on a user's preferred genre, mood, energy level, and acoustic preference.

The system compares these preferences with song attributes and ranks the closest matches.

VibeMatch 2.0 also evaluates whether user inputs fall within expected ranges and provides a confidence label for the recommendation result.

This project is intended for classroom exploration and learning. It demonstrates how recommendation logic can be combined with reliability engineering, explainability, validation, and testing.

It is **not** intended to be a production-level music recommendation platform or an authoritative predictor of a person's musical preferences.

---

## 3. How the System Works

VibeMatch uses a weighted content-based scoring system.

Each song contains attributes including:

- Genre
- Mood
- Energy
- Tempo
- Valence
- Danceability
- Acousticness

The recommendation algorithm primarily uses genre, mood, energy, and acousticness.

The user profile provides:

- Favorite genre
- Favorite mood
- Target energy level
- Acoustic music preference

### Recommendation Scoring

Each song is evaluated individually.

A song receives **2.0 points** when its genre matches the user's favorite genre and **1.0 point** when its mood matches the user's preferred mood.

Energy is evaluated using similarity. Songs with an energy value close to the user's target receive more points.

Acousticness is also considered. Users who prefer acoustic music receive stronger matches for songs with higher acousticness, while users who prefer less-acoustic music receive stronger matches for lower-acousticness songs.

The songs are sorted from highest to lowest score and the top five are returned.

The system also provides an explanation showing which factors contributed to each score.

---

## 4. Reliability Layer

VibeMatch 2.0 introduces a dedicated reliability component in:

```text
src/reliability.py
```

The reliability layer performs two main tasks.

### Input Validation

Before evaluating recommendation reliability, the system checks user preference values.

It detects conditions including:

- Unsupported moods
- Unsupported genres
- Energy values outside the expected 0–1 range
- Non-numeric energy values
- Incorrect preference input types

For unusual or unsupported inputs, the system produces warnings rather than silently treating the input as reliable.

### Confidence Assessment

After recommendations are generated, the system evaluates the score of the highest-ranked recommendation.

The current confidence heuristic is:

| Top Recommendation Score | Confidence |
|---|---|
| 2.5 or higher | High |
| 1.5–2.49 | Medium |
| Below 1.5 | Low |

For example:

```text
Confidence: High
Top recommendation score: 4.89
```

The confidence value represents the strength of the match according to VibeMatch's scoring rules.

**It is not a calibrated probability that the user will like the recommendation.**

This distinction is explicitly shown to users in the system output.

---

## 5. Data

The current dataset contains **10 songs**.

The catalog includes genres such as:

- Pop
- Lofi
- Rock
- Ambient
- Jazz
- Synthwave
- Indie Pop

It contains moods such as:

- Happy
- Chill
- Intense
- Relaxed
- Moody
- Focused

Each song also contains numerical features for energy, tempo, valence, danceability, and acousticness.

The dataset is intentionally small for this classroom simulation.

Because it contains only 10 songs, it cannot represent the diversity of real-world music.

Many genres, languages, artists, cultures, and musical styles are missing. The dataset also does not contain information such as lyrics, release year, listening history, popularity, or actual user interactions.

---

## 6. Strengths

One major strength of VibeMatch is explainability.

Instead of returning only a ranked list, the system explains why recommendations received their scores.

Possible explanation components include:

- Genre match
- Mood match
- Energy similarity
- Acoustic preference

For example, `Storm Runner` can receive:

```text
Genre match (+2.0)
Mood match (+1.0)
Energy similarity (+0.99)
Less-acoustic preference (+0.90)
```

This makes the recommendation process easier to inspect.

Another strength of VibeMatch 2.0 is that the system no longer presents recommendation scores without additional context.

The reliability layer provides:

- Input validation
- Warnings
- Confidence labels
- Empty-result handling
- Explicit uncertainty messaging

The system also has automated tests covering both recommendation logic and reliability behavior.

---

## 7. Limitations and Bias

### Small Dataset

The largest limitation is the dataset size.

With only 10 songs, VibeMatch has very few choices and cannot represent the diversity available on real music platforms.

### Filter Bubble Risk

Genre receives 2.0 points, which is the largest individual categorical weight.

This means songs from a user's favorite genre receive a significant advantage.

Repeatedly prioritizing the same genres could create a filter-bubble effect and reduce opportunities for users to discover unfamiliar music.

### Simplified User Preferences

Real musical taste is significantly more complicated than the features represented in this project.

The system does not consider:

- Listening history
- Likes and dislikes
- Skipped songs
- Playlist activity
- Lyrics
- Language
- Artist preferences
- Listening context
- Changes in taste over time

### Fixed Weights

The scoring weights are identical for every user.

One person may care primarily about mood, while another may care much more about genre or energy.

The current system cannot learn those differences.

### Confidence Is Heuristic

The High, Medium, and Low confidence categories are based on manually selected score thresholds.

They have not been calibrated against real user satisfaction data.

Therefore:

```text
High confidence ≠ 90% chance that the user will like the song
```

It only means that the song strongly matches the preference rules used by this system.

---

## 8. Evaluation

The recommendation system was evaluated using different user profiles representing different musical preferences.

Examples include:

### High-Energy Pop

- Favorite genre: Pop
- Favorite mood: Happy
- Target energy: 0.85
- Prefers less-acoustic music

### Chill Lofi

- Favorite genre: Lofi
- Favorite mood: Chill
- Target energy: 0.35
- Prefers acoustic music

### Deep Intense Rock

- Favorite genre: Rock
- Favorite mood: Intense
- Target energy: 0.90
- Prefers less-acoustic music

For a high-intensity profile, the system produced a strong match:

```text
Storm Runner - Voltline
Score: 4.89

Because:
genre match (+2.0),
mood match (+1.0),
energy similarity (+0.99),
less-acoustic preference (+0.90)
```

The reliability layer classified this result as:

```text
Status: Success
Confidence: High
Top recommendation score: 4.89
```

`Gym Hero` ranked second with a score of **2.92**.

Although its genre did not match rock, its intense mood, high energy, and low acousticness matched several other preferences.

This demonstrates that recommendations can rank highly through combinations of partially matching features rather than requiring an exact match on every attribute.

---

## 9. Reliability Evaluation

The reliability component was evaluated using normal inputs as well as edge cases.

### Valid Input

Example:

```python
{
    "mood": "happy",
    "genre": "pop",
    "energy": 0.8
}
```

Expected behavior:

```text
Validation passes with no warnings.
```

### Invalid Energy

Example:

```python
{
    "mood": "happy",
    "genre": "pop",
    "energy": 1.5
}
```

Expected behavior:

```text
Energy must be between 0 and 1.
```

### Unsupported Preferences

Example:

```python
{
    "mood": "super-excited",
    "genre": "space-music",
    "energy": 0.5
}
```

The system identifies the unsupported mood and genre and generates warnings.

### Empty Recommendations

The system also handles an empty recommendation list.

Instead of reporting successful recommendations, it returns:

```text
Status: No recommendations
Confidence: Low
```

---

## 10. Automated Testing

The project contains tests for both the original recommender and the new reliability layer.

The full test suite is run with:

```bash
python -m pytest -q
```

Current result:

```text
8 passed
```

Reliability tests cover:

- Valid preferences
- Invalid energy values
- Unknown moods
- Unknown genres
- High confidence
- Medium confidence
- Low confidence
- Reliability summary generation
- Empty recommendation behavior

Automated testing was especially useful for confirming that adding the reliability layer did not break the existing recommendation functionality.

---

## 11. Failure Modes

Several failure modes remain possible.

### Unsupported Preference Categories

A user may provide a mood or genre that is not represented by the supported categories.

The reliability layer warns about this situation, but the recommendation engine may still produce less meaningful rankings.

### Small Catalog

The recommender must choose from the available songs even when none are particularly strong matches.

A low confidence result can help communicate this limitation, but it does not solve the underlying lack of data.

### Misinterpreting Confidence

Users could interpret "High confidence" as meaning that they will definitely enjoy a recommendation.

To reduce this risk, the system explicitly displays:

```text
Confidence is estimated from the recommendation matching score.
It is not a probability of user satisfaction.
```

### Subjective Preferences

Musical taste is subjective and can change depending on context, mood, location, activity, or time.

A static preference profile cannot fully capture those changes.

---

## 12. Human-in-the-Loop Considerations

VibeMatch does not make high-stakes decisions, so human review is not required for each recommendation.

However, users should remain the final decision-maker about whether a recommendation is useful.

The system should avoid presenting recommendations as objective judgments about a person's taste.

When input quality is poor or recommendation confidence is low, the appropriate behavior is to communicate uncertainty rather than claim that the result is reliable.

---

## 13. Responsible AI Considerations

Recommendation systems influence what users discover and consume.

Even a small system like VibeMatch demonstrates how design decisions can affect what information users see.

For example, assigning genre a higher weight increases the likelihood that users continue seeing songs similar to their existing preferences.

VibeMatch attempts to improve responsible AI behavior through:

- Explainable scoring
- Input validation
- Reliability warnings
- Confidence labels
- Explicit uncertainty communication
- Graceful empty-result handling
- Edge-case testing

However, these safeguards do not eliminate bias introduced by the dataset or scoring rules.

---

## 14. Future Work

If I continued developing VibeMatch, I would first expand the dataset to include many more songs, genres, moods, languages, artists, and cultures.

Additional improvements could include:

- Learning from likes and dislikes
- Tracking skipped songs
- Considering listening history
- Adding artist preferences
- Using tempo, valence, and danceability more directly
- Supporting multiple favorite genres
- Allowing users to customize feature weights
- Adding diversity-aware recommendations
- Introducing unfamiliar songs to reduce filter bubbles
- Collaborative filtering
- Embedding-based similarity
- Calibrating confidence using real user feedback
- Building an interactive Streamlit interface
- Integrating a real music API

A future reliability system could also distinguish between uncertainty caused by weak preference matches and uncertainty caused by limited catalog coverage.

---

## 15. Personal Reflection

This project helped me understand that building an AI system involves more than producing an output.

My original Music Recommender Simulation focused primarily on ranking songs. While evolving it into VibeMatch 2.0, I started thinking more about what happens around the recommendation algorithm.

For example:

- What happens when the input is unusual?
- How should the system communicate uncertainty?
- What happens when there are no recommendations?
- How can users understand why a recommendation was generated?
- How can automated tests verify reliability behavior?

Adding the reliability layer showed me that a system can be improved significantly without replacing the core recommendation algorithm.

The most important lesson was that a confidence label needs context. Simply displaying "High confidence" could be misleading. For that reason, I explicitly state that confidence is based on the internal matching score and is not a probability of user satisfaction.

AI tools helped me brainstorm reliability approaches, debug Python import and integration issues, design test cases, and improve documentation. I still verified the suggestions by running the application, inspecting outputs, fixing errors, and running the automated test suite.

The project reinforced that responsible AI engineering includes not only the model or algorithm, but also validation, testing, explainability, failure handling, documentation, and honest communication of limitations.