from subtitle_parser import parse_srt, extract_unique_words
from level_detection import detect_level
from idioms import find_idioms
from vocab import get_vocab_list


def build_learning_post(file_path: str, title: str = "this episode") -> str:
    """
    Full pipeline: .srt file → formatted learning post string.
    """

    # Step 1 — Parse subtitle file
    text = parse_srt(file_path)
    unique_words = extract_unique_words(text)

    # Step 2 — Detect level
    level_data = detect_level(unique_words)

    # Step 3 — Find idioms
    idioms_found = find_idioms(text)

    # Step 4 — Get vocab with definitions
    vocab = get_vocab_list(unique_words, max_words=8)

    # Step 5 — Format the post
    lines = []

    lines.append(f"🎬 *{title}* — English Learning Post\n")

    # Level section
    lines.append(f"📊 *Recommended Level:* {level_data['level']}")
    lines.append(
        f"📝 Unique words: {level_data['total_unique_words']} "
        f"| Advanced: {level_data['advanced_pct']}% "
        f"| Intermediate: {level_data['intermediate_pct']}%\n"
    )

    # Vocabulary section
    if vocab:
        lines.append("📚 *Useful Vocabulary:*")
        for item in vocab:
            word_line = f"• *{item['word']}* _{item['part_of_speech']}_"
            if item['definition']:
                word_line += f"\n  ↳ {item['definition']}"
            if item['example']:
                word_line += f"\n  💬 _{item['example']}_"
            lines.append(word_line)
        lines.append("")

    # Idioms section
    if idioms_found:
        lines.append("💡 *Phrases & Idioms Found:*")
        for idiom in idioms_found[:6]:  # Cap at 6
            lines.append(f"• *{idiom['phrase']}*\n  ↳ {idiom['meaning']}")
        lines.append("")

    if not vocab and not idioms_found:
        lines.append("_No advanced vocabulary or idioms detected in this file._\n")

    lines.append("🚀 Keep learning through stories!")

    return "\n".join(lines)
