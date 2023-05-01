from EdgeGPT import Chatbot, ConversationStyle
import pathlib as pl
import json
import re
import requests as req

async def bing_chat(prompt="", style=ConversationStyle.balanced):
    # Функция получения ответа от BingAI с использованием cookies.
    path = pl.Path(pl.Path.cwd(), 'utils', 'cook.json')
    with open(path) as file:
        data = json.load(file)
    gbot = Chatbot(cookies=data)
    response_dict = await gbot.ask(prompt=prompt, conversation_style=style)
    urls = '\n'.join([response_dict['item']['messages'][1]['sourceAttributions'][i]['seeMoreUrl'] for i in range(len(response_dict['item']['messages'][1]['sourceAttributions']))])
    return response_dict['item']['messages'][1]['text'],urls



def reformat_bing_text(inn: list):
    raw = inn[0]
    rawlist = re.split('\^\d+\^', raw)
    links = inn[1].split('\n')
    counter = 1
    for it in re.finditer('\^\d+\^', raw):
        rawlist.insert(counter, f'[{it[0][1:-1]}]({links[int(it[0][1:-1])-1]})')
        counter+=2

    return "".join(rawlist)



def reformat_bing_links(inn: str):
    links = inn.split('\n')
    res = []
    hearders = {'headers':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    for link_id in range(len(links)):
        link = links[link_id]
        try:
            al = req.get(link, headers=hearders).text
            title = al[al.find('<title>') + 7 : al.find('</title>')]
            res.append(f'[{title}]({link})')
        except:
            title = "Невалидная ссылка"
            res.append(f'[{title}]({link})')
    return "\n".join(res)