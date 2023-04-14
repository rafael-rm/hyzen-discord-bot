from discord.ext import tasks
from discord.ext import commands
import logging
import dotenv
import requests
import os
import json
import datetime


dotenv.load_dotenv()
API_URL_BASE = str(os.getenv('API_BASE_STATUS'))
API_KEY = str(os.getenv('STATUS_PAGE_API_KEY'))
PAGE_ID = str(os.getenv('PAGE_ID'))
METRIC_ID = str(os.getenv('METRIC_ID_SHARDS'))


class StatusPageShardsEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.is_testing == True:
            logging.info('A aplicação está em modo de teste, não será enviado o numero de shards para Status Page.')
            return

        params = json.dumps({
            'data' : {
                        'timestamp': datetime.datetime.now().timestamp(),
                        'value': self.bot.shard_count
                    }
        })

        headers = {"Content-Type": "application/json", "Authorization": "OAuth " + API_KEY}

        url = f'https://{API_URL_BASE}/pages/{PAGE_ID}/metrics/{METRIC_ID}/data.json'

        request = requests.post(url, data=params, headers=headers)

        if request.status_code == 201:
            logging.info(f'Numero de shards enviado para Status Page com sucesso. Status: {request.status_code}. Shards: {self.bot.shard_count}.')
        else:
            logging.error(f'Falha ao enviar o numero de shards para Status Page. Status: {request.status_code}. Shards: {self.bot.shard_count}.')
            logging.error(f'Erro: {request.text}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StatusPageShardsEvent(bot))