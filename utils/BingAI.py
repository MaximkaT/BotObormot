from EdgeGPT import Chatbot, ConversationStyle
import pathlib as pl
import json
import re
import requests as req

class BingAI:
    def __init__(self):
        # cookie loading
        path = pl.Path(pl.Path.cwd(), 'utils', 'cook.json')
        with open(path) as file:
            data = json.load(file)
        self.cookies = data
        # threads for bing chat
        self.threads = {'0':Chatbot(cookies=data)}
        



    """replace footnotes with hyperlinks"""
    def reformat_text(self, response, urls):
        raw = response
        rawlist = re.split('\^\d+\^', raw)
        links = urls.split('\n')
        counter = 1
        for it in re.finditer('\^\d+\^', raw):
            rawlist.insert(counter, f'[{it[0][1:-1]}]({links[int(it[0][1:-1])-1]})')
            counter+=2

        return "".join(rawlist)
    


    """Get urls from bing dict"""
    def get_urls(self, response_dict):
        return '\n'.join([response_dict
                          ['item']
                          ['messages']
                          [1]
                          ['sourceAttributions']
                          [i]
                          ['seeMoreUrl'] for i in range(len(response_dict
                                                            ['item']
                                                            ['messages']
                                                            [1]
                                                            ['sourceAttributions']))])



    """replace link texts with page titles"""
    def reformat_links(self, inn: str):
        links = inn.split('\n')
        res = []
        hearders = {'headers':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
        for link_id in range(len(links)):
            link = links[link_id]
            try:
                al = req.get(link, headers=hearders).text
                title = al[al.find('<title>') + 7 : al.find('</title>')]
                if title != "":
                    res.append(f'[{title}]({link})')
                else:
                    res.append(f'{link}')
            except:
                title = "Невалидная ссылка"
                res.append(f'[{title}]({link})')
        return "\n".join(res)

    
    async def ask_bing(self, thread: Chatbot, prompt: str, style=ConversationStyle.balanced):
        """request to bing api through current thread
        """
        async for final, response_dict in thread.ask_stream(prompt=prompt, conversation_style=style):
            if final:
                response = response_dict['item']['messages'][1]['text']
                urls = self.get_urls(response_dict)
                return {
                    'answer':self.reformat_text(response, urls),
                    'urls':self.reformat_links(urls) if urls != '' else None
                    }
    

    async def ask_chat(self, prompt: str, thread_id: str, style=ConversationStyle.balanced):
        if thread_id not in self.threads.keys():
            self.threads[thread_id] = Chatbot(cookies=self.cookies)
        return await self.ask_bing(thread = self.threads[thread_id], prompt=prompt, style=style)
    

    async def prompt_bing(self, prompt: str, style=ConversationStyle.balanced):
        answer = await self.ask_bing(thread = self.threads['0'], prompt=prompt, style=style)
        await self.threads['0'].reset()
        return answer
    

    async def thread_close(self, thread_id: str):
            if thread_id not in self.threads.keys():
                raise Exception('thread_id does not exsist to be closed')
            await self.threads[thread_id].close()
            del self.threads[thread_id]
            return 200
