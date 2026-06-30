# Telegram Group Management Bot

A production-ready Telegram group moderation bot built with **Python 3.12+** and **python-telegram-bot v21+**. It supports muting, unmuting, promoting, and demoting members, with strict permission checks, rate limiting, and action logging.

---

## Features

- Works in any group it's added to.
- Auto-detects whether it has the administrator permissions it needs before acting.
- Only group owners/admins can run moderation commands.
- Clear success and error messages for every action.
- Full action logging (admin, action, target, time, group).
- Rate limiting to prevent command spam/abuse.
- Warning system with configurable auto-mute threshold.
- Timed mutes/bans that auto-expire.
- Anti-spam flood detection, anti-link filter, bad-word filter — all admin-configurable, all persisted in SQLite.
- Join captcha (button tap) to block bot/spam accounts, with auto-kick on timeout.
- Custom welcome message and rules text per group.
- Per-user `/info` lookups and `/stats` activity leaderboard.
- Clean, modular, fully type-hinted, async codebase.

## Commands

### Core moderation
| Command | Description |
|---|---|
| `/start` | Welcome message with command overview |
| `/help` | Detailed command reference |
| `/mute @username` (or reply) | Mute a user — blocks messages, photos, videos, stickers, voice, documents, polls, GIFs |
| `/unmute @username` (or reply) | Restore normal permissions |
| `/promote @username` (or reply) | Promote to admin (delete msgs, pin, invite, manage video chats, restrict members) |
| `/demote @username` (or reply) | Remove all admin privileges |

### Removal
| Command | Description |
|---|---|
| `/kick @username` (or reply) | Remove from group; user can rejoin via invite link |
| `/ban @username` (or reply) | Permanent ban |
| `/unban <user_id>` | Lift a ban (numeric ID required — Telegram can't resolve usernames of users who've left) |
| `/tempmute @username 2h` or reply + `/tempmute 2h` | Mute for a duration (`s`/`m`/`h`/`d`/`w`), auto-unmutes |
| `/tempban @username 1d` or reply + `/tempban 1d` | Ban for a duration, Telegram auto-lifts it |

### Group-wide
| Command | Description |
|---|---|
| `/lock` | Instantly mute the entire group (admins unaffected) |
| `/unlock` | Restore normal default permissions for everyone |

### Warning system
| Command | Description |
|---|---|
| `/warn @username [reason]` (or reply) | Issue a warning; auto-mutes at the configured limit |
| `/warnings @username` (or reply) | Show a user's current warning count |
| `/clearwarnings @username` (or reply) | Reset a user's warnings to zero |
| `/setwarnlimit <n>` | Configure warnings needed before auto-mute (default 3) |

### Auto-filters (admin-configurable, persisted in SQLite)
| Command | Description |
|---|---|
| `/antilink on\|off` | Delete messages containing links from non-admins |
| `/addbadword <word>` | Add a word to the filter (auto-deletes matching messages) |
| `/removebadword <word>` | Remove a word from the filter |
| `/setfloodlimit <n>` | Messages-per-window before auto-mute for spam (default 5 / 5s) |
| `/captcha on\|off` | Require new members to tap a button within 2 minutes or get kicked |

### Community
| Command | Description |
|---|---|
| `/setwelcome <text>` | Set the welcome message; supports `{name}` and `{group}` placeholders |
| `/rules` | Show the group's rules |
| `/setrules <text>` | Configure the rules text |
| `/info [@username]` | Show join date, message count, and warnings for a user (defaults to yourself) |
| `/stats` | Show the 10 most active members |
| `/report` (reply to a message) | Flag a message to all admins |
| `/pin` / `/unpin` (reply to a message) | Pin/unpin a message |

---

## Project Structure

