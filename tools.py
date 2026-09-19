import aiohttp
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

async def getAnimeName(anime_id):
    url = f"https://tsuzuki.top/api/v1/anime/{anime_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    title = data["anime"]["title"]
    return title["english"] or title["romaji"]

async def getLastNotifiedEp(anime_id):
    url = f"https://tsuzuki.top/api/v1/anime/{anime_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    now = datetime.now(timezone.utc).timestamp()

    aired = [
        ep for ep in data["episodes"]
        if ep["airType"] == "sub" and ep["airingAt"] <= now
    ]

    if not aired:
        return None

    return aired[-1]["episode"]

async def getNextEpisode(anime_id):
    url = f"https://tsuzuki.top/api/v1/anime/{anime_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    now = datetime.now(timezone.utc).timestamp()

    upcoming = [
        ep for ep in data["episodes"]
        if ep["airType"] == "sub" and ep["airingAt"] > now
    ]

    if not upcoming:
        return None

    next_ep = upcoming[0]

    release_time = datetime.fromtimestamp(
        next_ep["airingAt"],
        tz=ZoneInfo("Asia/Kolkata")
    )

    return release_time.strftime("%d %B %Y at %I:%M %p")

async def getAnimeCoverImage(anime_id):
    url = f"https://tsuzuki.top/api/v1/anime/{anime_id}"

    async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

    return data["anime"]["coverImage"]["large"]