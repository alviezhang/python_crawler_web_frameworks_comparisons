import uvloop

uvloop.install()

import os
from parse import parse_chinese_name

import aiohttp
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from starlette.routing import Route

GO_SLEEP_ADDRESS = os.getenv('GO_SLEEP_ADDRESS', '127.0.0.1:8090')
_connector = aiohttp.TCPConnector(ttl_dns_cache=300, limit=10000, keepalive_timeout=30)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def single_database_query(request):
    seconds = 3
    url = f'http://{GO_SLEEP_ADDRESS}/?seconds={seconds}'
    async with aiohttp.ClientSession(connector=_connector, connector_owner=False) as session:
        body = await fetch(session, url)

    return UJSONResponse([body] + parse_chinese_name())


async def multiple_database_queries(request):
    seconds = 1.5
    body_list = []

    url = f'http://{GO_SLEEP_ADDRESS}/?seconds={seconds}'
    async with aiohttp.ClientSession(connector=_connector, connector_owner=False) as session:
        body = await fetch(session, url)
    body_list.append(body)

    url = f'http://{GO_SLEEP_ADDRESS}/?seconds={seconds}'
    async with aiohttp.ClientSession(connector=_connector, connector_owner=False) as session:
        body = await fetch(session, url)
    body_list.append(body)

    return UJSONResponse('\n'.join(body_list))


routes = [
    Route('/single', single_database_query),
    Route('/multiple', multiple_database_queries),
]

app = Starlette(routes=routes)
