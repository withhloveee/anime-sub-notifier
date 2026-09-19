from dotenv import load_dotenv
import os

from telegram.ext import Application, CommandHandler

#Import: Commands
from handlers.start import start
from handlers.subscribe import subscribe

#Import: Timer
from jobs.timer import timer

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

if __name__ == "__main__":

    app = Application.builder().token(API_TOKEN).build()

    app.job_queue.run_repeating(
        timer,
        interval=60,
        job_kwargs={
            "misfire_grace_time": 60
        }
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sub", subscribe))

    app.run_polling()