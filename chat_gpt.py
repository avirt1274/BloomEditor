import typing
from g4f.client import Client

client = Client()  # Создаем один объект Client для работы

# Класс моделей GPT
class AI:
    models = typing.Literal[
        "gpt-3.5-turbo"
        # "gpt-4",
        # "gpt-4-turbo"
    ]

# Исключение для пустого вопроса
class NoneQuestionError(Exception):
    def __init__(self):
        super().__init__("Question can't be None!")

# Функция для запроса к GPT
def request_gpt(question: str, model: AI.models) -> str:
    if not question:  # Проверка на пустой вопрос
        raise NoneQuestionError()
    
    answer = gpt(question, model)
    
    # Перезапрашиваем, если есть недопустимые символы
    while check_china_town(answer):
        answer = gpt(question, model)
    
    return answer.strip()

# Функция для отправки запроса в GPT
def gpt(question: str, model: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

# Проверка текста на наличие китайских символов
def check_china_town(text: str) -> bool:
    return any(ord(c) > 0x31C0 for c in text)