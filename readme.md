# anime-sub-notifier

A small Telegram bot that pings you when a new episode of an anime you follow comes out. I got tired of checking release dates by hand, so I made this.

There are no commands to learn. Just talk to it.

## How to use it

Send `/start` to the bot, then type whatever you want:

- `subscribe me to frieren s3`
- `what's airing today?`
- `anything airing tomorrow?`
- or just send an anime name and it'll look it up

If more than one anime matches, it shows you the options and asks which one you meant. Once you pick, you're subscribed, and it messages you when a new episode drops.

## How it works

- An AI model (through OpenRouter) reads your message and decides what to do, like searching, subscribing, or checking the schedule
- All the anime data (search, air times, schedule) comes from the [Tsuzuki API](https://tsuzuki.top/api)
- A background job checks for new episodes every 30 minutes and sends the notifications
- Your subscriptions are saved in a database so they survive restarts

## Setup

You'll need Python 3.10+, a Telegram bot token (get one from [@BotFather](https://t.me/BotFather)), and an [OpenRouter](https://openrouter.ai/) API key.

```bash
git clone https://github.com/withhloveee/anime-sub-notifier.git
cd anime-sub-notifier
pip install -r requirements.txt
```

Make a `.env` file in the project folder:

```
TELEGRAM_API_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_key
DB_URL=your_database_url
```

Uses peewee ORM, so Postgres, MySQL or SQLite URLs all work. I use Postgres.

Then run it:

```bash
python main.py
```

## How it's laid out

```
main.py      starts the bot and sets up the 30 min timer
handlers/    /start and message handling
jobs/        the repeating episode check
db/          saving what each user follows
ai/          the AI prompt and tool definitions
tools.py     the functions the AI can call (Tsuzuki API requests)
```

## Notes

- It uses long polling (as of today)
- The check runs every 1800 seconds, you can change `interval` in `main.py`
- Anime data is from [tsuzuki.top](https://tsuzuki.top/), all credit to them