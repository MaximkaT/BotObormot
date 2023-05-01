from EdgeGPT import Chatbot, ConversationStyle
import pathlib as pl
import json
import re
import requests as req

class BingAI:
    def __init__(self):
        path = pl.Path(pl.Path.cwd(), 'utils', 'cook.json')
        with open(path) as file:
            data = json.load(file)
        self.threads = {'0':Chatbot(cookies=data)}
        self.cookies = data


    def reformat_text(self, response, urls):
        raw = response
        rawlist = re.split('\^\d+\^', raw)
        links = urls.split('\n')
        counter = 1
        for it in re.finditer('\^\d+\^', raw):
            rawlist.insert(counter, f'[{it[0][1:-1]}]({links[int(it[0][1:-1])-1]})')
            counter+=2

        return "".join(rawlist)
    

    def get_urls(self, response_dict):
        return '\n'.join([response_dict['item']['messages'][1]['sourceAttributions'][i]['seeMoreUrl'] for i in range(len(response_dict['item']['messages'][1]['sourceAttributions']))])


    def reformat_links(self, inn: str):
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


    async def ask_bing(self, bot: Chatbot, prompt: str, style=ConversationStyle.balanced):
        async for final, response_dict in bot.ask_stream(prompt=prompt, conversation_style=style):
            if final:
                response = response_dict['item']['messages'][1]['text']
                urls = '\n'.join([response_dict['item']['messages'][1]['sourceAttributions'][i]['seeMoreUrl'] for i in range(len(response_dict['item']['messages'][1]['sourceAttributions']))])
                return {
                    'answer':self.reformat_text(response, urls),
                    'urls':self.reformat_links(urls)
                    }
    

    async def ask_chat(self, prompt: str, thread_id: str, style=ConversationStyle.balanced):
        if thread_id not in self.threads.keys():
            self.threads[thread_id] = Chatbot(cookies=self.cookies)
        return await self.ask_bing(bot = self.threads[thread_id], prompt=prompt, style=style)
    

    async def prompt_bing(self, prompt: str, style=ConversationStyle.balanced):
        answer = await self.ask_bing(bot = self.threads['0'], prompt=prompt, style=style)
        await self.threads['0'].reset()
        return answer
    

    async def thread_close(self, thread_id: str):
            if thread_id not in self.threads.keys():
                raise Exception('thread_id does not exsist to be closed')
            await self.threads[thread_id].close()
            del self.threads[thread_id]
            return 200
