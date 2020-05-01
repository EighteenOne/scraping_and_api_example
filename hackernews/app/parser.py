import asyncio
import logging

import aiohttp
from bs4 import BeautifulSoup

from hackernews.app.config import Config
from hackernews.app.models import Post

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


async def extract_posts(html: str):
    """
    Extracting posts from html by searching for the 'storylink' class
    Args:
        html: text from site

    Returns: filling the database with Post objects

    """
    soup = BeautifulSoup(html, 'html.parser')
    content_area = soup.findAll("a", {"class": "storylink"})
    log.info('Found %d posts on page', len(content_area))

    for el in content_area:
        title = el.text
        url = el['href']

        log.debug('%s %s %s', title, url, el)
        await Post.create_post(title, url)


async def run_parse():
    """
    Run parse process with aiohttp client session
    """
    url = Config.hackernews_url

    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html_str = await response.text()

                    await extract_posts(html_str)
        except aiohttp.ClientError:
            log.exception('Connection error')
        except Exception:
            log.exception('Something went wrong')

        log.info('Sleep on 10 min')
        await asyncio.sleep(600)
