import logging

import aiohttp

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


async def json_request(url: str) -> dict:
    """
    Makes a request to the URL and returns the decoded JSON.

    :param url: A string.
    :return: A dictionary of the decoded JSON.
    """
    async with aiohttp.ClientSession() as session:
        logger.debug(f"Requesting {url}")
        async with session.get(url) as response:
            logger.debug(f"Status: {response.status}")
            logger.debug(f"Content-type: {response.headers['content-type']}")
            json = await response.json()
    return json
