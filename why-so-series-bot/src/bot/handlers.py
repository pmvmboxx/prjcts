import os
import tempfile
from recommendations_service import get_random_series, format_series
from learning_post import build_learning_post


def register_handlers(bot):

    # ──────────────────────────────────────────
    # /start
    # ──────────────────────────────────────────
    @bot.message_handler(commands=['start'])
    def start(message):
        name = message.from_user.first_name
        bot.send_message(
            message.chat.id,
            f"👋 Hi, *{name}*! Welcome to *Why So Series Bot* 🎬🍿\n\n"
            f"What can I do for you?\n\n"
            f"📺 */recommend* — Get a random series\n"
            f"🎭 */genres* — Browse by genre\n"
            f"📖 */learn* — Upload a .srt subtitle file to get an English learning post\n"
            f"❓ */help* — Show all commands",
            parse_mode='Markdown'
        )

    # ──────────────────────────────────────────
    # /help
    # ──────────────────────────────────────────
    @bot.message_handler(commands=['help'])
    def help_cmd(message):
        bot.send_message(
            message.chat.id,
            "🆘 *Available commands:*\n\n"
            "/start — Welcome message\n"
            "/recommend — Get a random series recommendation\n"
            "/genres — See all available genres\n"
            "/learn — Upload a .srt file and get a learning post\n"
            "/help — Show this message",
            parse_mode='Markdown'
        )

    # ──────────────────────────────────────────
    # /recommend
    # ──────────────────────────────────────────
    @bot.message_handler(commands=['recommend'])
    def recommend(message):
        series = get_random_series()
        bot.send_message(
            message.chat.id,
            "🍿 Here's your recommendation:\n\n" + format_series(series),
            parse_mode='Markdown'
        )

    # ──────────────────────────────────────────
    # /genres
    # ──────────────────────────────────────────
    @bot.message_handler(commands=['genres'])
    def genres(message):
        genre_list = get_all_genres()
        genres_text = "\n".join(f"• {g.capitalize()}" for g in genre_list)
        bot.send_message(
            message.chat.id,
            f"🎭 *Available genres:*\n\n{genres_text}\n\n"
            f"_Genre filtering with buttons coming in the next update!_",
            parse_mode='Markdown'
        )

    # ──────────────────────────────────────────
    # /learn — prompt user to upload .srt
    # ──────────────────────────────────────────
    @bot.message_handler(commands=['learn'])
    def learn(message):
        bot.send_message(
            message.chat.id,
            "📂 Send me a *.srt* subtitle file and I'll generate an English learning post for you!\n\n"
            "_Tip: You can find .srt files on sites like OpenSubtitles.org_",
            parse_mode='Markdown'
        )

    # ──────────────────────────────────────────
    # Handle .srt file uploads
    # ──────────────────────────────────────────
    @bot.message_handler(content_types=['document'])
    def handle_document(message):
        doc = message.document

        # Check file extension
        if not doc.file_name.endswith('.srt'):
            bot.reply_to(
                message,
                "⚠️ Please send a *.srt* subtitle file.\n"
                "_Other formats are not supported yet._",
                parse_mode='Markdown'
            )
            return

        # Check file size (max 2MB)
        if doc.file_size > 2 * 1024 * 1024:
            bot.reply_to(message, "⚠️ File is too large. Please send a file under 2MB.")
            return

        # Let user know we're working on it
        processing_msg = bot.reply_to(message, "⏳ Processing your subtitle file...")

        try:
            # Download file from Telegram
            file_info = bot.get_file(doc.file_id)
            downloaded = bot.download_file(file_info.file_path)

            # Save to temp file
            with tempfile.NamedTemporaryFile(suffix='.srt', delete=False) as tmp:
                tmp.write(downloaded)
                tmp_path = tmp.name

            # Use filename (minus extension) as the title
            title = doc.file_name.replace('.srt', '').replace('.', ' ').replace('_', ' ').strip()

            # Build the learning post
            post = build_learning_post(tmp_path, title=title)

            # Clean up temp file
            os.unlink(tmp_path)

            # Delete the "processing" message
            bot.delete_message(message.chat.id, processing_msg.message_id)

            # Send the learning post
            bot.send_message(
                message.chat.id,
                post,
                parse_mode='Markdown'
            )

        except Exception as e:
            bot.edit_message_text(
                f"❌ Something went wrong while processing your file.\n_Error: {str(e)}_",
                message.chat.id,
                processing_msg.message_id,
                parse_mode='Markdown'
            )

    # ──────────────────────────────────────────
    # Catch-all for unknown messages
    # ──────────────────────────────────────────
    @bot.message_handler(func=lambda message: True)
    def unknown(message):
        bot.send_message(
            message.chat.id,
            "🤔 I don't understand that. Use /help to see what I can do!"
        )
