import logging

from aiohttp import web

from hackernews.app.config import Config
from hackernews.main import create_app

log = logging.getLogger(__name__)


def run():
    log.info('Starting http api')
    app = create_app()

    try:
        web.run_app(
            app=app,
            port=Config.listen_port,
        )
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()
