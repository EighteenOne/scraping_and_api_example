import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    db_host = os.environ.get('POSTGRES_HOST')
    db_port = os.environ.get('POSTGRES_PORT')
    db_name = os.environ.get('APP_DB_NAME')
    db_user = os.environ.get('APP_DB_USER')
    db_password = os.environ.get('APP_DB_PASSWORD')

    hackernews_url = os.environ.get('HACKERNEWS_URL', 'https://news.ycombinator.com/')

    listen_port = os.environ.get('LISTEN_PORT', 8080)
