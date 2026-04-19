import random

series = [
    {
        "title": "Breaking Bad",
        "genre": "drama",
        "description": "A chemistry teacher turns into a drug kingpin.",
        "imdb": 9.5
    },
    {
        "title": "Dark",
        "genre": "sci-fi",
        "description": "Time travel and mysterious disappearances in a German town.",
        "imdb": 8.7
    },
    {
        "title": "The Office",
        "genre": "comedy",
        "description": "A mockumentary about everyday office life.",
        "imdb": 8.9
    },
    {
        "title": "Sherlock",
        "genre": "mystery",
        "description": "A modern take on the classic detective Sherlock Holmes.",
        "imdb": 9.1
    },
    {
        "title": "Stranger Things",
        "genre": "sci-fi",
        "description": "Kids face supernatural forces in a small town.",
        "imdb": 8.7
    },
    {
        "title": "Chernobyl",
        "genre": "drama",
        "description": "The true story of the 1986 nuclear disaster.",
        "imdb": 9.4
    },
]


def get_random_series():
    """Return a random series from the list."""
    return random.choice(series)


def get_series_by_genre(genre: str):
    """Return a random series filtered by genre."""
    filtered = [s for s in series if s["genre"] == genre.lower()]
    if filtered:
        return random.choice(filtered)
    return None


def get_all_genres():
    """Return a sorted list of unique genres."""
    return sorted(set(s["genre"] for s in series))


def format_series(s: dict) -> str:
    """Format a series dict into a nice message string."""
    return (
        f"🎬 *{s['title']}*\n"
        f"🎭 Genre: {s['genre'].capitalize()}\n"
        f"📖 {s['description']}\n"
        f"⭐ IMDb: {s['imdb']}"
    )
