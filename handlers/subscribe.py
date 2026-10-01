from db.models import Subscription
from tools import getAnimeName, getLastNotifiedEp, check_finished_airing

async def subscribe(update, context):
    #check: if any message was sent with /sub command.
    try:
        anime_id = context.args[0]
    except:
        await update.message.reply_text("No animeId was provided.")
        return
    
    user_id = update.effective_user.id
    anime_name = await getAnimeName(anime_id)

    #probably the anime_id was not send as expected.
    if anime_name is None:
        await update.message.reply_text("Hmm... we couldn't find that anime.\n\nDid you provide anime_Id correctly?")
        return

    last_notified_ep = await getLastNotifiedEp(anime_id)
    
    if last_notified_ep is None:
        # No episode has aired yet
        last_notified_ep = 0

    is_finished = await check_finished_airing(anime_id)

    if is_finished is None:
        await update.message.reply_text("Hmm... we couldn't find that anime. :<\n\nSomething to do with airing issues.")
        return

    if is_finished:
        await update.message.reply_text("This anime has already finished airing. Nothing to notify you about. 😭")
        return

    anime_found = Subscription.get_or_none(
        user_id=user_id,
        anime_id=anime_id
    )

    if anime_found:
        await update.message.reply_text("You're already subscribed to this anime! 📺")
    else:
        Subscription.create(
            user_id=user_id,
            anime_name=anime_name,
            anime_id=anime_id,
            last_notified_ep=last_notified_ep
        )
        await update.message.reply_text(f'''"{anime_name}" has been added to your notifications! ✅\n\n📺 Last episode released: {last_notified_ep}''')