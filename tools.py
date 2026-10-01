import aiohttp
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

async def getAnimeName(anime_id):
    url = f"https://tsuzuki.top/api/v1/anime/{anime_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    try:
        title = data["anime"]["title"]
        return title["english"] or title["romaji"]
    except:
        return None

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

async def search_api(anime_id):
    url = f"https://tsuzuki.top/api/v1/search?q={anime_id}"

    async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()

    try:
        ListOfResults = data["anime"]

        if not ListOfResults:
            return None

        output = ""
        for match in ListOfResults:
            title = match["title"]

            if title.get("english"):
                output += title["english"]
            else:
                output += title["romaji"]

            output += "\n"
            output += "id: " + str(match["id"])
            output += "\n\n"

        return output
    except:
        return None

async def check_finished_airing(anime_id):
    url = f"https://tsuzuki.top/api/v1/anime/{anime_id}"
     
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    try:
        last_ep_airing_time = data.get("episodes")[-1]["airingAt"]
    except (TypeError, IndexError, KeyError):
        #failed to determine due to API issues (probably anime is too old).
        return None
    
    now = datetime.now(timezone.utc).timestamp()

    return last_ep_airing_time < now