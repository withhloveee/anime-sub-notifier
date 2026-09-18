from dotenv import load_dotenv
import os

from db.models import User, Subscription, db
from telegram.ext import Application, CommandHandler

import requests
from tools import getAnimeName, getLastNotifiedEp

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Commands
async def start(update,contet):
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

async def register(update, context):

    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name

    user, created = User.get_or_create(
        user_id=user_id,
        defaults={
            "f_name": first_name,
            "l_name": last_name
        }
    )

    if created == False:
        await update.message.reply_text("It was found that you are already registered.")
    else:
        await update.message.reply_text("You are now successfully registered.")

async def subscribe(update, context):
    try:
        anime_id = context.args[0]
    except:
        await update.message.reply_text("No animeId was provided.")
        return
    
    user_id = update.effective_user.id
    anime_name = await getAnimeName(anime_id)
    last_notified_ep = await getLastNotifiedEp(anime_id)

    print(anime_id)
    print(user_id)

    Subscription.create(
        user_id=user_id,
        anime_name=anime_name,
        anime_id=anime_id,
        last_notified_ep=last_notified_ep
    )

    await update.message.reply_text(f'''"{anime_name}" has been added to your notifications! ✅\n\n📺 Last episode released: {last_notified_ep}''')

async def timer(context):

    print("timer was called...")

    with db.connection_context():

        users = User.select()
           
        for user in users:
            user_id = user.user_id

            for subscription in user.subscriptions:
                anime_id = subscription.anime_id
                anime_name = subscription.anime_name
                last_ep = subscription.last_notified_ep

                recent_ep = await getLastNotifiedEp(anime_id)

                if recent_ep != last_ep:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=f'''"{anime_name}"\n\nEpisode number:{recent_ep} just dropped!'''
                )
                    subscription.last_notified_ep = recent_ep
                    subscription.save()

if __name__ == "__main__":

    app = Application.builder().token(API_TOKEN).build()

    app.job_queue.run_repeating(
        timer,
        interval=600,
        job_kwargs={
            "misfire_grace_time": 60
        }
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("sub", subscribe))
    app.run_polling()