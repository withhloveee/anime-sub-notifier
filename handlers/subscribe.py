from db.models import Subscription
from tools import getAnimeName, getLastNotifiedEp

async def subscribe(update, context):
    try:
        anime_id = context.args[0]
    except:
        await update.message.reply_text("No animeId was provided.")
        return
    
    user_id = update.effective_user.id
    anime_name = await getAnimeName(anime_id)
    last_notified_ep = await getLastNotifiedEp(anime_id)


    user = Subscription.get_or_none(
        user_id=user_id,
        anime_id=anime_id
    )

    if user:
        await update.message.reply_text("You're already subscribed to this anime! 📺")
    else:
        Subscription.create(
            user_id=user_id,
            anime_name=anime_name,
            anime_id=anime_id,
            last_notified_ep=last_notified_ep
        )
        await update.message.reply_text(f'''"{anime_name}" has been added to your notifications! ✅\n\n📺 Last episode released: {last_notified_ep}''')