import os

from dotenv import load_dotenv
from naff import Intents
from naff.ext.debug_extension import DebugExtension

from core.init_logging import init_logging
from core.base import CustomClient
from core.extensions_loader import load_extensions
import openai


config = {
    'bot_name': 'Бот-обормот',
    'admin_role': 'Тимлид',
    'bot_image_url': 'https://media.discordapp.net/attachments/1046772205876424794/1092428709300011039/CineOP_dumpling_simplified_logo_simple_forms_a7fd2df5-94e4-4538-b193-e55fa249702a.png?width=676&height=676',
    'server_meet_url': 'https://discord.gg/z4p8h8Xybk'
}

if __name__ == "__main__":
    # load the environmental vars from the .env file
    load_dotenv()

    #Init ChatGPT key
    openai.api_key = str(os.getenv("OPENAI_API_KEY"))
    # initialise logging
    init_logging()

    # create our bot instance
    bot = CustomClient(
        intents=Intents.ALL,  # intents are what events we want to receive from discord, `DEFAULT` is usually fine
        auto_defer=True,  # automatically deferring interactions
        activity="доброго бота",  # the status message of the bot
    )

    # load the debug extension if that is wanted
    if os.getenv("LOAD_DEBUG_COMMANDS") == "true":
        DebugExtension(bot=bot)

    # load all extensions in the ./extensions folder
    load_extensions(bot=bot, config=config)

    # start the bot
    bot.start(os.getenv("DISCORD_TOKEN"))
