import os

from naff import Intents
from naff.ext.debug_extension import DebugExtension

import json

from core.init_logging import init_logging
from core.base import CustomClient
from core.extensions_loader import load_extensions
import openai


if __name__ == "__main__":
    # get keys and tokens for a bot
    with open('./keys.json') as keys_file:
        settings = json.load(keys_file)
    config = settings['config']

    #Init ChatGPT key
    openai.api_key = settings['openai-key']
    # initialise logging
    init_logging()

    # create our bot instance
    bot = CustomClient(
        intents=Intents.ALL,  # intents are what events we want to receive from discord, `DEFAULT` is usually fine
        auto_defer=True,  # automatically deferring interactions
        activity="доброго бота",  # the status message of the bot
    )

    # load the debug extension if that is wanted
    if settings['debug-mode'] == "true":
        DebugExtension(bot=bot)

    # load all extensions in the ./extensions folder
    load_extensions(bot=bot, config=config)

    # start the bot
    bot.start(settings['bot-token'])
