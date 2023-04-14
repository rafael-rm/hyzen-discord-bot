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
METRIC_ID = str(os.getenv('METRIC_ID_PING'))


class StatusPagePingEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.enviar_ping_status_page.start()
        logging.info(f'Carregado: {__name__}')


    @tasks.loop(seconds=300)
    async def enviar_ping_status_page(self):
        if self.bot.is_testing == True:
            logging.info('A aplicação está em modo de teste, não será enviado ping para Status Page.')
            return

        if (self.bot.time_start + 300) > datetime.datetime.now().timestamp():
            logging.info('A aplicação acaba de iniciar, aguardando 5 minutos para enviar o primeiro ping para Status Page.')
            return

        ping = round(self.bot.latency * 1000)

        params = json.dumps({
            'data' : {
                        'timestamp': datetime.datetime.now().timestamp(),
                        'value': ping
                    }
        })

        headers = {"Content-Type": "application/json", "Authorization": "OAuth " + API_KEY}

        url = f'https://{API_URL_BASE}/pages/{PAGE_ID}/metrics/{METRIC_ID}/data.json'

        request = requests.post(url, data=params, headers=headers)

        if request.status_code == 201:
            logging.info(f'Ping enviado para Status Page com sucesso. Status: {request.status_code}. Ping: {ping}ms.')
        else:
            logging.error(f'Falha ao enviar ping para Status Page. Status: {request.status_code}. Ping: {ping}ms.')
            logging.error(f'API_URL_BASE: {API_URL_BASE}\n API_KEY: {API_KEY}\n PAGE_ID: {PAGE_ID}\n METRIC_ID: {METRIC_ID}')
            logging.error(f'Erro: {request.text}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StatusPagePingEvent(bot))