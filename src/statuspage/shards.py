import asyncio
from asyncio import tasks
from discord.ext import commands
import logging
import dotenv
import requests
import os
import json
import configparser
import datetime


class StatusPageShardsEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        dotenv.load_dotenv()
        config = configparser.ConfigParser()
        config.read('config.conf')
        self.api_url_base = config.get('STATUSPAGE', 'API_URL_BASE')
        self.api_key = str(os.getenv('STATUS_PAGE_API_KEY'))
        self.page_id = str(os.getenv('PAGE_ID'))
        self.metric_id = config.get('STATUSPAGE', 'METRIC_ID_SHARDS')


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')
        await asyncio.sleep(30)
        self.enviar_shards_status_page.start()


    @tasks.loop(seconds=900)
    async def enviar_shards_status_page(self):
        if self.bot.is_testing == True:
            logging.info('A aplicação está em modo de teste, não será enviado o numero de shards para Status Page.')
            return

        params = json.dumps({
            'data' : {
                        'timestamp': datetime.datetime.now().timestamp(),
                        'value': self.bot.shard_count
                    }
        })

        headers = {"Content-Type": "application/json", "Authorization": "OAuth " + self.api_key}

        url = f'https://{self.api_url_base}/pages/{self.page_id}/metrics/{self.metric_id}/data.json'

        request = requests.post(url, data=params, headers=headers)

        if request.status_code == 201:
            logging.info(f'Numero de shards enviado para Status Page com sucesso. Status: {request.status_code}. Shards: {self.bot.shard_count}.')
        else:
            logging.error(f'Falha ao enviar o numero de shards para Status Page. Status: {request.status_code}. Shards: {self.bot.shard_count}.')
            logging.error(f'Erro: {request.text}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StatusPageShardsEvent(bot))