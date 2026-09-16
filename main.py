from dotenv import load_dotenv
import os

from db.models import User, Subscription
from telegram.ext import Application, CommandHandler

import requests
from tools import getAnimeName, getLastNotifiedEp

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Commands
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

    await update.message.reply_text("You are now registered!")


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

    users = User.select()

    for user in users:

        user_id = user.user_id

        await context.bot.send_message(
            chat_id=user_id,
            text="10s reminder here!"
        )

if __name__ == "__main__":

    app = Application.builder().token(API_TOKEN).build()

    app.job_queue.run_repeating(
        timer,
        interval=30
    )

    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("sub", subscribe))
    app.run_polling()