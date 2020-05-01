import logging

import peewee
from aiohttp import web

from hackernews.app import views
from hackernews.app.models import Post

log = logging.getLogger(__name__)

routes_app = web.RouteTableDef()

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 5
DEFAULT_ORDER_KEY = 'id'
DEFAULT_ORDER_TYPE = 'asc'

AVAILABLE_PARAMS = {'offset', 'limit', 'order'}
AVAILABLE_ORDER_KEYS = {'id', 'title', 'url', 'created'}
AVAILABLE_ORDER_TYPES = {'asc', 'desc'}


def _validate_init_params(query_params):
    """
    Validate and initialize request query params
    Args:
        query_params:

    Returns: limit, offset, order_key, order_type

    """
    if (AVAILABLE_PARAMS | set(query_params.keys())) != AVAILABLE_PARAMS:
        raise web.HTTPBadRequest(text=f'Available params: {AVAILABLE_PARAMS}')

    try:
        offset = int(query_params.get('offset', DEFAULT_OFFSET))
        limit = int(query_params.get('limit', DEFAULT_LIMIT))

        assert 0 <= offset <= 30
        assert 0 <= limit <= 30

    except (ValueError, AssertionError):
        raise web.HTTPBadRequest(text='Limit and offset value must be in range 0..30')

    order_key = query_params.get('order', DEFAULT_ORDER_KEY)
    order_type = DEFAULT_ORDER_TYPE

    if order_key.count(':') > 1:
        raise web.HTTPBadRequest(text='Many order type in one order key')

    if ':' in order_key:
        order_key, order_type = order_key.split(':')

    if order_key not in AVAILABLE_ORDER_KEYS:
        raise web.HTTPBadRequest(text='Order key not available')

    if order_type not in AVAILABLE_ORDER_TYPES:
        raise web.HTTPBadRequest(text='Order type must be asc or desc')

    return limit, offset, order_key, order_type


@routes_app.get('/posts')
async def get_posts(request: web.Request) -> web.Response:
    """
    Getting posts from db with applying query params
    Args:
        request: aiohttp request

    Returns:
        List with posts
    """
    query_params = request.rel_url.query
    limit, offset, order_key, order_type = _validate_init_params(query_params)

    try:
        posts = await Post.get_list(
            limit=limit,
            offset=offset,
            order_key=order_key,
            order_type=order_type
        )
        result = views.json_posts(posts)

        return web.json_response(result)
    except peewee.DatabaseError:
        return web.HTTPServerError(text='Something went wrong')