```
telegram_admin_bot/
│── main.py
│── config.py
│── handlers/
│     ├── admin.py          (mute/unmute/promote/demote)
│     ├── moderation.py     (kick/ban/unban/tempmute/tempban/lock/warn)
│     ├── filters.py        (anti-spam, anti-link, bad-words, captcha)
│     ├── community.py      (welcome, rules, info, report, stats, pin)
│     ├── general.py        (start/help)
│── utils/
│     ├── permissions.py
│     ├── logger.py
│     ├── database.py       (SQLite persistence)
│     ├── time_parser.py    (duration parsing for tempmute/tempban)
│── requirements.txt
│── .env.example
│── Dockerfile
│── docker-compose.yml
│── Procfile
│── README.md
```

---

## 1. BotFather Configuration

1. Open Telegram and message **[@BotFather](https://t.me/BotFather)**.
2. Send `/newbot` and follow the prompts to choose a name and a unique username (must end in `bot`).
3. BotFather will give you a **token** — looks like `123456789:AAExampleTokenHere`. Save it.
4. Disable privacy mode so the bot can see all group messages (needed for some moderation flows; optional but recommended):
   - Send `/mybots` → select your bot → **Bot Settings** → **Group Privacy** → **Turn off**.
5. (Optional) Set a description and profile picture via `/setdescription` and `/setuserpic`.
6. (Optional) Register the command list for the in-chat `/` menu via `/setcommands`:
   ```
   start - Show welcome message
   help - Show all commands
   mute - Mute a user
   unmute - Unmute a user
   promote - Promote a user to admin
   demote - Remove admin privileges
   kick - Remove a user (can rejoin)
   ban - Permanently ban a user
   unban - Lift a ban
   tempmute - Mute a user for a duration
   tempban - Ban a user for a duration
   lock - Freeze the whole group
   unlock - Unfreeze the whole group
   warn - Warn a user
   warnings - Show a user's warnings
   clearwarnings - Reset a user's warnings
   setwarnlimit - Set warnings before auto-mute
   antilink - Toggle the link filter
   addbadword - Add a filtered word
   removebadword - Remove a filtered word
   setfloodlimit - Set anti-spam threshold
   captcha - Toggle join captcha
   setwelcome - Set the welcome message
   rules - Show group rules
   setrules - Set group rules
   info - Show info about a user
   stats - Show most active members
   report - Report a message to admins
   pin - Pin a message
   unpin - Unpin a message
   ```

---

## 2. Local Setup

### Prerequisites
- Python 3.12+
- A Telegram bot token from BotFather (above)

### Steps

```bash
# 1. Clone / copy the project, then enter it
cd telegram_admin_bot

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and paste your BOT_TOKEN

# 5. Run the bot
python main.py
```

You should see a log line: `Telegram Group Management Bot starting...`

### Add the bot to a group

1. Open your group → **Add Member** → search your bot's username → add it.
2. Promote the bot to **Administrator** with at least:
   - **Restrict members** (required for `/mute`, `/unmute`)
   - **Promote members** (required for `/promote`, `/demote`)
3. Try `/start` or `/help` in the group.

> The bot will refuse to run moderation commands and reply with `❌ I need administrator permission.` until it has the right admin rights.

---

## 3. Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `BOT_TOKEN` | ✅ | — | Token from BotFather |
| `GRANT_ANONYMOUS_ADMIN` | ❌ | `false` | Whether `/promote` also grants anonymous admin |
| `RATE_LIMIT_SECONDS` | ❌ | `3` | Cooldown between an admin's moderation commands |
| `LOG_FILE` | ❌ | `bot_actions.log` | Path to the action log file |
| `LOG_LEVEL` | ❌ | `INFO` | Logging verbosity |

---

## 4. Deployment Guides

### A. Railway

1. Push this project to a GitHub repository.
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**.
3. Select your repo.
4. Railway auto-detects Python. In **Variables**, add `BOT_TOKEN` (and any optional vars).
5. Under **Settings → Deploy**, set the **Start Command** to `python main.py` (the included `Procfile` also works automatically).
6. Deploy. Check the **Deployments → Logs** tab to confirm `Telegram Group Management Bot starting...` appears.

### B. Render

1. Push this project to GitHub.
2. Go to [render.com](https://render.com) → **New** → **Background Worker** (not Web Service, since this bot uses polling and doesn't serve HTTP).
3. Connect your repo.
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
5. Add environment variable `BOT_TOKEN` under **Environment**.
6. Deploy and check logs for confirmation.

### C. VPS (Ubuntu/Debian example)

```bash
# SSH into your VPS
sudo apt update && sudo apt install -y python3.12 python3.12-venv git

git clone <your-repo-url> telegram_admin_bot
cd telegram_admin_bot

python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env   # paste your BOT_TOKEN

# Run with a process manager so it survives reboots/crashes
sudo apt install -y supervisor
```

Create `/etc/supervisor/conf.d/telegram_admin_bot.conf`:

```ini
[program:telegram_admin_bot]
directory=/home/youruser/telegram_admin_bot
command=/home/youruser/telegram_admin_bot/venv/bin/python main.py
autostart=true
autorestart=true
stderr_logfile=/var/log/telegram_admin_bot.err.log
stdout_logfile=/var/log/telegram_admin_bot.out.log
user=youruser
```

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start telegram_admin_bot
```

(Alternatively, use a `systemd` service or `tmux`/`screen` for simpler setups.)

### D. Docker

```bash
# Build the image
docker build -t telegram-admin-bot .

# Run it (pass your token directly)
docker run -d --name telegram-admin-bot \
  -e BOT_TOKEN=123456789:AAExampleTokenHere \
  --restart unless-stopped \
  telegram-admin-bot
```

Or with **docker-compose** (recommended — reads from `.env`):

```bash
cp .env.example .env
nano .env   # set BOT_TOKEN
docker compose up -d --build
```

Check logs:

```bash
docker compose logs -f
```

---

## 5. How Permission Checks Work

Every moderation command runs this pipeline before doing anything:

1. **Group-only** — commands are ignored in private chats.
2. **Rate limit** — admin must wait `RATE_LIMIT_SECONDS` between commands.
3. **Bot permission** — bot must be an admin with the specific permission needed (`can_restrict_members` for mute/unmute, `can_promote_members` for promote/demote).
4. **Issuer permission** — command sender must be an admin or the owner.
5. **Target resolution** — via reply or `@username`.
6. **Target safety** — target can't be the bot itself, the group owner, or (for mute/promote) another admin with equal/higher privileges.

If any check fails, a clear, specific error message is sent — e.g.:

```
❌ Only admins can use this command.
❌ I need administrator permission.
❌ I cannot mute the group owner.
❌ User not found.
❌ I cannot modify an admin with higher privileges.
```

## 6. Logging

Every successful moderation action is appended to `bot_actions.log` (and stdout) in this format:

```
Admin: @owner
Action: Mute
Target: @username
Time: 30-06-2026 10:45 PM
Group: My Group
```

## 7. Limitations & Notes

- Telegram's Bot API does not let bots resolve an arbitrary `@username` to a user ID unless that user is already a cached chat member. If `/mute @username` reports "User not found," **reply to the user's message instead** — this always works reliably.
- `/unmute` restores a sensible default permission set; it does not memorize each group's original custom permissions (Telegram's API doesn't expose a per-user permission history).
- Anonymous admin is **off by default** on `/promote`; enable via `GRANT_ANONYMOUS_ADMIN=true` if desired.
- All settings (warnings, rules, welcome message, filters) are stored in `bot_data.db` (SQLite), created automatically on first run in the project directory. Back this file up if you care about retaining warnings/config across redeploys — it is **not** included in Docker images or git by default (see `.gitignore`).
- Flood detection and captcha state are kept in memory and reset on bot restart; this is intentional and avoids unnecessary DB writes for high-frequency, short-lived data.

## 8. License

Free to use and modify for your own projects.
