from core.base import CustomClient
from naff import (
    Extension
)

class Midjourney(Extension):
    
    def __init__(self, bot, config):
        self.bot = bot
        print('picture', self.bot)
        self.CONFIG = config





    def setup(bot: CustomClient, config: dict):
        """Let naff load the extension"""

        Midjourney(bot, config=config)