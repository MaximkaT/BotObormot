from notionai import NotionAI
from notionai.enums import TopicEnum
import pathlib as pl
import json

class NotionAi:
    def __init__(self,filename: str):
        path = pl.Path(pl.Path.cwd(), filename)
        with open(path) as keys_file:
            data = json.load(keys_file)
        
        self.token = data['notion-key']
        self.space_id = data['space-id']
        self.ai = NotionAI(self.token, self.space_id)
        self.context = ''
    
    # Пишет по prompt, по заданному стилю (topic)
    '''темы
    "brainstormIdeas" - идеи на тему
    "blogPost" - пост блога
    "outline" - 
    "socialMediaPost" - пост в соц. сети
    "pressRelease" - 
    "creativeStory" - креативная история
    "essay" - ессэ
    "poem" - поэма
    "meetingAgenda"
    "prosConsList" 
    "jobDescription" - описание работы
    "salesEmail" - 
    "recruitingEmail" - 
    '''
    def notion_topic_writing(self, topic: TopicEnum, prompt: str
                             ) -> str:
        writed = self.ai.writing_with_topic(topic=topic, prompt=prompt)
        self.context = writed
        return writed
    
    # prompt - как надо изменить, context - изменяемый текст
    def notion_help_edit(self, prompt: str, context: str
                         ) -> str:
        edit = self.ai.help_me_edit(prompt=prompt, context=context)
        return edit

ai = NotionAi('keys.json')
