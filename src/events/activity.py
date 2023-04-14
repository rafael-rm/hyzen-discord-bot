import asyncio
from discord.ext import commands
import discord
import logging


class ActivityEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')

        await asyncio.sleep(30)
    
        status = 'hyzen.com.br'
        logging.info(f'Alterando a atividade da aplicação para: {status}')
        await self.bot.change_presence(activity=discord.Game(name=status))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ActivityEvent(bot))