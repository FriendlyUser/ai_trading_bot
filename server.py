import asyncio
import aiohttp

from ai_trading_bot.server import app

async def start_monitoring():
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner)    
    await site.start()

if __name__ == '__main__':
    asyncio.run(start_monitoring())
