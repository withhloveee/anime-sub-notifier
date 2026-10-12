import os
import json
from dotenv import load_dotenv
from openrouter import OpenRouter

from tools import search_anime,subscribe,getNextEpisodeDetails,getTodaysAiringAnime,getAnimeDetails

load_dotenv()

MODEL = "openai/gpt-6-luna"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
client = OpenRouter(api_key=OPENROUTER_API_KEY)

with open("ai/system_prompt.txt","r") as f:
    SYSTEM_PROMPT = f.read()

with open("ai/tool_definitions.json", "r") as f:
    tools = json.load(f)

async def execute_tool(tool_call, user_id):
    "Run the tool AI asked for"

    tool_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    if tool_name == "search_anime":
        print("Searching:", arguments["query"])

        return await search_anime(arguments["query"]) or "No anime was found."

    elif tool_name == "subscribe":
        anime_id = arguments["anime_id"]

        print("Subscribing:", anime_id)

        return await subscribe(anime_id, user_id)

    elif tool_name == "getNextEpisodeDetails":
        return await getNextEpisodeDetails(arguments["anime_id"])

    elif tool_name == "getTodaysAiringAnime":
        return await getTodaysAiringAnime()
    
    elif tool_name == "getAnimeDetails":
        return await getAnimeDetails((arguments["anime_id"]))

    return f"Unknown tool: {tool_name}"

async def handle_message(update, context):

    user_message = update.message.text
    user_id = update.effective_user.id

    if "history" not in context.user_data:
        context.user_data["history"] = [{"role": "system", "content": SYSTEM_PROMPT}]

    history = context.user_data["history"]

    #safety: don't let the history grow forever
    if len(history) > 20:
        history[:] = history[:1]

    history.append({"role": "user", "content": user_message})

    poster_url = None
    while True:
        response = client.chat.send(
                model=MODEL,
                messages=history,
                tools=tools,
            )
        message = response.choices[0].message
        history.append(message)

        if not message.tool_calls:
            break
        
        for tool_call in message.tool_calls:
            result = await execute_tool(tool_call, user_id)

            if tool_call.function.name == "getAnimeDetails":
                if isinstance(result, dict):
                    poster_url = result.get("cover_image")

            history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    reply = message.content or "Sorry, something went wrong."
    if poster_url:
        try:
            await update.message.reply_photo(
                photo=poster_url,
                caption=reply[:1024]
            )

            # Send remaining text if the caption was too long
            if len(reply) > 1024:
                await update.message.reply_text(reply[1024:])

        except Exception as e:
            print(f"Failed to send poster: {e}")
            await update.message.reply_text(reply)

    else:
        await update.message.reply_text(reply)