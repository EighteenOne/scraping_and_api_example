import asyncio
import logging

import peewee_async
import pytest
from aiohttp.test_utils import loop_context

from hackernews.app import config
from hackernews.app.models import Post
from hackernews.main import create_app

log = logging.getLogger(__name__)

pytest_plugins = 'aiohttp.pytest_plugin'

TEST_POSTS = [
    {'created': '2020-05-01T00:16:22.281146',
     'id': 1,
     'title': 'Test 1',
     'url': 'https://test1.com'},
    {'created': '2020-05-01T00:16:22.306465',
     'id': 2,
     'title': 'Test 2',
     'url': 'https://test2.com'},
    {'created': '2020-05-01T00:16:22.312315',
     'id': 3,
     'title': 'Test 3',
     'url': 'https://test3.com'},
    {'created': '2020-05-01T00:16:22.317698',
     'id': 4,
     'title': 'Test 4',
     'url': 'https://test4.com'},
    {'created': '2020-05-01T00:16:22.322895',
     'id': 5,
     'title': 'Test 5',
     'url': 'https://test5.com'},
    {'created': '2020-05-01T00:16:22.328525',
     'id': 6,
     'title': 'Test 6',
     'url': 'https://test6.com'},
    {'created': '2020-05-01T00:16:22.334072',
     'id': 7,
     'title': 'Test 7',
     'url': 'https://test7.com'},
    {'created': '2020-05-01T00:16:22.339197',
     'id': 8,
     'title': 'Test 8',
     'url': 'https://test8.com'},
    {'created': '2020-05-01T00:16:22.344538',
     'id': 9,
     'title': 'Test 9',
     'url': 'https://test9.com'},
    {'created': '2020-05-01T00:16:22.350241',
     'id': 10,
     'title': 'Test 10',
     'url': 'https://test10.com'}
]


@pytest.yield_fixture(scope='session', autouse=True)
def loop():
    with loop_context() as loop:
        asyncio.set_event_loop(loop)
        yield loop


@pytest.fixture()
async def api_client(aiohttp_client):
    """Base fixture for starting app and getting aiohttp client"""
    app = create_app()
    client = await aiohttp_client(app)

    yield client


@pytest.fixture(scope='session')
def database():
    db = peewee_async.PostgresqlDatabase(
        host=config.Config.db_host,
        port=config.Config.db_port,
        database=config.Config.db_name,
        user=config.Config.db_user,
        password=config.Config.db_password,
    )
    yield db


@pytest.fixture
async def db_without_data(database, loop):
    database.set_allow_sync(True)
    Post._meta.database = database
    db = peewee_async.Manager(database, loop=loop)

    Post.truncate_table(True)
    database.set_allow_sync(False)

    yield db

    await db.close()

    database.set_allow_sync(True)
    Post.truncate_table(True)


@pytest.fixture(scope='session')
async def db_with_10_posts(database, loop):
    Post._meta.database = database
    Post.create_table(True)

    db = peewee_async.Manager(database, loop=loop)

    Post.truncate_table(True)
    database.set_allow_sync(False)

    for test_post in TEST_POSTS:
        await db.create(Post, **test_post)

    yield db

    await db.close()

    database.set_allow_sync(True)
    Post.drop_table(True)


@pytest.fixture
def html_15_items_test():
    """Html example from https://news.ycombinator.com/ page with cleared content"""
    with open('tests/resources/hackernews_15_items.html', 'r') as f:
        html_test = f.read()

    return html_test
