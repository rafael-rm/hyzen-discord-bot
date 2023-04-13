from discord.ext import tasks
from discord.ext import commands
import logging
import dotenv
import requests
import os
import json
import datetime


class StatusPagePingEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.enviar_ping_status_page.start()
        logging.info(f'Carregado: {__name__}')


    @tasks.loop(seconds=300)
    async def enviar_ping_status_page(self):

        if (self.bot.time_start + 300) > datetime.datetime.now().timestamp():
            logging.info('A aplicação acaba de iniciar, aguardando 5 minutos para enviar o primeiro ping para Status Page.')
            return

        dotenv.load_dotenv()
        api_base = os.getenv('API_BASE_STATUS')
        api_key = os.getenv('STATUS_PAGE_API_KEY')
        page_id = os.getenv('PAGE_ID_PING')
        metric_id = os.getenv('METRIC_ID_PING')

        ping = round(self.bot.latency * 1000)

        params = json.dumps({
            'data' : {
                        'timestamp': datetime.datetime.now().timestamp(),
                        'value': ping
                    }
        })

        headers = {"Content-Type": "application/json", "Authorization": "OAuth " + api_key}

        url = f'https://{api_base}/pages/{page_id}/metrics/{metric_id}/data.json'

        request = requests.post(url, data=params, headers=headers)

        if request.status_code == 201:
            logging.info(f'Ping enviado para Status Page com sucesso. Status: {request.status_code}. Ping: {ping}ms.')
        else:
            logging.error(f'Falha ao enviar ping para Status Page. Status: {request.status_code}. Ping: {ping}ms.')
            logging.error(f'Erro: {request.text}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StatusPagePingEvent(bot))