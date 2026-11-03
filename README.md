# 🎵 Music Recommender Simulation

## Project Summary

This project is a simple content-based music recommendation system built in Python. It compares a user's music preferences with song attributes and calculates a weighted score for every song in the dataset.

My recommender considers genre, mood, energy, and acousticness when ranking songs. Instead of only returning recommendations, the system also explains why each song received its score. This makes it easier to understand how user preferences are transformed into ranked recommendations.

---

## How The System Works

The system uses information about each song and compares it with a user's taste profile.

### Song Features

Each `Song` contains:

- Title
- Artist
- Genre
- Mood
- Energy
- Tempo (BPM)
- Valence
- Danceability
- Acousticness

### User Profile

A `UserProfile` stores:

- Favorite genre
- Favorite mood
- Target energy level
- Acoustic music preference

### Algorithm Recipe

Each song receives a score based on how closely it matches the user's preferences.

- **+2.0 points** for a matching genre
- **+1.0 point** for a matching mood
- **Energy similarity points** based on how close the song's energy is to the user's target energy
- **Acoustic preference points** based on whether the user prefers acoustic or less-acoustic music

The energy score is calculated by measuring the difference between the song's energy and the user's target energy. A smaller difference produces a higher score.

The recommender calculates a score for every song, sorts the songs from highest score to lowest score, and returns the top `k` recommendations.

### Data Flow

```text
User Preferences
      ↓
Load Song Dataset
      ↓
Score Every Song
      ↓
Genre + Mood + Energy + Acousticness
      ↓
Sort by Score
      ↓
Return Top K Recommendations
```

This is a simplified content-based recommender. Real platforms such as Spotify and YouTube can combine content information with listening behavior, interactions, and information from many users.

---

## Getting Started

### Setup

1. Create a virtual environment:

```bash
python3 -m venv .venv
```

2. Activate the environment on macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the recommender:

```bash
python -m src.main
```

### Running Tests

Run the tests with:

```bash
python -m pytest
```

Current test result:

```text
2 passed
```

---

## Sample Recommendation Output

The recommender was evaluated with multiple user profiles.

### Deep Intense Rock

```text
PROFILE: Deep Intense Rock

1. Storm Runner - Voltline
   Genre: rock | Mood: intense
   Score: 4.89
   Because: genre match (+2.0), mood match (+1.0),
   energy similarity (+0.99), less-acoustic preference (+0.90)

2. Gym Hero - Max Pulse
   Genre: pop | Mood: intense
   Score: 2.92
   Because: mood match (+1.0), energy similarity (+0.97),
   less-acoustic preference (+0.95)

3. Sunrise City - Neon Echo
   Genre: pop | Mood: happy
   Score: 1.74
   Because: energy similarity (+0.92),
   less-acoustic preference (+0.82)

4. Night Drive Loop - Neon Echo
   Genre: synthwave | Mood: moody
   Score: 1.63
   Because: energy similarity (+0.85),
   less-acoustic preference (+0.78)

5. Rooftop Lights - Indigo Parade
   Genre: indie pop | Mood: happy
   Score: 1.51
   Because: energy similarity (+0.86),
   less-acoustic preference (+0.65)
```

The system correctly ranked `Storm Runner` first because it matches the user's preferred genre and mood, has almost exactly the requested energy level, and is highly non-acoustic.

---

## Evaluation Profiles

I tested the recommender with three different user profiles.

### High-Energy Pop

Preferences:

- Genre: Pop
- Mood: Happy
- Target Energy: 0.85
- Prefers less-acoustic music

This profile is designed to favor energetic pop songs. `Sunrise City` is a strong match because its genre and mood both match and its energy level is close to the user's target.

### Chill Lofi

Preferences:

- Genre: Lofi
- Mood: Chill
- Target Energy: 0.35
- Prefers acoustic music

This profile shifts the rankings toward lower-energy and more acoustic tracks. Songs such as `Library Rain` and `Midnight Coding` have characteristics that fit this profile well.

### Deep Intense Rock

Preferences:

- Genre: Rock
- Mood: Intense
- Target Energy: 0.90
- Prefers less-acoustic music

`Storm Runner` ranked first for this profile with a score of 4.89. This result makes sense because it is rock, intense, has an energy value of 0.91, and has very low acousticness.

The different results demonstrate that changing the user preferences changes the ranking instead of producing the same recommendations for every user.

---

## Experiments You Tried

I compared recommendation results across three very different taste profiles: High-Energy Pop, Chill Lofi, and Deep Intense Rock.

The experiment showed that genre has a strong influence because an exact genre match contributes 2.0 points. Mood contributes another 1.0 point, while energy and acousticness help distinguish songs that otherwise have similar categorical matches.

One interesting result was `Gym Hero` for the Deep Intense Rock profile. Although it is a pop song rather than rock, it ranked second because its intense mood, 0.93 energy level, and very low acousticness strongly matched the other user preferences.

This demonstrated that a song does not necessarily need to match every feature to receive a relatively high recommendation score.

---

## Limitations and Risks

This recommender has several limitations.

- The dataset currently contains only 10 songs, so the recommendation choices are limited.
- Genre receives a relatively large weight, which may cause the system to repeatedly recommend songs from a user's existing favorite genre.
- The system does not learn from actual user behavior such as likes, skips, listening time, or playlist additions.
- It does not understand lyrics, language, artist similarity, or the context in which someone is listening.
- The fixed scoring weights may not represent every user's definition of a good recommendation.
- Content-based recommendations can create a filter bubble by repeatedly favoring music similar to preferences the user already provided.

A larger real-world system would need more diverse data and feedback signals to balance relevance with discovery.

---

## Reflection

One of my biggest learning moments in this project was seeing how a relatively simple mathematical scoring system can produce recommendations that feel personalized. The program does not actually understand music like a person does. Instead, it converts preferences such as genre, mood, energy, and acousticness into numbers and uses those numbers to rank songs. Seeing `Storm Runner` rank first for the Deep Intense Rock profile helped me understand how individual feature weights directly affect the final prediction.

AI tools helped me think through the scoring logic, debug Python import issues, and organize the recommendation explanations. However, I still needed to run the program and tests myself and compare the results with the original dataset. This was important because code that looks reasonable can still behave differently than expected when tested with real data. If I continued developing this project, I would expand the dataset, incorporate user interactions such as likes and skips, experiment with different scoring weights, and add a diversity mechanism so recommendations introduce users to new genres instead of only reinforcing their existing preferences.

For a more detailed discussion of the system, evaluation, intended use, and limitations, see the [Model Card](model_card.md).