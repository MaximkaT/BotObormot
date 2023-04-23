from EdgeGPT import Chatbot, ConversationStyle
import pathlib as pl
import json

async def bing_chat(prompt="", style=ConversationStyle.balanced):
    # Функция получения ответа от BingAI с использованием cookies.
    path = pl.Path(pl.Path.cwd(), 'utils', 'cook.json')
    with open(path) as file:
        data = json.load(file)
    gbot = Chatbot(cookies=data)
    response_dict = await gbot.ask(prompt=prompt, conversation_style=style)
    urls = '\n'.join([response_dict['item']['messages'][1]['sourceAttributions'][i]['seeMoreUrl'] for i in range(len(response_dict['item']['messages'][1]['sourceAttributions']))])
    return response_dict['item']['messages'][1]['text'].replace("[^\\d^]", ""),urls
