import discord
import os
import asyncio
import dotenv
from discord.ext import commands
import datetime
import logging
import src.functions.logs as logs
from src.database.firebase import FirebaseDB
import configparser


class App(commands.AutoShardedBot):
    def __init__(self, token, shards, intents, prefixo, is_testing):
        super().__init__(
            intents = intents,
            command_prefix = prefixo,
            shard_count = shards,
        )
        self.token = token
        self.is_testing = is_testing
        self.time_start = datetime.datetime.now().timestamp()
        self.firebase = FirebaseDB()
        self.config = configparser.ConfigParser()
        self.config.read('config.conf')
        self.color_embed_default = int(self.config['COLORS']['DEFAULT'])
        self.cache_comandos_executados = 0


    async def carregar(self):
        for folder in os.listdir('./src/commands/'):
            for file in os.listdir(f'./src/commands/{folder}'):
                if file.endswith('.py'):
                    try:
                        logging.info(f'Encontrado arquivo: {(f"./src/commands/{folder}/{file}")}')
                        await self.load_extension(f'src.commands.{folder}.{file[:-3]}')
                    except Exception as error:
                        logging.error(f'{error}')

        for file in os.listdir('./src/events/'):
            if file.endswith('.py'):
                try:
                    logging.info(f'Encontrado arquivo: {(f"./src/events/{file}")}')
                    await self.load_extension(f'src.events.{file[:-3]}')
                except Exception as error:
                    logging.error(f'{error}')

        for file in os.listdir('./src/statuspage/'):
            if file.endswith('.py') and file == 'ping.py':
                try:
                    logging.info(f'Encontrado arquivo: {(f"./src/statuspage/{file}")}')
                    await self.load_extension(f'src.statuspage.{file[:-3]}')
                except Exception as error:
                    logging.error(f'{error}')


    async def iniciar(self):
        await App.carregar(self)
        await self.start(self.token)


def main():
    logs.main()

    intents = discord.Intents.default()
    intents.members = True

    config = configparser.ConfigParser()
    config.read('config.conf')
    shards = config.getint('CLIENT', 'SHARDS')
    prefixo = config.get('CLIENT', 'PREFIX')
    is_testing = config.getboolean('CLIENT', 'IS_TESTING')

    dotenv.load_dotenv()
    token = os.getenv('TOKEN-CANARY') if is_testing else os.getenv('TOKEN-PROD')

    asyncio.run(App(token, shards, intents, prefixo, is_testing).iniciar())


if __name__ == '__main__':
    main()