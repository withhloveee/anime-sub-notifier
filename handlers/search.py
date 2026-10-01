from tools import search_api

async def search(update,context):
    try:
        anime_name = context.args[0]
    except:
        await update.message.reply_text("No search query was provided?")
        return

    results = await search_api(anime_name)

    if results is None:
        await update.message.reply_text("Hmm... are you sure that's an anime? :<\n\nTry searching for an anime title.")
        return

    await update.message.reply_text(results)