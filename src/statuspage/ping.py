import asyncio
from discord.ext import tasks
from discord.ext import commands
import logging
import dotenv
import requests
import os
import json
import datetime
import configparser


class StatusPagePingEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        dotenv.load_dotenv()
        config = configparser.ConfigParser()
        config.read('config.conf')
        self.api_url_base = config.get('STATUSPAGE', 'API_URL_BASE')
        self.page_id = config.get('STATUSPAGE', 'PAGE_ID')
        self.metric_id = config.get('STATUSPAGE', 'METRIC_ID_PING')
        self.api_key = str(os.getenv('STATUS_PAGE_API_KEY'))

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')

        await asyncio.sleep(15)
        config = configparser.ConfigParser()
        config.read('config.conf')
        enviar_metricas = config.getboolean('STATUSPAGE', 'ENVIAR_METRICAS')

        if self.bot.is_testing == True:
            logging.info('A aplicação está em modo de teste, não será enviado o numero de shards para Status Page.')
            return

        if enviar_metricas == True:
            self.enviar_ping_status_page.start()
        else:
            logging.info('A aplicação não está configurada para enviar métricas de ping para Status Page.')
            return

    @tasks.loop(seconds=300)
    async def enviar_ping_status_page(self):
        if self.bot.is_testing == True:
            logging.info('A aplicação está em modo de teste, não será enviado ping para Status Page.')
            return

        if (self.bot.time_start + 300) > datetime.datetime.now().timestamp():
            logging.info(
                'A aplicação acaba de iniciar, aguardando 5 minutos para enviar o primeiro ping para Status Page.')
            return

        ping = round(self.bot.latency * 1000)

        params = json.dumps({
            'data': {
                'timestamp': datetime.datetime.now().timestamp(),
                'value': ping
            }
        })

        headers = {"Content-Type": "application/json", "Authorization": "OAuth " + self.api_key}

        url = f'https://{self.api_url_base}/pages/{self.page_id}/metrics/{self.metric_id}/data.json'

        request = requests.post(url, data=params, headers=headers)

        if request.status_code == 201:
            logging.info(f'Ping enviado para Status Page com sucesso. Status: {request.status_code}. Ping: {ping}ms.')
        else:
            logging.error(f'Falha ao enviar ping para Status Page. Status: {request.status_code}. Ping: {ping}ms.')
            logging.error(f'Erro: {request.text}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StatusPagePingEvent(bot))
