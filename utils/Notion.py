from notionai import NotionAI
import pathlib as pl
import json

# see NotionAI with f12
class NotionAi(NotionAI):
    def __init__(self, model: str = 'openai-3') -> None:
        path = pl.Path(pl.Path.cwd(),'keys.json')
        with open(path) as keys_file:
            data = json.load(keys_file)

        self.token = data['notion-key']
        self.space_id = data['space-id']
        self.model = model
        self.is_space_permission = False
        self.url = "https://www.notion.so/api/v3/getCompletion"