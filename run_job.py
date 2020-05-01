import asyncio
import logging

from hackernews.app.parser import run_parse

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

if __name__ == '__main__':
    log.info('Starting job parser hackernews')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_parse())
