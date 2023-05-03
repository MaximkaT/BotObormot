from core.base import CustomClient
from utils.GPT import *
from utils.Kandinsky import *
from naff import (
    Embed, EmbedAuthor,
    Extension, InteractionContext,
    slash_command, slash_option, check,
    SlashCommandChoice, OptionTypes, Context,
    AutoArchiveDuration, Message,
    ThreadChannel,
    User, EmbedField
)
class Midjourney(Extension):
    
    def __init__(self, bot, config):
        self.bot = bot
        self.CONFIG = config
        self.replica = Replica()


    @slash_command(
            name="imagine",
            description="Создание изображения по текстовому запросу.",
            sub_cmd_name="kandinskiy",
            sub_cmd_description="Рисование изображения по запросу с помощью нейросети Kandinsky 2.0.",
    )
    @slash_option(
        name="prompt",
        description="Опишите изображение",
        opt_type=OptionTypes.STRING,
        required=True
    )
    async def kandinskiy(self):
        



    def setup(bot: CustomClient, config: dict):
        """Let naff load the extension"""

        Midjourney(bot, config=config)