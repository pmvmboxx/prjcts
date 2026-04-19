import re


def parse_srt(file_path: str) -> str:
    """Read a .srt file and return clean plain text (no timestamps or indices)."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Remove index numbers (lines that are just digits)
    content = re.sub(r'^\d+$', '', content, flags=re.MULTILINE)

    # Remove timestamps like 00:01:23,456 --> 00:01:25,789
    content = re.sub(r'\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}', '', content)

    # Remove HTML tags like <i>, <b>, <font ...>
    content = re.sub(r'<[^>]+>', '', content)

    # Remove special subtitle formatting like {\an8}
    content = re.sub(r'\{[^}]+\}', '', content)

    # Collapse multiple blank lines
    content = re.sub(r'\n{2,}', '\n', content)

    return content.strip()


def extract_words(text: str) -> list[str]:
    """Extract all individual lowercase words from text."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return [w.lower() for w in words]


def extract_unique_words(text: str) -> list[str]:
    """Return a sorted list of unique lowercase words."""
    return sorted(set(extract_words(text)))


def get_word_frequency(text: str) -> dict[str, int]:
    """Return a dict of word -> count, sorted by frequency descending."""
    words = extract_words(text)
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
