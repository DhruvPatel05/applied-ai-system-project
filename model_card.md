# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

VibeMatch is a simple content-based music recommendation system that ranks songs according to a user's musical preferences.

---

## 2. Intended Use

VibeMatch is designed to recommend songs from a small music catalog based on a user's preferred genre, mood, energy level, and acoustic preference.

The system assumes that these features provide a basic representation of a person's musical taste. It compares the user's preferences with the attributes of each available song and ranks the closest matches.

This project is designed for classroom exploration and learning. It demonstrates how data can be transformed into recommendation scores and should not be considered a production-level music recommendation system.

The system should not be used to make important decisions about users or to assume that a person's musical taste can be completely represented by a few attributes.

---

## 3. How the Model Works

VibeMatch uses a weighted scoring system.

Each song contains several attributes, including genre, mood, energy, tempo, valence, danceability, and acousticness. The current recommendation algorithm primarily uses genre, mood, energy, and acousticness.

The user provides:

- A favorite genre
- A favorite mood
- A target energy level
- An acoustic music preference

The algorithm evaluates every song individually.

A song receives **2.0 points** when its genre matches the user's favorite genre and **1.0 point** when its mood matches the user's preferred mood.

Energy is treated as a similarity measurement instead of an exact match. Songs with an energy level close to the user's target receive more points than songs that are farther away.

Acousticness is also considered. A user who prefers acoustic music receives higher matches for songs with higher acousticness, while a user who prefers less-acoustic music receives higher matches for songs with lower acousticness.

After every song receives a score, the songs are sorted from highest to lowest score and the top results are returned.

The system also generates explanations showing which features contributed to each recommendation.

---

## 4. Data

The current dataset contains **10 songs**.

The catalog includes several genres:

- Pop
- Lofi
- Rock
- Ambient
- Jazz
- Synthwave
- Indie Pop

It also contains moods such as:

- Happy
- Chill
- Intense
- Relaxed
- Moody
- Focused

Each song includes numerical features for energy, tempo, valence, danceability, and acousticness.

The dataset is intentionally small for this classroom simulation. Because there are only 10 songs, it cannot represent the diversity of real-world music.

Many genres, languages, artists, cultures, and musical styles are missing. The dataset also does not contain information such as lyrics, release year, listening history, popularity, or actual user interactions.

---

## 5. Strengths

The recommender works well when a user's preferences closely match songs represented in the dataset.

For example, the **Deep Intense Rock** profile strongly matched `Storm Runner`. The song is categorized as rock and intense, has an energy value of 0.91 compared with the user's target of 0.90, and has low acousticness.

As a result, `Storm Runner` received the highest score of **4.89** for that profile.

The system also successfully distinguishes between different types of listeners. A Chill Lofi profile favors lower-energy and more acoustic music, while the Deep Intense Rock profile favors high-energy and less-acoustic music.

Another strength is explainability. Instead of returning only a ranking, the system explains contributions such as:

- Genre match
- Mood match
- Energy similarity
- Acoustic preference

This makes it easier to understand why one song ranks above another.

---

## 6. Limitations and Bias

One major limitation is the small dataset. With only 10 songs, the recommender has very few choices and cannot represent the variety available on a real music platform.

The scoring system may also create a **filter bubble**. Genre receives 2.0 points, which is the largest individual categorical weight. As a result, songs from a user's existing favorite genre can receive a significant advantage. Repeatedly recommending similar music could make it harder for users to discover new genres.

The model also assumes that musical taste can be represented using a small number of features. Real musical preferences are much more complicated.

The system does not consider:

- Listening history
- Likes or dislikes
- Skipped songs
- Playlist activity
- Lyrics
- Language
- Artist preferences
- Listening context
- Changes in taste over time

The fixed scoring weights are the same for every user. One person may care much more about mood than genre, while another may care primarily about energy or artist.

Because the dataset itself is limited, genres or moods with fewer songs also have fewer opportunities to appear in recommendations.

---

## 7. Evaluation

I evaluated the system using three different user profiles:

### High-Energy Pop

- Favorite genre: Pop
- Favorite mood: Happy
- Target energy: 0.85
- Prefers less-acoustic music

This profile was designed to favor energetic and upbeat pop music.

### Chill Lofi

- Favorite genre: Lofi
- Favorite mood: Chill
- Target energy: 0.35
- Prefers acoustic music

This profile tests whether the ranking changes toward lower-energy, calmer, and more acoustic songs.

### Deep Intense Rock

- Favorite genre: Rock
- Favorite mood: Intense
- Target energy: 0.90
- Prefers less-acoustic music

This profile strongly favored `Storm Runner`.

Its recommendation score was:

```text
Storm Runner - Voltline
Score: 4.89
Genre match: +2.0
Mood match: +1.0
Energy similarity: +0.99
Less-acoustic preference: +0.90
```

`Gym Hero` ranked second with a score of **2.92**. Although its genre is pop instead of rock, its intense mood, high energy, and low acousticness still matched several parts of the user's preferences.

This was an interesting result because it showed that a song can rank relatively high without matching every preference.

Comparing the profiles showed that changing the user preferences changes the recommendation ranking in understandable ways. The Chill Lofi profile shifts toward calmer and more acoustic tracks, while the Deep Intense Rock profile shifts toward high-energy and less-acoustic tracks.

I also ran the provided automated tests after implementing the recommendation logic.

```text
2 passed
```

This verified that the required recommender interfaces continued to behave correctly.

---

## 8. Future Work

If I continued developing VibeMatch, I would first expand the dataset to include many more songs, genres, moods, languages, and artists.

I would also allow users to control how important different features are. For example, one user could prioritize mood while another prioritizes genre.

Additional improvements could include:

- Learning from likes and dislikes
- Tracking skipped songs
- Considering listening history
- Adding artist preferences
- Using tempo, valence, and danceability more directly in scoring
- Adding playlist information
- Supporting multiple favorite genres
- Creating different recommendation modes
- Adding a diversity penalty to avoid recommending too many similar songs
- Introducing some unfamiliar songs to reduce filter bubbles

A larger version could also combine content-based recommendations with collaborative filtering to learn from the behavior of similar users.

---

## 9. Personal Reflection

This project helped me understand that a recommendation system does not necessarily need a complicated machine learning model to produce results that feel personalized. Even a simple weighted scoring algorithm can transform user preferences into meaningful rankings.

The most interesting part for me was seeing how individual weights affected the results. `Storm Runner` ranking first for the Deep Intense Rock profile made sense when I looked at each part of its score. At the same time, seeing `Gym Hero` rank second showed that recommendations can emerge from combinations of partially matching features rather than one perfect match.

AI tools helped me brainstorm the scoring approach, debug import and data-loading problems, and think about possible biases in the system. I still needed to verify the suggestions by running the code, checking the dataset, comparing the rankings with my expectations, and running the automated tests.

This project changed how I think about recommendation apps. A recommendation can appear intelligent to a user even though it may be produced by relatively simple rules underneath. It also showed me why the choice of features, weights, and training or catalog data matters: those design decisions directly influence what users see and what they may never discover.