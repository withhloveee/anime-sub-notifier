import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

#import: handlers
from handlers.start import start
from handlers.messages import handle_message

from jobs.timer import timer

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

if __name__ == "__main__":

    app = Application.builder().token(API_TOKEN).build()

    app.job_queue.run_repeating(
        timer,
        interval=1800,
        job_kwargs={
            "misfire_grace_time": 60
        }
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()