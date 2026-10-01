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
<b>Welcome 👋</b>

Just follow the instructions below. They're simple enough.

━━━━━━━━━━━━━━━━━

<b>📌 HOW TO SUBSCRIBE</b>

<b>1️⃣ Search for your anime</b>

Use:
<code>/search &lt;anime_name&gt;</code>

Example:
<code>/search Frieren</code>

<b>2️⃣ Find the anime you want</b>

The bot will show you the search results.
Each result will have an Anime ID.

<b>3️⃣ Subscribe</b>

Copy the Anime ID and use:

<code>/sub &lt;anime_ID&gt;</code>

Example:
<code>/sub 12345</code>

<b>✅ That's it!</b> You'll now receive notifications
when a new episode is released.
"""

    await update.message.reply_text(text, parse_mode="HTML")