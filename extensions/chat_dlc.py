from core.base import CustomClient
from utils.GPT import *
from utils.BingAI import *
from naff import (
    Embed, EmbedAuthor,
    Extension, InteractionContext,
    slash_command, slash_option, check,
    SlashCommandChoice, OptionTypes, Context,
    AutoArchiveDuration, Message,
    ThreadChannel,
    User, EmbedField
)


class ChatGPTDLC(Extension):


    def __init__(self, bot, config):
        self.bot = bot
        self.bot_channel = None
        self.CONFIG = config

    #--------------------------------------------Utilities-------------------------------------------
    """ 
    arrange every message to bot form 
    {'user': 'user/assistant',
     'content': user message / bot message}
    """
    def embToGPT(self, message: Message):
        embs: Embed = message.embeds[0]
        role = 'user' if embs.title == 'ВОПРОС' else 'assistant'
        mes = embs.description
        res = {'role': role, 'content': mes}
        return res
    

    # sends the message to the openai api. While the message is being processed, print wait message
    async def reply(self, ctx, messages: list, mesAuthor=None):
        author = ctx.author if mesAuthor is None else mesAuthor

        q_embed_author = EmbedAuthor(name=str(author), icon_url=author.avatar.as_url(size=128))
        q_embed = Embed(title='ВОПРОС', description=messages[-1]['content'], color=(256, 0, 0), author=q_embed_author)
        
        
        reply = chatGptReuqest(messages)
        # reply = 'Иди нахрен'
        embs = []
        while len(reply) > 1024:
            embs.append(EmbedField(name='answer_field', value=reply[:1024]))
            reply = reply[1024:]
        embs.append(EmbedField(name='answer_field', value=reply))

        emb_author = EmbedAuthor(name=self.CONFIG['bot_name'], icon_url=self.CONFIG['bot_image_url'])
        res_embed = Embed(title='ОТВЕТ', author=emb_author, color=(0, 256, 0), fields=embs)
        await ctx.send(embed=q_embed)
        await ctx.send(f'{author.mention}', embed = res_embed)
    #------------------------------------------------------------------------------------------------


    @slash_command(
            name="prompt",
            description="Одноразовый ответ на вопрос, можно задать в любом месте.",
            sub_cmd_name="gpt3",
            sub_cmd_description="Вопрос к ChatGPT на основе GPT 3.5",
    )
    @slash_option(name="prompt",
                  description="текст запроса",
                  required=True,
                  opt_type=OptionTypes.STRING,
                  max_length=3000)
    async def prompt(self, ctx: InteractionContext, *, prompt: str):
        arranged_message = {'role': 'user', 'content':prompt}
        await ctx.defer()
        repl = chatGptReuqest([arranged_message])

        embs = []
        embs.append(EmbedField(name='Ответ:', value=repl[:1024]))
        repl = repl[1024:]
        while len(repl) > 0:
            embs.append(EmbedField(name='\n', value=repl[:1024]))
            repl = repl[1024:]
        
        q_embed_author = EmbedAuthor(name=str(ctx.author), icon_url=ctx.author.avatar.as_url(size=128))
        ans_emb = Embed(color=(255, 255, 255), author=q_embed_author, fields=embs)
        await ctx.send(content=ctx.author.mention, embed=ans_emb)

    @slash_command(
            name="prompt",
            description="Одноразовый ответ на вопрос, можно задать в любом месте.",
            sub_cmd_name="bing",
            sub_cmd_description="Вопрос к поисковику bing на основе GPT 4. Возвращает ответ и ссылки на страницы, откуда он был взят",
    )
    @slash_option(name="prompt",
                  description="текст запроса",
                  required=True,
                  opt_type=OptionTypes.STRING)
    @slash_option(name="style", 
                  description="стиль ответа",
                  required=False,
                  opt_type=OptionTypes.INTEGER,
                  choices=[
                      SlashCommandChoice(name="Сбалансированный", value=1),
                      SlashCommandChoice(name="Креативный", value=2),
                      SlashCommandChoice(name="Точный", value=3),
                  ]
                  )
    async def bing(self, ctx: InteractionContext, *, prompt: str, style: int = 1):
        await ctx.defer()
        reply = await bing_chat(prompt=prompt,
                                style={1: ConversationStyle.balanced,
                                       2: ConversationStyle.creative,
                                       3: ConversationStyle.precise}.get(style))
        
        fields = []
        question = EmbedField(name="**Вопрос:**", value = prompt, inline=False)
        fields.append(question)

        repl = reformat_bing_text(reply)
        fields.append(EmbedField(name='Ответ:', value=repl[:1024]))
        repl = repl[1024:]
        while len(repl) > 0:
            fields.append(EmbedField(name='\n', value=repl[:1024]))
            repl = repl[1024:]
        
        if reply[1] != "":
            links = reformat_bing_links(reply[1])
            urls = EmbedField(name='Источники:',value=links, inline=False)
            fields.append(urls)
        q_embed_author = EmbedAuthor(name=str(ctx.author), icon_url=ctx.author.avatar.as_url(size=128))
        ans_emb = Embed(color=(255, 255, 255), author=q_embed_author, fields=fields)
        await ctx.send(content=ctx.author.mention, embed=ans_emb)

    


    @slash_command(name="chat", description="Позволяет общаться с искуственным интеллектом на базе ChatGPT")
    @slash_option(name="prompt",
                  description="текст запроса",
                  required=True,
                  opt_type=OptionTypes.STRING)
    async def chat_gpt(self, ctx: InteractionContext, *, prompt: str):

        # creating new thread if message is in the channel for bot threads
        if ctx.channel == self.bot_channel:

            new_thread = await ctx.channel.create_thread_from_message(
                name='bot ' + '_'.join(prompt.split()[:5]) + ' ' + str(ctx.author),
                message=ctx.message,
                auto_archive_duration=AutoArchiveDuration.ONE_HOUR
            )

            # send answer from chat gpt to first user message
            arranged_message = {'role': 'user', 'content':prompt}
            await ctx.send(content = 'Создана ветка для беседы с чат-ботом. Если вы хотите одноразового ответа в любом месте, выбирайте /prompt.', ephemeral=True)
            await self.reply(new_thread, [arranged_message], ctx.author)
            
            # print('Ответ отправлен')
        
        #if user already typing in bot thread, answer, using context of the thread
        elif ctx.channel.name.startswith('bot '):
            print(type(self.bot))
            # make conversation history from user messages, that starts with slash command
            # and bot messages

            messages = [message async for message in ctx.channel.history(limit=200) if
                        message.author == self.bot.user]
            
            # sort message list from first to last
            messages.reverse()

            # reformate messages for bot
            messages = list(map(self.embToGPT, messages))
            # print(messages)
            messages.append({'role': 'user', 'content': prompt})

            await ctx.defer()
            # reply to user with bot context answer
            await self.reply(ctx, messages)
            print('Ответ отправлен')
        else:
            await ctx.send(content="Неправильный канал для бесед", ephemeral=True)
        
    
    @slash_command(name="thanks", description='Закрывает ветку и выгоняет всех участников')
    async def thanks(self, ctx: InteractionContext):
        if ctx.channel.name.startswith('bot '):
            chann: ThreadChannel = ctx.channel
            for mem in await chann.fetch_members():
                us: User = mem.get_user()
                await chann.remove_member(us)
            await ctx.send(content="Спасибо за беседу. До новых встреч.", ephemeral=True)
            await chann.archive()

    
    @slash_command(name='delete', description='Удаляет ветку общения с ботом')
    async def delete(self, ctx: InteractionContext):
        if ctx.channel.name.startswith('bot '):
            await ctx.channel.delete()
        await ctx.channel.parent_channel.delete_message(await ctx.channel.parent_channel.fetch_message(ctx.channel.id))

    async def my_check(ctx: Context):
        return True

    @check(check=my_check)
    @slash_command(name='init_channel', description='Устанавливает канал для общения с ботом')
    async def init_channel(self, ctx: InteractionContext):
        self.bot_channel = ctx.channel
        await ctx.send('Канал установлен')
        for role in ctx.author.roles:
            print(role.name, role.id)
        print(f'new channel - {self.bot_channel}')






def setup(bot: CustomClient, config: dict):
    """Let naff load the extension"""
    ChatGPTDLC(bot, config)
    