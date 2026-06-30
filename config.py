"""
config.py
---------
Central configuration for the Telegram Group Management Bot.

All sensitive values (like BOT_TOKEN) are loaded from environment
variables so the bot can be safely deployed to Railway, Render, a VPS,
or Docker without hardcoding secrets in source code.

Create a `.env` file (see .env.example) or set environment variables
directly on your hosting platform.
"""

import os
from dotenv import load_dotenv

# Load variables from a local .env file if present (no-op in production
# environments where env vars are injected by the platform).
load_dotenv()

# ---------------------------------------------------------------------
# Core bot settings
# ---------------------------------------------------------------------

# Telegram Bot token obtained from @BotFather. REQUIRED.
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

# Whether promoted admins should also be granted "anonymous admin"
# status (i.e. messages appear as "Group Name" instead of the user).
# Per requirements, this is OFF by default.
GRANT_ANONYMOUS_ADMIN: bool = os.getenv("GRANT_ANONYMOUS_ADMIN", "false").lower() == "true"

# ---------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------

# Minimum number of seconds an individual admin must wait between
# consecutive moderation commands (mute/unmute/promote/demote).
RATE_LIMIT_SECONDS: float = float(os.getenv("RATE_LIMIT_SECONDS", "3"))

# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------

# Path to the log file that records every moderation action.
LOG_FILE: str = os.getenv("LOG_FILE", "bot_actions.log")

# Logging verbosity for the root logger (DEBUG, INFO, WARNING, ERROR).
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# ---------------------------------------------------------------------
# Sanity check
# ---------------------------------------------------------------------

if not BOT_TOKEN:
    # We don't raise here so that `config.py` can still be imported by
    # tools/tests without a token set, but main.py will refuse to start.
    pass
