# Expenses Tracker Telegram Bot

A simple Telegram bot for tracking personal expenses. Add expenses by category, list them, and see your running total, all from a Telegram chat.

Built with [aiogram 3](https://docs.aiogram.dev/) and stores data locally in a SQLite database.

## Features

- **Add expenses** with a guided category → amount flow (`/add`)
- **List all expenses** by category (`/list`)
- **Total up** everything you've spent (`/total`)
- Tracks expenses per user, so multiple people can use the same bot without their data mixing
- Persists data to `expenses.db` so it survives bot restarts

## Commands

| Command  | Description                                      |
|----------|---------------------------------------------------|
| `/start` | Greets the user and gives a quick intro           |
| `/add`   | Starts a conversation to add a new expense         |
| `/list`  | Shows every recorded expense and its category      |
| `/total` | Calculates and shows the total amount spent        |
| `/help`  | Show all commands                                  |

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