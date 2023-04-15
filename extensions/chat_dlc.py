import openai
from core.base import CustomClient
from utils.GPT import *
from naff import (
    Button,
    ButtonStyles,
    ComponentContext, Embed, EmbedAuthor,
    Extension, InteractionContext,
    component_callback, slash_command, slash_option,
    SlashCommandOption, OptionTypes,
    AutoArchiveDuration, Message,
    Color, COLOR_TYPES,
)


class ChatGPTDLC(Extension):
    bot: CustomClient
    bot_channel = None
    default_id = 1046772205876424794
    REQUEST_STRING = '**Запрос:**\n'
    MENTION_TEXT_SEPARATOR = ':\n'
    BOT_IMAGE = ''
    BOT_NAME = 'Бот-обормот'
    EMBED_COLOR = 'white'

    #--------------------------------------------Utilities-------------------------------------------
    """ 
    arrange every message to bot form 
    {'user': 'user/assistant',
     'content': user message with cutted command prefix/bot message with cutted user mention}
    """
    def embToGPT(self, message: Message):
        embs: Embed = message.embeds[0]
        role = 'user' if embs.title == 'ВОПРОС' else 'assistant'
        mes = embs.description
        res = {'role': role, 'content': mes}
        # print(res)
        return res
    

    # sends the message to the openai api. While the message is being processed, print wait message
    async def reply(self, ctx, messages, mesAuthor=None):
        author = ctx.author if mesAuthor is None else mesAuthor

        # q_embed_author = EmbedAuthor(name=str(author), icon_url=author.avatar.as_url(size=128))
        # q_embed = Embed(title='ВОПРОС', description=messages[-1]['content'], color=(256, 0, 0), author=q_embed_author)
        # await ctx.send(embed=q_embed)



        
        ans = await ctx.send('Обработка запроса...')
        # reply = chatGptReuqest(messages)
        reply = 'Иди нахрен'
        await ans.delete()
        emb_author = EmbedAuthor(name=self.BOT_NAME, icon_url=self.BOT_IMAGE)
        res_embed = Embed(title='ОТВЕТ', description=reply, author=emb_author, color=(0, 256, 0))
        await ctx.send(f'{author.mention}', embed = res_embed)
        return
    #------------------------------------------------------------------------------------------------

    @slash_command(name="chat", description="Позволяет общаться с искуственным интеллектом на базе ChatGPT")
    @slash_option(name="prompt",
                  description="текст запроса",
                  required=True,
                  opt_type=OptionTypes.STRING)
    async def chat_gpt(self, ctx: InteractionContext, *, scopes=[default_id], prompt: str):

        

        # creating new thread if message is in the channel for bot threads
        if ctx.channel == self.bot_channel:

            new_thread = await ctx.channel.create_thread_from_message(
                name='bot ' + '_'.join(prompt.split()[:5]) + ' ' + str(ctx.author),
                message=ctx.message,
                auto_archive_duration=AutoArchiveDuration.ONE_HOUR
            )

            # send answer from chat gpt to first user message
            arranged_message = {'role': 'user', 'content':prompt}
            await self.reply(new_thread, [arranged_message], ctx.author)
            print('Ответ отправлен')
        
        #if user already typing in bot thread, answer, using context of the thread
        elif ctx.channel.name.startswith('bot '):

            q_embed_author = EmbedAuthor(name=str(ctx.author), icon_url=ctx.author.avatar.as_url(size=128))
            q_embed = Embed(title='ВОПРОС', description=messages[-1]['content'], color=(256, 0, 0), author=q_embed_author)
            await ctx.send(embed=q_embed)
            # make conversation history from user messages, that starts with slash command
            # and bot messages
            messages = [message async for message in ctx.channel.history(limit=200) if
                        message.author == self.bot.user]
            
            print([mes.content for mes in messages])

            # sort message list from first to last
            messages.reverse()

            # reformate messages for bot
            messages = list(map(self.embToGPT, messages))
            print(messages)

            # reply to user with bot context answer
            await self.reply(ctx, messages)
            print('Ответ отправлен')
        


    @slash_command(name='init_channel', description='Устанавливает канал для общения с ботом')
    async def init_channel(self, ctx: InteractionContext):
        self.bot_channel = ctx.channel
        # await ctx.message.delete()
        await ctx.send('Канал установлен')
        print(f'new channel - {self.bot_channel}')






def setup(bot: CustomClient):
    """Let naff load the extension"""

    ChatGPTDLC(bot)