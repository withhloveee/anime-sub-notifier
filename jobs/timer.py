from db.models import db, Subscription, User
from tools import  getLastNotifiedEp, getAnimeCoverImage,getNextEpisode


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

                if recent_ep is not None and recent_ep != last_ep:

                    next_ep_time = await getNextEpisode(anime_id)

                    if next_ep_time:
                        caption = f'''📺{anime_name}\n\n🎉 Episode {recent_ep} just dropped.\n\n📅 Next episode:\n{next_ep_time} IST'''
                    else:
                        caption = f'''"📺{anime_name}\n\n🎉 Episode {recent_ep} just dropped.'''
                    
                    await context.bot.send_photo(
                        chat_id=user_id,
                        photo= await getAnimeCoverImage(anime_id),
                        caption=caption
                    )

                    subscription.last_notified_ep = recent_ep
                    subscription.save()