# FORiskMatch

This repository contains a simple Discord bot that can simulate games using the Friends of Risk open API.

## Requirements
- Python 3.8+
- `discord.py` and `aiohttp`

Install dependencies with:

```bash
pip install discord.py aiohttp
```

## Running
Set the `DISCORD_TOKEN` environment variable to your bot token and run:

```bash
python riskmatch_bot.py
```

Use the command `!match` followed by 2-6 Discord user mentions in any channel the bot can read. The bot will start a new thread and post each round until the game is completed.
