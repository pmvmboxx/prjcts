import requests
from wordfreq import word_frequency

# Free Dictionary API - no key required
DICT_API = "https://api.dictionaryapi.dev/api/v2/entries/en/"

# Common words to skip (too basic to be useful)
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "is", "it", "be", "as",
    "was", "are", "were", "been", "has", "have", "had", "do", "did",
    "does", "not", "no", "so", "if", "up", "out", "he", "she",
    "we", "you", "me", "my", "his", "her", "its", "our", "your",
    "they", "them", "their", "i", "that", "this", "what", "which",
    "who", "how", "when", "where", "will", "would", "could", "should",
    "can", "may", "might", "just", "like", "get", "got", "go",
    "went", "come", "came", "said", "say", "know", "think", "see",
    "look", "want", "make", "made", "take", "took", "give", "gave",
    "one", "two", "all", "some", "more", "than", "then", "there",
    "here", "about", "after", "before", "into", "over", "also",
    "back", "him", "us", "let", "way", "very"
}

ADVANCED_THRESHOLD = 1e-5


def is_worth_learning(word: str) -> bool:
    """Return True if a word is advanced enough to be worth defining."""
    if word in STOPWORDS or len(word) < 4:
        return False
    freq = word_frequency(word, 'en')
    return freq < ADVANCED_THRESHOLD


def fetch_definition(word: str) -> dict | None:
    """
    Fetch a word's definition from the free dictionary API.
    Returns dict with word, part of speech, definition, example — or None.
    """
    try:
        response = requests.get(DICT_API + word, timeout=5)
        if response.status_code != 200:
            return None

        data = response.json()
        entry = data[0]
        meanings = entry.get('meanings', [])
        if not meanings:
            return None

        meaning = meanings[0]
        definitions = meaning.get('definitions', [])
        if not definitions:
            return None

        definition = definitions[0]

        return {
            'word': word,
            'part_of_speech': meaning.get('partOfSpeech', ''),
            'definition': definition.get('definition', ''),
            'example': definition.get('example', ''),
        }
    except Exception:
        return None


def get_vocab_list(unique_words: list[str], max_words: int = 10) -> list[dict]:
    """
    Filter words worth learning, fetch their definitions.
    Returns up to max_words defined words.
    """
    candidates = [w for w in unique_words if is_worth_learning(w)]

    # Sort by rarity (least frequent first = most advanced)
    candidates.sort(key=lambda w: word_frequency(w, 'en'))

    results = []
    for word in candidates:
        if len(results) >= max_words:
            break
        definition = fetch_definition(word)
        if definition:
            results.append(definition)

    return results
