from EdgeGPT import Chatbot, ConversationStyle
import pathlib as pl
import json

async def bing_chat(prompt="", style=ConversationStyle.balanced):
    # Функция получения ответа от BingAI с использованием cookies.
    if prompt == "":
        return "Пустой запрос, повторите"
    path = pl.Path(pl.Path.cwd(), 'utils', 'cook.json')
    with open(path) as file:
        data = json.load(file)
    gbot = Chatbot(cookies=data)
    response_dict = await gbot.ask(prompt=prompt, conversation_style=style)
    return response_dict['item']['messages'][1]['text'].replace("[^\\d^]", "")
