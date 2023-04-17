import asyncio
import json
import random
from discord.ext import commands
from discord.ext import tasks
import discord
import logging
import configparser


class ActivityEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.status = []


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')

        await asyncio.sleep(5)
        config = configparser.ConfigParser()
        config.read('config.conf')

        self.status = json.loads(config.get('CLIENT', 'ACTIVITY'))
        self.alterar_status.start()


    @tasks.loop(seconds=600)
    async def alterar_status(self):
        status = random.choice(self.status)
        logging.info(f'Alterando a atividade da aplicação para: {status}')
        await self.bot.change_presence(activity=discord.Game(name=status))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ActivityEvent(bot))