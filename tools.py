import aiohttp
from datetime import datetime, timezone

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

    return aired[-1]["episode"]