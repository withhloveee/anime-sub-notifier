from db.models import db, Subscription, User
from tools import  getLastNotifiedEp


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