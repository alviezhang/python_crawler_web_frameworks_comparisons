import asyncio
import os
from operator import itemgetter
from urllib.parse import parse_qs

import aiohttp
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from starlette.routing import Route

_connector = aiohttp.TCPConnector(ttl_dns_cache=300, limit=10000)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def single_database_query(request):
    seconds = 3
    url = f'http://192.168.10.18:8090/?seconds={seconds}'
    async with aiohttp.ClientSession(connector=_connector, connector_owner=False) as session:
        body = await fetch(session, url)
    return UJSONResponse(body)


async def multiple_database_queries(request):
    seconds = 1.5
    body_list = []

    url = f'http://192.168.10.18:8090/?seconds={seconds}'
    async with aiohttp.ClientSession(connector=_connector, connector_owner=False) as session:
        body = await fetch(session, url)
    body_list.append(body)

    url = f'http://192.168.10.18:8090/?seconds={seconds}'
    async with aiohttp.ClientSession(connector=_connector, connector_owner=False) as session:
        body = await fetch(session, url)
    body_list.append(body)

    return UJSONResponse('\n'.join(body_list))


routes = [
        Route('/single', single_database_query),
        Route('/multiple', multiple_database_queries),
        ]

app = Starlette(routes=routes)
