import logging
from datetime import datetime
from typing import List

import peewee
import peewee_async

from hackernews.app.config import Config

log = logging.getLogger(__name__)

db = peewee_async.PostgresqlDatabase(
    host=Config.db_host,
    port=Config.db_port,
    database=Config.db_name,
    user=Config.db_user,
    password=Config.db_password,
)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Post(BaseModel):
    title = peewee.CharField(max_length=255, unique=True)
    url = peewee.CharField(max_length=255, unique=True)
    created = peewee.DateTimeField(default=datetime.now, unique=True)

    def __repr__(self):
        return '<Post#%d title=%r, url=%r, create=%r>' % (
            self.id,
            self.title,
            self.url,
            self.created,
        )

    @classmethod
    async def create_post(cls, title: str, url: str):
        post = await objects.get_or_create(
            cls,
            title=title,
            url=url,
        )
        return post

    @classmethod
    async def get_list(
            cls,
            limit: int,
            offset: int,
            order_key: str,
            order_type: str
    ) -> List['Post']:

        fields = {
            'id': Post.id,
            'title': Post.title,
            'url': Post.url,
            'created': Post.created,
        }

        if order_type == 'desc':
            posts = await objects.execute(
                cls.select().order_by(fields[order_key].desc()).limit(limit).offset(offset)
            )
        else:
            posts = await objects.execute(
                cls.select().order_by(fields[order_key]).limit(limit).offset(offset)
            )

        result = []
        for post in posts:
            result.append(post)

        return result


Post.create_table(True)
db.close()

objects = peewee_async.Manager(db)
db.set_allow_sync(False)
