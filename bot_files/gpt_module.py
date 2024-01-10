import json

import openai

from config import OPEN_AI_KEY, logger


class OpenAI:
    openai.api_key = OPEN_AI_KEY
    MODEL_ENGINE = "gpt-3.5-turbo"

    def __init__(self):
        self._prompt_content = ""

    @property
    def prompt_content(self) -> str:
        return self._prompt_content

    @prompt_content.setter
    def prompt_content(self, new_prompt_content: str):
        if isinstance(new_prompt_content, str):
            self._prompt_content = new_prompt_content
        else:
            logger.error('Incorrect data type %s', type(new_prompt_content))

    async def request_to_api(self, user_request: str) -> bool:
        try:
            response = openai.ChatCompletion.create(
                model=self.MODEL_ENGINE,
                messages=[
                    {"role": "system", "content": self.prompt_content},
                    {"role": "user", "content": user_request}
                ]
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            logger.error(e, exc_info=True)
            return False

    @staticmethod
    async def reduce_vacancy_description(input_data: dict):
        from bot_files.constants import REDUCE_VACANCY_DESCRIPTION_PROMPT
        full_prompt = '{}\n{}\nLink is {}'.format(
            REDUCE_VACANCY_DESCRIPTION_PROMPT,
            json.dumps(input_data), input_data["link"]
        )
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=full_prompt,
            max_tokens=1000
        )
        generated_text = response.choices[0].text.strip()
        return generated_text


gpt_api = OpenAI()
