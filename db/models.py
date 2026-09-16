from playhouse.db_url import connect
from peewee import *

from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DB_URL")

db = connect(DB_URL)

class User(Model):
    user_id = BigIntegerField(primary_key=True)
    f_name = CharField()
    l_name = CharField(null=True)

    class Meta:
        database = db
        table_name = "users"


class Subscription(Model):
    user_id = ForeignKeyField(User, backref="subscriptions")
    anime_name = CharField()
    anime_id = IntegerField()
    last_notified_ep = IntegerField(default=0)

    class Meta:
        database = db
        table_name = "subscriptions"