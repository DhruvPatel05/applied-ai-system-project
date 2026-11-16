# Reliable AI Music Recommendation System

An applied AI system that recommends songs based on user preferences while also providing explainable scoring, input validation, and a reliability assessment.

This project evolves my earlier **Music Recommender Simulation** into a more complete and reliable AI system. The original recommendation engine ranked songs based on user preferences. The upgraded system adds validation, confidence assessment, reliability warnings, testing, and system-level documentation.

## Project Overview

Music recommendation systems can provide useful personalized results, but users should also understand why a recommendation was made and how much confidence they should place in it.

This project combines:

- User preference processing
- Song recommendation and ranking
- Explainable recommendation scores
- Input validation
- Reliability checks
- Confidence labels
- Automated testing

The goal is not only to recommend songs but also to make the recommendation process more transparent and reliable.

## Key Features

### Personalized Recommendations

The system recommends the top five songs based on preferences such as:

- Genre
- Mood
- Energy
- Acoustic preference

### Explainable Recommendations

Each recommendation includes an explanation describing why the song received its score.

Example:

```text
Storm Runner - Voltline
Genre: rock | Mood: intense
Score: 4.89

Because:
genre match (+2.0),
mood match (+1.0),
energy similarity (+0.99),
less-acoustic preference (+0.90)
```

### Input Validation

Before assessing the recommendation results, the reliability layer validates supported user preference values.

It checks for:

- Unknown moods
- Unknown genres
- Invalid energy values
- Non-numeric energy values
- Incorrect preference input types

Invalid or unusual preferences generate warnings so that unreliable inputs are not silently accepted.

### Reliability Assessment

The system evaluates the score of the highest-ranked recommendation and converts it into an interpretable confidence level.

| Top Score | Confidence |
|---|---|
| 2.5 or higher | High |
| 1.5–2.49 | Medium |
| Below 1.5 | Low |

The confidence label is a system heuristic based on the recommendation matching score.

**Important:** It is not a probability that the user will like the song.

### Graceful Failure Handling

If the system cannot generate recommendations, the reliability layer returns:

```text
Status: No recommendations
Confidence: Low
```

instead of presenting an empty result as a successful recommendation.

## System Architecture

The system follows this workflow:

```text
User Preferences
       |
       v
Input Validation
       |
       v
Preference Check
       |
       v
Music Recommendation Engine
       |
       v
Song Dataset
       |
       v
Scoring and Ranking
       |
       v
Top 5 Recommendations
       |
       v
Reliability Assessment
       |
       v
Confidence Level
       |
       v
Final Output
```

The Mermaid source for the full architecture is available at:

```text
diagrams/architecture.mmd
```

## Project Structure

```text
applied-ai-system-project/
|
|-- assets/
|
|-- data/
|   `-- songs.csv
|
|-- diagrams/
|   `-- architecture.mmd
|
|-- src/
|   |-- main.py
|   |-- recommender.py
|   `-- reliability.py
|
|-- tests/
|   |-- test_recommender.py
|   `-- test_reliability.py
|
|-- ai_interactions.md
|-- model_card.md
|-- README.md
|-- requirements.txt
`-- .gitignore
```

## How the System Works

### 1. Load Data

The system loads song information from:

```text
data/songs.csv
```

### 2. Process User Preferences

Different user profiles contain preferences such as genre, mood, energy level, and acoustic preference.

### 3. Validate Preferences

`src/reliability.py` examines preference values and produces warnings when inputs fall outside the expected ranges or supported categories.

### 4. Score Songs

The recommendation engine compares each song against the user's preferences.

Matching characteristics contribute to the recommendation score.

### 5. Rank Recommendations

Songs are ranked according to their total scores, and the top five are returned.

### 6. Explain Results

The system displays the factors that contributed to each recommendation.

### 7. Assess Reliability

The top recommendation score is passed through the reliability layer and assigned a confidence level of:

```text
High
Medium
Low
```

## Example Run

Run:

```bash
python -m src.main
```

Example output:

```text
PROFILE: High-Energy Pop

RELIABILITY CHECK
Status: Success
Confidence: High
Top recommendation score: 4.89

Note: Confidence is estimated from the recommendation matching score.
It is not a probability of user satisfaction.

1. Storm Runner - Voltline
Genre: rock | Mood: intense
Score: 4.89
Because: genre match (+2.0), mood match (+1.0),
energy similarity (+0.99), less-acoustic preference (+0.90)

2. Gym Hero - Max Pulse
Genre: pop | Mood: intense
Score: 2.92

3. Sunrise City - Neon Echo
Genre: pop | Mood: happy
Score: 1.74
```

Exact recommendations depend on the selected profile and dataset.

## Reliability Examples

### Example 1 — Valid Input

```python
{
    "mood": "happy",
    "genre": "pop",
    "energy": 0.8
}
```

Result:

```text
Input validation: Passed
```

### Example 2 — Invalid Energy

```python
{
    "mood": "happy",
    "genre": "pop",
    "energy": 1.5
}
```

Result:

```text
Reliability Warning:
Energy must be between 0 and 1.
```

### Example 3 — Unknown Preferences

```python
{
    "mood": "super-excited",
    "genre": "space-music",
    "energy": 0.5
}
```

The system identifies the unsupported mood and genre and generates reliability warnings.

## Installation

Clone the repository:

```bash
git clone https://github.com/DhruvPatel05/applied-ai-system-project.git
cd applied-ai-system-project
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the System

From the project root:

```bash
python -m src.main
```

## Running Tests

Run:

```bash
python -m pytest -q
```

Current test suite:

```text
8 passed
```

The tests cover both the original recommendation logic and the new reliability layer.

Reliability tests include:

- Valid preferences
- Invalid energy ranges
- Unknown mood and genre values
- High, medium, and low confidence levels
- Successful reliability summaries
- Empty recommendation handling

## Reliability and Limitations

The reliability layer improves transparency but does not guarantee that a user will enjoy a recommendation.

Current limitations include:

- The dataset is small.
- Preferences are represented using predefined features.
- Confidence is based on recommendation scores rather than calibrated probabilities.
- The system does not learn from real user feedback.
- Musical preferences are subjective and may change over time.
- Unsupported genres or moods may reduce recommendation quality.
- The system does not currently use large-scale behavioral listening history.

Therefore, the confidence label should be interpreted as an indication of how strongly a song matches the configured preference rules, not as certainty about user satisfaction.

## Testing Strategy

The project uses automated tests to verify both recommendation behavior and reliability behavior.

The reliability tests intentionally include edge cases such as:

```text
energy = 1.5
unknown genre
unknown mood
empty recommendation list
```

These tests help ensure that unusual inputs are handled predictably instead of silently producing misleading results.

## Future Improvements

Potential improvements include:

- Larger real-world music datasets
- User feedback collection
- Collaborative filtering
- Embedding-based semantic similarity
- Learned recommendation models
- Calibrated confidence scores
- More detailed uncertainty estimates
- Interactive Streamlit interface
- Spotify or another music API integration

## Responsible AI Considerations

Recommendation systems can influence what users discover and consume.

This system attempts to improve responsible AI behavior by:

- Explaining why recommendations were generated
- Identifying unsupported inputs
- Reporting uncertainty through confidence labels
- Explicitly stating that confidence is not a probability of satisfaction
- Handling empty results gracefully
- Testing known failure and edge cases

The system should be treated as a recommendation aid rather than an authoritative predictor of a person's musical preferences.

## Author

**Dhruv Patel**

AI110 — Foundations of AI Engineering  
Applied AI System Project