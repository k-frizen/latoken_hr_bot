"""
This module provides functions for fetching and processing vacancy information. It utilizes the 'parse_hh_data'
module to download vacancy information based on provided vacancy IDs.
"""

import asyncio
from parse_hh_data import download
from requests import HTTPError

from bot_files.config import logger
from bot_files.constants import EXTRACTED_VACANCIES_FIELDS


async def fetch_vacancy_info(_id: str) -> dict:
    """
    Asynchronously fetches and downloads information for a given vacancy ID.

    :param _id: The ID of the vacancy.
    :returns: Information about the vacancy.
    """

    try:
        assert _id.isnumeric()
        return download.vacancy(_id)
    except (AssertionError, HTTPError):
        logger.error('Incorrect vacancy id %s', _id, exc_info=True)
        return {}


async def process_vacancies(vacancies_data: dict):
    """
    Asynchronously processes a list of vacancies by fetching detailed information for each.

    :param vacancies_data: A list of vacancies with basic information.
    """
    tasks = []
    for _vacancy in vacancies_data:
        link: str = _vacancy['link']
        _id = link.split('/')[-1]
        tasks.append(fetch_vacancy_info(_id))

    vacancy_infos = await asyncio.gather(*tasks)
    for vacancy_info, _vacancy in zip(vacancy_infos, vacancies_data):
        for field in EXTRACTED_VACANCIES_FIELDS:
            _vacancy[field] = vacancy_info.get(field, "Field not available")
        if not vacancy_info:
            logger.error('Error fetching data for vacancy: %s', _vacancy['title'])

