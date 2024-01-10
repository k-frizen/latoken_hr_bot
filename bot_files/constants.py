from aiogram.types import BotCommand

CMD_VACANCIES: str = "vacancies"
CMD_GET_INFO: str = "get_info"
CMD_SET_INFO: str = "set_info"

ADMINS_COMMANDS = [
    BotCommand(command=CMD_GET_INFO, description="Receive hackathon info"),
    BotCommand(command=CMD_SET_INFO, description="Update hackathon info"),
]

# wordings
WELCOME_START_MESSAGE = "Hello! Welcome to the hackathon registration bot. I'll help you to provide all neccesary information!"
CURRENT_HACKATHON_DATA = 'Current hackathon text data is:\n\n<code>{}</code>\n\n' \
                         f'You should send <code>/{CMD_SET_INFO}</code> and updated info as single message.'
INFO_IS_CHANGED = 'Hackathon data has been updated!'
WAIT_FOR_RESPONSE = 'Please, wait few seconds. Your response has been generating'
VACANCIES_TEXT = "We are looking for:\n\n{}"

# prompts
REDUCE_VACANCY_DESCRIPTION_PROMPT = """ссылка на вакансию обязательно должна быть в ответе. 
Сгенерируй из данной информации короткое описание на 1-2 абзаца максимум, сохраняя ключевые детали включая заголовок."""

# FILES
HACKATHON_INFO_FILE = 'hackathon_info.txt'
VACANCIES_JSON_FILE = 'vacancies_data.json'

# head hunter
EXTRACTED_VACANCIES_FIELDS = "employment", "experience", "key_skills", "languages", "salary"
