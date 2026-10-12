import aiohttp
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from db.models import Subscription
import json

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

async def search_anime(query):
    url = f"https://tsuzuki.top/api/v1/search?q={query}"

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

async def subscribe(anime_id, user_id):

    anime_name = await getAnimeName(anime_id)

    if anime_name is None:
        return "Failed to get the Anime name."

    last_notified_ep = await getLastNotifiedEp(anime_id)

    if last_notified_ep is None:
        last_notified_ep = 0

    is_finished = await check_finished_airing(anime_id)

    if is_finished:
        return "This anime has already finished airing. Nothing to notify you about. 😭"

    subscription_found = Subscription.get_or_none(
        user_id=user_id,
        anime_id=anime_id
    )

    if subscription_found:
        return "You're already subscribed to this anime! 📺"

    Subscription.create(
        user_id=user_id,
        anime_name=anime_name,
        anime_id=anime_id,
        last_notified_ep=last_notified_ep
    )

    return f'''"{anime_name}" has been added to your notifications! ✅

📺 Last episode released: {last_notified_ep}'''

async def getTodaysAiringAnime():
    url = "https://tsuzuki.top/api/v1/schedule?days=1&airType=sub"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    animeList = data["episodes"]

    responseToSend = ""

    for anime in animeList:
        airing_time = datetime.fromisoformat(anime["airingAtIso"].replace("Z", "+00:00"))

        airing_time = airing_time.astimezone(ZoneInfo("Asia/Kolkata"))

        formatted_time = airing_time.strftime("%d %B, %I:%M %p")

        responseToSend += (
            f"{anime['title']} | "
            f"Episode: {anime['episode']} | "
            f"At: {formatted_time}\n\n"
        )

    return responseToSend

async def getNextEpisodeDetails(anime_id):
    url = f"https://tsuzuki.top/api/v1/anime/{anime_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    now = datetime.now(timezone.utc).timestamp()

    upcoming = [
        ep for ep in data["episodes"]
        if ep["airType"] == "sub"
        and ep["airingAt"] > now
    ]

    if not upcoming:
        return None

    next_ep = upcoming[0]

    release_time = datetime.fromtimestamp(
        next_ep["airingAt"],
        tz=ZoneInfo("Asia/Kolkata")
    )

    return {
        "episode": next_ep["episode"],
        "release_time": release_time.strftime(
            "%d %B %Y at %I:%M %p"
        )
    }


async def getAnimeDetails(anime_id):
    url = f"https://tsuzuki.top/api/v1/anime/{anime_id}?full=1"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return {"error": f"API returned status {response.status}"}

            data = await response.json()

    try:
        anime = data["media"]
        title = anime.get("title", {})

        return {
            "id": anime["id"],
            "title": title.get("english") or title.get("romaji"),
            "description": anime.get("description"),
            "genres": anime.get("genres", []),
            "episodes": anime.get("episodes"),
            "status": anime.get("status"),
            "format": anime.get("format"),
            "average_score": anime.get("averageScore"),
            "cover_image": anime.get("coverImage", {}).get("large"),
            "site_url": anime.get("siteUrl")
        }

    except (KeyError, TypeError, AttributeError):
        return {"error": "Could not parse the anime details returned by the API."}
