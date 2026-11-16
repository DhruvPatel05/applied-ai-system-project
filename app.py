import streamlit as st

from src.recommender import load_songs, recommend_songs
from src.reliability import validate_preferences, reliability_summary


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="VibeMatch",
    page_icon="🎧",
    layout="wide",
)


# ---------------------------------------------------------
# THEME
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Main app background */
    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(124, 58, 237, 0.16), transparent 28%),
            radial-gradient(circle at 85% 15%, rgba(6, 182, 212, 0.12), transparent 30%),
            linear-gradient(135deg, #070B14 0%, #0B1120 55%, #0F172A 100%);
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    /* Typography */
    h1 {
        font-size: 3.3rem !important;
        font-weight: 850 !important;
        letter-spacing: -2px;
        background: linear-gradient(90deg, #A78BFA, #67E8F9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h2, h3 {
        color: #F8FAFC !important;
    }

    p, label {
        color: #CBD5E1;
    }

    /* Hero */
    .hero-subtitle {
        font-size: 1.2rem;
        color: #94A3B8;
        margin-top: -12px;
        margin-bottom: 8px;
    }

    .hero-description {
        color: #CBD5E1;
        max-width: 760px;
        font-size: 1rem;
        line-height: 1.7;
    }

    /* Preset buttons */
    div[data-testid="stButton"] button {
        border-radius: 12px;
        min-height: 46px;
        font-weight: 650;
        transition: all 0.2s ease;
    }

    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.20);
    }

    /* Primary recommendation button */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(90deg, #7C3AED, #0891B2);
        color: white;
        border: 0;
    }

    /* Inputs */
    [data-baseweb="select"] > div {
        background: rgba(15, 23, 42, 0.90);
        border-color: rgba(148, 163, 184, 0.20);
        border-radius: 12px;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.70);
        border: 1px solid rgba(103, 232, 249, 0.14);
        border-radius: 16px;
        padding: 18px;
    }

    [data-testid="stMetricLabel"] {
        color: #94A3B8;
    }

    [data-testid="stMetricValue"] {
        color: #F8FAFC;
    }

    /* Recommendation cards */
    .song-card {
        background: linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.94),
            rgba(30, 41, 59, 0.72)
        );
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 18px;
        padding: 22px 24px;
        margin: 14px 0;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
    }

    .top-song {
        border: 1px solid rgba(167, 139, 250, 0.55);
        background:
            linear-gradient(
                145deg,
                rgba(76, 29, 149, 0.24),
                rgba(8, 145, 178, 0.12)
            );
    }

    .song-number {
        color: #67E8F9;
        font-size: 0.82rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .song-title {
        color: #F8FAFC;
        font-size: 1.35rem;
        font-weight: 750;
        margin-top: 5px;
    }

    .song-meta {
        color: #94A3B8;
        margin-top: 7px;
    }

    .score {
        display: inline-block;
        background: rgba(124, 58, 237, 0.20);
        border: 1px solid rgba(167, 139, 250, 0.30);
        color: #C4B5FD;
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: 700;
        margin-top: 10px;
    }

    .explanation {
        color: #CBD5E1;
        margin-top: 13px;
        line-height: 1.6;
    }

    /* Confidence badges */
    .confidence-high {
        display: inline-block;
        background: rgba(16, 185, 129, 0.13);
        border: 1px solid rgba(52, 211, 153, 0.35);
        color: #6EE7B7;
        padding: 7px 13px;
        border-radius: 30px;
        font-weight: 750;
    }

    .confidence-medium {
        display: inline-block;
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(251, 191, 36, 0.30);
        color: #FCD34D;
        padding: 7px 13px;
        border-radius: 30px;
        font-weight: 750;
    }

    .confidence-low {
        display: inline-block;
        background: rgba(148, 163, 184, 0.12);
        border: 1px solid rgba(148, 163, 184, 0.30);
        color: #CBD5E1;
        padding: 7px 13px;
        border-radius: 30px;
        font-weight: 750;
    }

    hr {
        border-color: rgba(148, 163, 184, 0.14);
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------

songs = load_songs("data/songs.csv")


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

defaults = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.70,
    "acoustic": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def apply_preset(genre, mood, energy, acoustic):
    st.session_state.genre = genre
    st.session_state.mood = mood
    st.session_state.energy = energy
    st.session_state.acoustic = acoustic


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.title("🎧 VibeMatch")

st.markdown(
    '<div class="hero-subtitle">Find your next vibe.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-description">
    A reliable AI music recommendation system that matches songs
    to your mood and preferences, explains why each song was selected,
    and reports how confident the match is.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()


# ---------------------------------------------------------
# QUICK PRESETS
# ---------------------------------------------------------

st.subheader("Quick Vibes")

p1, p2, p3, p4 = st.columns(4)

with p1:
    if st.button("⚡ Workout", use_container_width=True):
        apply_preset("rock", "intense", 0.90, False)
        st.rerun()

with p2:
    if st.button("🌙 Chill", use_container_width=True):
        apply_preset("lofi", "chill", 0.35, True)
        st.rerun()

with p3:
    if st.button("🎉 Happy", use_container_width=True):
        apply_preset("pop", "happy", 0.80, False)
        st.rerun()

with p4:
    if st.button("🌌 Night Drive", use_container_width=True):
        apply_preset("synthwave", "moody", 0.75, False)
        st.rerun()

st.divider()


# ---------------------------------------------------------
# USER PREFERENCES
# ---------------------------------------------------------

st.subheader("Your Preferences")

left, right = st.columns(2, gap="large")

with left:

    genre = st.selectbox(
        "Favorite Genre",
        [
            "pop",
            "lofi",
            "rock",
            "ambient",
            "jazz",
            "synthwave",
            "indie pop",
        ],
        key="genre",
    )

    mood = st.selectbox(
        "Favorite Mood",
        [
            "happy",
            "chill",
            "intense",
            "relaxed",
            "moody",
            "focused",
        ],
        key="mood",
    )

with right:

    energy = st.slider(
        "Energy Level",
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        key="energy",
    )

    acoustic = st.checkbox(
        "I prefer acoustic music",
        key="acoustic",
    )


user_preferences = {
    "favorite_genre": genre,
    "favorite_mood": mood,
    "target_energy": energy,
    "prefers_acoustic": acoustic,
}

validation_preferences = {
    "genre": genre,
    "mood": mood,
    "energy": energy,
}


st.write("")

recommend = st.button(
    "✨ Find My Vibe",
    type="primary",
    use_container_width=True,
)


# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------

if recommend:

    is_valid, warnings = validate_preferences(
        validation_preferences
    )

    if warnings:
        for warning in warnings:
            st.warning(warning)

    recommendations = recommend_songs(
        user_preferences,
        songs,
        k=5,
    )

    summary = reliability_summary(recommendations)

    st.divider()

    st.subheader("Reliability Assessment")

    m1, m2 = st.columns(2)

    with m1:
        st.metric(
            "Top Match Score",
            summary.get("top_score", "N/A"),
        )

    with m2:

        confidence = summary["confidence"]

        css_class = {
            "High": "confidence-high",
            "Medium": "confidence-medium",
            "Low": "confidence-low",
        }.get(confidence, "confidence-low")

        icon = {
            "High": "●",
            "Medium": "●",
            "Low": "●",
        }.get(confidence, "●")

        st.markdown(
            f"""
            **Confidence**

            <span class="{css_class}">
            {icon} {confidence}
            </span>
            """,
            unsafe_allow_html=True,
        )

    st.caption(summary["message"])

    st.divider()

    st.subheader("Your Recommendations")

    if not recommendations:
        st.info("No recommendations were generated.")

    for index, recommendation in enumerate(
        recommendations,
        start=1,
    ):

        song, score, explanation = recommendation

        top_class = " top-song" if index == 1 else ""
        label = "🏆 Top Match" if index == 1 else f"#{index}"

        st.markdown(
            f"""
            <div class="song-card{top_class}">
                <div class="song-number">{label}</div>

                <div class="song-title">
                    {song['title']} — {song['artist']}
                </div>

                <div class="song-meta">
                    {song['genre'].title()} &nbsp;•&nbsp;
                    {song['mood'].title()}
                </div>

                <div class="score">
                    Match Score {score:.2f}
                </div>

                <div class="explanation">
                    <strong>Why this song?</strong><br>
                    {explanation}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "VibeMatch confidence represents the strength of the preference "
    "match. It is not a probability that you will enjoy a song."
)