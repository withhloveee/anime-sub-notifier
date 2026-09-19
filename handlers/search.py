from tools import search_api

async def search(update,context):
    try:
        anime_name = context.args[0]
    except:
        await update.message.reply_text("No search query was provided?")
        return

    results = await search_api(anime_name)

    await update.message.reply_text(results)