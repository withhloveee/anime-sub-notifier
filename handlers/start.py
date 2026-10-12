from db.models import User, db

async def start(update, context):

    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name

    with db.connection_context():
        User.get_or_create(
            user_id=user_id,
            defaults={
                "f_name": first_name,
                "l_name": last_name
            }
        )

    text = """
Hey there, human!👋

I'm your little companion.

You can talk to me about anime, ask me to find something to watch, or subscribe to an anime and I'll keep an eye out for new episodes for you.

Try asking me things like:

• "Subscribe me to Frieren"
• "What anime are airing today?"
• "When is the next episode of Black Clover S2 coming out?"

I'll handle the rest.?
"""

    await update.message.reply_text(text)