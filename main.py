"""
main.py
-------
Entry point for the Telegram Group Management Bot.

Run with:
    python main.py

Requires BOT_TOKEN to be set in the environment (or a .env file).
"""

from __future__ import annotations

import sys

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers.admin import (
    demote_command,
    mute_command,
    promote_command,
    unmute_command,
)
from handlers.community import (
    addbadword_command,
    antilink_command,
    captcha_command,
    info_command,
    pin_command,
    removebadword_command,
    report_command,
    rules_command,
    setfloodlimit_command,
    setrules_command,
    setwarnlimit_command,
    setwelcome_command,
    stats_command,
    unpin_command,
)
from handlers.filters import on_captcha_button, on_group_message, on_new_member
from handlers.general import help_command, start_command
from handlers.moderation import (
    ban_command,
    clearwarnings_command,
    kick_command,
    lock_command,
    tempban_command,
    tempmute_command,
    unban_command,
    unlock_command,
    warn_command,
    warnings_command,
)
from utils.database import init_db
from utils.logger import logger


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Global error handler so a single failed update never crashes the
    bot process. Logs full details for debugging.
    """
    logger.error("Unhandled exception while processing update %s", update, exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ An unexpected error occurred while processing your request."
            )
        except Exception:
            # If we can't even send the error message, just log it.
            logger.error("Failed to notify user about the error.")


def build_application() -> Application:
    """Construct and configure the python-telegram-bot Application."""
    application = Application.builder().token(BOT_TOKEN).build()

    # General commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # Core moderation commands
    application.add_handler(CommandHandler("mute", mute_command))
    application.add_handler(CommandHandler("unmute", unmute_command))
    application.add_handler(CommandHandler("promote", promote_command))
    application.add_handler(CommandHandler("demote", demote_command))

    # Extended moderation commands
    application.add_handler(CommandHandler("kick", kick_command))
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("tempmute", tempmute_command))
    application.add_handler(CommandHandler("tempban", tempban_command))
    application.add_handler(CommandHandler("lock", lock_command))
    application.add_handler(CommandHandler("unlock", unlock_command))
    application.add_handler(CommandHandler("warn", warn_command))
    application.add_handler(CommandHandler("warnings", warnings_command))
    application.add_handler(CommandHandler("clearwarnings", clearwarnings_command))

    # Community / configuration commands
    application.add_handler(CommandHandler("setwelcome", setwelcome_command))
    application.add_handler(CommandHandler("rules", rules_command))
    application.add_handler(CommandHandler("setrules", setrules_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("report", report_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("pin", pin_command))
    application.add_handler(CommandHandler("unpin", unpin_command))
    application.add_handler(CommandHandler("antilink", antilink_command))
    application.add_handler(CommandHandler("addbadword", addbadword_command))
    application.add_handler(CommandHandler("removebadword", removebadword_command))
    application.add_handler(CommandHandler("setwarnlimit", setwarnlimit_command))
    application.add_handler(CommandHandler("setfloodlimit", setfloodlimit_command))
    application.add_handler(CommandHandler("captcha", captcha_command))

    # Passive moderation: flood / anti-link / bad-word filters + stats,
    # runs on every non-command group message (text or captioned media).
    application.add_handler(
        MessageHandler(
            filters.ChatType.GROUPS & (filters.TEXT | filters.CAPTION) & ~filters.COMMAND,
            on_group_message,
        )
    )

    # New member captcha / welcome message.
    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_new_member)
    )

    # Captcha "I'm not a robot" button presses.
    application.add_handler(CallbackQueryHandler(on_captcha_button, pattern=r"^captcha:"))

    # Global error handler
    application.add_error_handler(error_handler)

    return application


def main() -> None:
    if not BOT_TOKEN:
        logger.error(
            "BOT_TOKEN is not set. Create a .env file or set the "
            "BOT_TOKEN environment variable before starting the bot."
        )
        sys.exit(1)

    init_db()

    application = build_application()

    logger.info("Telegram Group Management Bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
