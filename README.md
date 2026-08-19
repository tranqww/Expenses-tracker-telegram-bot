# Expenses Tracker Telegram Bot

A simple Telegram bot for tracking personal expenses. Add expenses by category, list them, and see your running total, all from a Telegram chat.

Built with [aiogram 3](https://docs.aiogram.dev/) and stores data locally in a JSON file.

## Features

- **Add expenses** with a guided category → amount flow (`/add`)
- **List all expenses** by category (`/list`)
- **Total up** everything you've spent (`/total`)
- Persists data to `expenses.json` so it survives bot restarts

## Commands

| Command  | Description                                      |
|----------|---------------------------------------------------|
| `/start` | Greets the user and gives a quick intro           |
| `/add`   | Starts a conversation to add a new expense         |
| `/list`  | Shows every recorded expense and its category      |
| `/total` | Calculates and shows the total amount spent        |

## Requirements

- Python 3.10+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

## Setup

1. Clone the repository and move into it:
   ```bash
   git clone <repo-url>
   cd Expenses-tracker-telegram-bot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your bot token:
   ```
   BOT_TOKEN=your-telegram-bot-token-here
   ```

## Running the bot

```bash
python main.py
```

The bot starts long-polling Telegram for updates. On first run it creates an empty `expenses.json` file next to `main.py`; every added expense is appended and saved there.

## Project structure

```
main.py                  # Bot entry point, handlers, and expense storage logic
telegram_api_check.py    # Standalone script to check Telegram API reachability
requirements.txt         # Python dependencies
expenses.json            # Local data store (created automatically on first run)
```

## License

MIT — see [LICENSE](LICENSE).
