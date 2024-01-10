"""
This module provides functionality for extracting and processing job vacancies data.
It utilizes JSON files, processes data using GPT-based models, and creates a formatted list of vacancies.
"""

import asyncio
import json

from bot_files.constants import VACANCIES_JSON_FILE
from bot_files.parse_hh import process_vacancies


async def extract_vacancies_data() -> dict:
    """
    Extracts job vacancies data from a JSON file.

    :return: A dictionary containing job vacancies data.
    """
    return await extract_data_from_json(VACANCIES_JSON_FILE)


async def extract_data_from_json(file_path: str) -> dict:
    """
    Extracts data from a JSON file given the file path.

    :param file_path: The path to the JSON file.
    :return: A dictionary containing the extracted data.
    """
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


async def create_vacancies_list() -> str:
    """
    Creates a formatted list of job vacancies.

    :return: A formatted string containing the list of job vacancies.
    """
    vacancies_data = await extend_vacancies_data()
    return '\n\n'.join(vacancies_data)


async def reduce_and_append_description(data: dict):
    """
    Reduces and appends descriptions of job vacancies using GPT-based models.

    :param data: A dictionary containing job vacancies data.
    :return: The reduced and appended description.
    """
    from bot_files.gpt_module import gpt_api
    return await gpt_api.reduce_vacancy_description(data)


async def extend_vacancies_data():
    """
    Extends job vacancies data by processing and enhancing descriptions.

    :return: A list containing the extended job vacancies data.
    """
    vacancies_data = await extract_vacancies_data()
    await process_vacancies(vacancies_data)
    vacancies_list = await asyncio.gather(
        *map(reduce_and_append_description, vacancies_data)
    )
    return vacancies_list
