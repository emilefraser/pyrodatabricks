"""Asynchronously get links embedded in multiple pages' HMTL."""

import asyncio
import logging
import re
import sys
from typing import IO
import urllib.error
import urllib.parse

import aiofiles
import aiohttp
from aiohttp import ClientSession, TCPConnector

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True


async def post (url: str, data: dict, session: ClientSession, **kwargs) -> str:
    logger.info(f"Posting to URL={url}")
    try:
        resp = await session.request(method="POST", url=url, data=data, **kwargs)
        resp.raise_for_status()
        logger.info("Got response [%s] for URL: %s", resp.status, url)
        html = await resp.text()
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return None
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
        return None
    else:
        return html

async def broker1(url: str, data: set, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    async with ClientSession() as session:
        tasks = []
        for d in data:
            tasks.append(
                post(url=url, data=d, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)

async def broker2(url: str, data: set, **kwargs) -> None:
    # https://docs.aiohttp.org/en/stable/client_advanced.html
    conn = aiohttp.TCPConnector(
        limit=4,
        enable_cleanup_closed=True,
        ttl_dns_cache=100,
        ssl=False,
    )
    async with ClientSession(connector=conn) as session:
        tasks = []
        for d in data:
            tasks.append(
                post(url=url, data=d, session=session, **kwargs)
            )
        # _ = await asyncio.gather(*tasks)
        for res in asyncio.as_completed(tasks):
            await res


if __name__ == "__main__":
    import pathlib
    import sys

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    here = pathlib.Path(__file__).parent
    url = 'http://localhost:3000/process'
    with open(here.joinpath("source_docs.txt")) as infile:
        source_docs = set(map(str.strip, infile))

    # broker 1
    # asyncio.run(broker1(url=url, data=source_docs))
    
    # broker 2
    loop = asyncio.get_event_loop()
    loop.run_until_complete(broker2(url=url, data=source_docs))
    loop.close()