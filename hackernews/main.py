from aiohttp import web

from hackernews.app.handlers import routes_app


def create_app():
    app = web.Application()
    app.router.add_routes(routes_app)
    return app
