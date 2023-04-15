import openai
from core.base import CustomClient
from utils.GPT import *
from naff import (
    Button,
    ButtonStyles,
    ComponentContext, Embed,
    Extension, InteractionContext,
    component_callback, slash_command,
)


class ChatGPTDLC(Extension):
    bot: CustomClient
    bot_channel = None

    #------------------------Utilities------------------------
    """ 
    arrange every message to bot form 
    {'user': 'user/assistant',
     'content': user message with cutted command prefix/bot message with cutted user mention}
    """
    def arrangeMes(self, message):
        role = 'user' if message.author != self.bot.user else 'assistant'
        mes = message.content.replace(f'/chat ', '') if message.author != self.bot.user \
            else message.content.split(':\n', 1)[1]
        return {'role': role, 'content': mes}
    

    # sends the message to the openai api. While the message is being processed, print wait message
    async def reply(self, ctx, messages, mesAuthor=None):
        author = ctx.message.author.mention if mesAuthor is None else mesAuthor.mention
        ans = await ctx.send('Обработка запроса...')
        reply = chatGptReuqest(messages)
        print(reply)
        await ans.delete()
        res_embed = Embed(title='Ответ', description=reply)
        await ctx.send(f'{author}', embeds = res_embed)
    #---------------------------------------------------------

    @slash_command(name="chat", description="Позволяет общаться с искуственным интеллектом на базе ChatGPT")
    async def chat_gpt(self, ctx: InteractionContext, message):

        # creating new thread if message is in the channel for bot threads
        if ctx.channel == self.bot_channel:
            new_thread = await ctx.channel.create_thread(
                name='bot ' + '_'.join(message.split()[:5]) + ' ' + str(ctx.message.author),
                message=ctx.message,
                auto_archive_duration=120  # 2 hours
            )

            # send answer from chat gpt to first user message
            await self.reply(new_thread, [self.arrangeMes(ctx.message)], ctx.message.author)
            print('Ответ отправлен')
            return
        
        #if user already typing in bot thread, answer, using context of the thread
        elif ctx.channel.name.startswith('bot '):

            # make conversation history from user messages, that starts with slash command
            # and bot messages
            messages = [message async for message in ctx.channel.history(limit=200) if
                        message.content.startswith(f'{self.bot_prefix}gpt ')
                        or message.author == self.bot.user][:-1]
            
            # adding thread starter message by finding it's id on parent channel
            messages.append(await ctx.channel.parent.fetch_message(ctx.channel.id))

            # sort message list from first to last
            messages.reverse()

            # reformate messages for bot
            messages = list(map(self.arrangeMes, messages))

            # reply to user with bot context answer
            await self.reply(ctx, messages)
            print('Ответ отправлен')






def setup(bot: CustomClient):
    """Let naff load the extension"""

    ChatGPTDLC(bot)