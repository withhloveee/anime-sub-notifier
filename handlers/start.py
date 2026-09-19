from db.models import User

async def start(update,context):

    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name

    User.get_or_create(
        user_id=user_id,
        defaults={
            "f_name": first_name,
            "l_name": last_name
        }
    )

    text = """
Hii! 👋✨

Want to get notified whenever a new episode drops?
It's super easy! 

1️⃣ /register

First, register yourself so I know where to send your notifications. 😊

2️⃣ /sub <animeID>

Example:
/sub 182205

Just replace 182205 with the animeID of the anime you want to follow.

And you're all set! 🎉

I'll let you know whenever a new episode drops. 🔔

Now go enjoy your anime~ 🍿✨
"""
    await update.message.reply_text(text)