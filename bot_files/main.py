"""
This module contains the main functionality for a Telegram bot, including handlers for various commands,
information retrieval, and interaction with the GPT API.
"""

import asyncio

from aiogram.dispatcher.filters import IDFilter
from aiogram.types import Message

from bot_files.gpt_module import gpt_api
from config import dp, bot, ADMINISTRATORS
from constants import *


async def start(message: Message):
    """
    Handle the /start command by sending a welcome message.

    :param message: Message object representing the incoming message.
    """
    await message.reply(WELCOME_START_MESSAGE)


@dp.message_handler(IDFilter(ADMINISTRATORS), commands=[CMD_GET_INFO])
async def get_info(message: Message):
    """
    Handle the /get_info command (accessible only to administrators) by retrieving information
    about the current hackathon and sending it as a reply.

    :param message: Message object representing the incoming message.
    """
    current_info_text: str = await retrieve_hackathon_info()
    await message.answer(CURRENT_HACKATHON_DATA.format(current_info_text))


@dp.message_handler(IDFilter(ADMINISTRATORS), commands=[CMD_SET_INFO])
async def set_info(message: Message):
    """
    Handle the /set_info command (accessible only to administrators) by extracting new information
    from the message text and updating the hackathon information file.

    :param message: Message object representing the incoming message.
    """
    new_info = message.text.removeprefix(f"/{CMD_SET_INFO}").strip()
    await update_hackathon_info(new_info)


async def free_written_text_handler(message: Message):
    """
    Handle free-written text messages by sending them to the GPT API and responding with the generated content.

    :param message: Message object representing the incoming message.
    """
    msg = await message.answer(WAIT_FOR_RESPONSE)
    await bot.send_chat_action(message.chat.id, 'typing')
    response = await gpt_api.request_to_api(message.text)
    await msg.edit_text(response)


async def retrieve_hackathon_info() -> str:
    """
    Retrieve hackathon information from the hackathon information file.

    :returns: The content of the hackathon information file.
    """
    with open(HACKATHON_INFO_FILE, 'r', encoding='utf-8') as file:
        return file.read()


async def update_hackathon_info(new_info: str) -> None:
    """
    Update the hackathon information file with new information.

    :param new_info: New information to be added to the hackathon information file.
    """
    with open(HACKATHON_INFO_FILE, 'w', encoding='utf-8') as file:
        file.write(new_info)


async def set_commands():
    """
    Set custom commands for the bot, specifically for administrators.
    """
    await bot.delete_my_commands()
    from aiogram.types import BotCommandScopeChat
    for admin_id in ADMINISTRATORS:
        await bot.set_my_commands(ADMINS_COMMANDS, scope=BotCommandScopeChat(admin_id))


async def on_bot_startup():
    """
    Perform necessary actions when the bot starts, including setting commands,
    creating a list of vacancies, and updating the GPT API prompt content.
    """
    await set_commands()
    from bot_files.vacancies import create_vacancies_list
    vacancies = await create_vacancies_list()
    new_info = await retrieve_hackathon_info() + vacancies
    gpt_api.prompt_content = new_info


def main():
    """
    Main function to launch the bot. Initializes the event loop, sets up commands, and starts the polling.
    """
    from aiogram.utils import executor
    loop = asyncio.new_event_loop()
    asyncio.run(on_bot_startup())
    asyncio.set_event_loop(loop)
    executor.start_polling(dp, loop=loop, skip_updates=True)


if __name__ == '__main__':
    main()
