from notionai import NotionAI
import pathlib as pl
import json

class NotionAi:
    def __init__(self,filename):
        path = pl.Path(pl.Path.cwd(), filename)
        with open(path) as keys_file:
            data = json.load(keys_file)
        
        self.token = data['notion-key']
        self.space_id = data['space-id']
        self.ai = NotionAI(self.token, self.space_id)

    def notion_blog(self,prompt):
        blog = self.ai.blog_post(prompt)
        return blog

ai = NotionAi('keys.json')
print(ai.notion_blog('Напиши небольшой рассказ про цветы в летнем саду'))