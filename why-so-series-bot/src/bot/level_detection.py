from wordfreq import word_frequency

# Thresholds based on wordfreq scores
# word_frequency returns a float between 0 and 1
# More common words have higher scores

BEGINNER_THRESHOLD = 1e-4      # very common words (the, go, eat)
INTERMEDIATE_THRESHOLD = 1e-5  # moderately common
# Below intermediate = advanced


def classify_word(word: str) -> str:
    """Classify a single word as beginner, intermediate, or advanced."""
    freq = word_frequency(word, 'en')
    if freq >= BEGINNER_THRESHOLD:
        return 'beginner'
    elif freq >= INTERMEDIATE_THRESHOLD:
        return 'intermediate'
    else:
        return 'advanced'


def detect_level(unique_words: list[str]) -> dict:
    """
    Analyse a list of unique words and return:
    - overall level label
    - breakdown counts
    - percentage of advanced words
    """
    counts = {'beginner': 0, 'intermediate': 0, 'advanced': 0}

    for word in unique_words:
        level = classify_word(word)
        counts[level] += 1

    total = len(unique_words) or 1
    advanced_pct = counts['advanced'] / total * 100
    intermediate_pct = counts['intermediate'] / total * 100

    if advanced_pct >= 30:
        overall = 'Advanced (C1–C2)'
    elif advanced_pct >= 15 or intermediate_pct >= 30:
        overall = 'Intermediate (B1–B2)'
    else:
        overall = 'Beginner (A1–A2)'

    return {
        'level': overall,
        'breakdown': counts,
        'advanced_pct': round(advanced_pct, 1),
        'intermediate_pct': round(intermediate_pct, 1),
        'total_unique_words': total,
    }
