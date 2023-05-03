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
    User, EmbedField, EmbedAttachment
)
class Midjourney(Extension):
    
    def __init__(self, bot, config):
        self.bot = bot
        self.CONFIG = config
        self.kand = Replica(url='kandinsky-2')
        self.diff = Replica(url='stable-diffusion')


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
    async def kandinskiy(self, ctx: InteractionContext, *, prompt: str):
        await ctx.defer()
        urle = self.kand.imagine(prompt)[0]
        imag_emb = EmbedAttachment(urle)
        q_embed_author = EmbedAuthor(name=str(ctx.author), icon_url=ctx.author.avatar.as_url(size=128))
        emb = Embed(title=prompt, image=imag_emb, color=(255, 255, 255), author=q_embed_author)
        await ctx.send(f'{ctx.author.mention}', embed=emb)
    


    @slash_command(
            name="imagine",
            description="Создание изображения по текстовому запросу.",
            sub_cmd_name="diffusion",
            sub_cmd_description="Рисование изображения по запросу с помощью нейросети Stable Diffusion",
    )
    @slash_option(
        name="prompt",
        description="Опишите изображение",
        opt_type=OptionTypes.STRING,
        required=True
    )
    async def kandinskiy(self, ctx: InteractionContext, *, prompt: str):
        await ctx.defer()
        urle = self.diff.imagine(prompt)[0]
        imag_emb = EmbedAttachment(urle)
        q_embed_author = EmbedAuthor(name=str(ctx.author), icon_url=ctx.author.avatar.as_url(size=128))
        emb = Embed(title=prompt, image=imag_emb, color=(255, 255, 255), author=q_embed_author)
        await ctx.send(f'{ctx.author.mention}', embed=emb)
        



    def setup(bot: CustomClient, config: dict):
        """Let naff load the extension"""

        Midjourney(bot, config=config)