import logging
from aiohttp import web
from ai_trading_bot.application import __version__
async def hello(request):
    return web.Response(text=f"Hello, world __version__: {__version__}")

app = web.Application()
app.router.add_get('/', hello)
