import configparser
import discord
from discord import app_commands
from discord.ext import commands
from src.functions.comando_executado import comando_executado
from src.functions.comando_executado import comando_executado_erro
from src.functions.permissoes import permissao_desenvolvedor
import psutil
import datetime
import logging
import os
import zipfile


class ButtonsDevelopersCommands(discord.ui.View):
    def __init__(self, author):
        self.author = author
        super().__init__()


    @discord.ui.button(label="Baixar", style=discord.ButtonStyle.success, custom_id="download", emoji="📥")
    async def baixar_logs(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message(file=discord.File('logs.log'))
            logging.info(f"Arquivo de logs solicitado por {interaction.user.id} enviado no canal {interaction.channel.id}.")
        except Exception as error:
            logging.error(f"Erro ao enviar arquivo de logs solicitado por {interaction.user.id} no canal {interaction.channel.id}.")
            logging.error(f"{error}")
            await interaction.response.send_message("Erro ao enviar arquivo de logs, verifique o console da aplicação.")


    @discord.ui.button(label="Apagar logs", style=discord.ButtonStyle.danger, custom_id="clear", emoji="🗑️")
    async def apagar_logs(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open('logs.log', 'w') as f:
            f.write('')
        logging.info(f"Solicitação para apagar arquivo de logs enviada por {interaction.user.id} no canal {interaction.channel.id}.")
        await interaction.response.send_message("Arquivo de logs apagado com sucesso.")


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("Você não possui permissão para utilizar esta interação.", ephemeral=True)
            logging.warn(f"O usuário {interaction.user.id} tentou utilizar uma interação do comando de logs no servidor {interaction.guild.id} no canal {interaction.channel.id} sem permissão.")
            return False
        return True


class DevelopersCommands(commands.GroupCog, name="desenvolvedor", description="Comandos de desenvolvedor."):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @staticmethod
    def permissao_usar_cmd():
        def verificar_permissoes(interaction: discord.Interaction) -> bool:
            return permissao_desenvolvedor(interaction.user.id)
        return app_commands.check(verificar_permissoes)


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @app_commands.command(name='ping', description='Mostra o ping da aplicação.')
    @permissao_usar_cmd()
    async def ping(self, interaction: discord.Interaction): 
        await comando_executado(interaction, self.bot)
        await interaction.response.send_message(f"A aplicação encontra-se com **{round(self.bot.latency * 1000)}ms** de latência") 


    @app_commands.command(name='ram', description='Mostra o uso de RAM da máquina.')
    @permissao_usar_cmd()
    async def ram(self, interaction: discord.Interaction):
        await comando_executado(interaction, self.bot)
        await interaction.response.send_message(f"A máquina encontra-se utilizando **{psutil.virtual_memory().used / 1024 / 1024:.0f}/{psutil.virtual_memory().total / 1024 / 1024:.0f}MB ({psutil.virtual_memory().percent}%)** de RAM")


    @app_commands.command(name='cpu', description='Mostra o uso da CPU da máquina.')
    @permissao_usar_cmd()
    async def cpu(self, interaction: discord.Interaction):
        await comando_executado(interaction, self.bot)
        await interaction.response.send_message(f"A máquina possui **{psutil.cpu_count()} núcleos lógicos** e está utilizando **{psutil.cpu_percent()}%** de sua capacidade total")


    @app_commands.command(name='sync', description='Sincroniza os comandos da aplicação.')
    @permissao_usar_cmd()
    async def sync(self, interaction: discord.Interaction):
        await comando_executado(interaction, self.bot)
        await interaction.response.send_message('Sincronizando aplicação com o Discord...')
        logging.info('Sincronizando aplicação com o Discord...')
        await self.bot.tree.sync()
        await interaction.channel.send('Aplicação sincronizada com o Discord.')
        logging.info('Aplicação sincronizada com o Discord.')


    @app_commands.command(name='shard', description='Mostra informações sobre as shards da aplicação.')
    @permissao_usar_cmd()
    async def shard(self, interaction: discord.Interaction):
        await comando_executado(interaction, self.bot)
        if interaction.guild is not None:
            mensagem = f"A aplicação possui **{self.bot.shard_count} shards.** \nShard atual: **{interaction.guild.shard_id}** \nPing médio: **{round(self.bot.latency * 1000)}ms**```autohotkey"
            for shard in self.bot.latencies:
                mensagem += f"\nShard {shard[0]}: {round(shard[1] * 1000)}ms"
            mensagem += "```"
            await interaction.response.send_message(mensagem)
        else:
            mensagem = f"A aplicação possui **{self.bot.shard_count} shards.** \nShard atual: **0** \nPing médio: **{round(self.bot.latency * 1000)}ms**```autohotkey"
            for shard in self.bot.latencies:
                mensagem += f"\nShard {shard[0]}: {round(shard[1] * 1000)}ms"
            mensagem = mensagem + "```"
            await interaction.response.send_message(f"{mensagem}")


    @app_commands.command(name='uptime', description='Mostra o tempo de atividade da aplicação.')
    @permissao_usar_cmd()
    async def uptime(self, interaction: discord.Interaction):
        await comando_executado(interaction, self.bot)
        time_now = datetime.datetime.now().timestamp()
        uptime = time_now - self.bot.time_start
        await interaction.response.send_message(f"A aplicação está online há **{int(uptime / 3600)}h {int(uptime / 60) % 60}m {int(uptime % 60)}s**")


    @app_commands.command(name='status', description='Mostra o status da aplicação.')
    @permissao_usar_cmd()
    async def status(self, interaction: discord.Interaction):
        await comando_executado(interaction, self.bot)
        embed = discord.Embed(title="Status da aplicação", color=self.bot.color_embed_default)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.description = f"\
            \n**Nome:** {self.bot.user.name}\
            \n**ID:** {self.bot.user.id}\
            \n**Ping:** {round(self.bot.latency * 1000)}ms \
            \n**RAM:** {psutil.virtual_memory().used / 1024 / 1024:.0f}/{psutil.virtual_memory().total / 1024 / 1024:.0f}MB ({psutil.virtual_memory().percent}%) \
            \n**CPU:** {psutil.cpu_count()} núcleos lógicos e {psutil.cpu_percent()}% de sua capacidade total \
            \n**Shards:** {self.bot.shard_count} shards \
            \n**Guildas:** {len(self.bot.guilds)} \
            \n**Usuários:** {len(self.bot.users)} \
            \n**Uptime:** {int((datetime.datetime.now().timestamp() - self.bot.time_start) / 3600)}h {int((datetime.datetime.now().timestamp() - self.bot.time_start) / 60) % 60}m {int((datetime.datetime.now().timestamp() - self.bot.time_start) % 60)}s"
        embed.set_footer(text=f"{str(self.bot.status).title()}")
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name='logs', description='Exibe as últimas logs da aplicação.')
    @permissao_usar_cmd()
    async def logs(self, interaction: discord.Interaction):
        await comando_executado(interaction, self.bot)
        await interaction.response.defer()

        embed = discord.Embed(title="Logs da aplicação", color=self.bot.color_embed_default)
        erros = False
        with open('logs.log', 'r', encoding='utf-8') as file:
            logs = file.read()
        logs_enviar = ''
        for linha in logs.splitlines()[::-1]:
            if len(logs_enviar) + len(linha) > 2000:
                break
            if '[ERROR]' in linha or '[CRITICAL]' in linha:
                linha = f'-{linha}'
                erros = True
            logs_enviar = f"{linha}\n{logs_enviar}"

        embed.description = f'```diff\n{logs_enviar}```' if erros else f'```autohotkey\n{logs_enviar}```'
        embed.set_footer(text=f'Total de logs:  {len(logs.splitlines())}  ({round(os.path.getsize("logs.log") / 1024 / 1024, 2)}MB)')
        view = ButtonsDevelopersCommands(interaction.user)

        await interaction.followup.send(view=view, embed=embed)


    @app_commands.command(name='backup', description='Faz um backup completo da aplicação.')
    @permissao_usar_cmd()
    async def backup(self, interaction: discord.Interaction):
        await comando_executado(interaction, self.bot)
        await interaction.response.send_message("Iniciando backup...", ephemeral=False)
        zip = zipfile.ZipFile('Backup.zip', 'w', zipfile.ZIP_DEFLATED)
        for root, _, files in os.walk('.'):
            for file in files:
                if file == 'serviceAccountKey.json' or file == '.env' or file == 'Backup.zip' or file.endswith('.pyc'):
                    continue
                zip.write(os.path.join(root, file))
        zip.close()
        await interaction.user.send(content="Backup atual da aplicação.", file=discord.File('Backup.zip'))
        await interaction.edit_original_response(content="Backup concluído, arquivos enviados na DM.")
        os.remove('Backup.zip')

    
    @app_commands.command(name='configs', description='Lista todas as configurações da aplicação.')
    @permissao_usar_cmd()
    async def configs(self, interaction: discord.Interaction):
        await comando_executado(interaction, self.bot)
        config = configparser.ConfigParser()
        config.read('config.conf')
        mensagem = "```ini\n"
        for section in config.sections():
            mensagem += f"[{section}]\n"
            for key, value in config.items(section):
                mensagem += f"{key} = {value}\n"
            mensagem += "\n"
        mensagem += "```"
        await interaction.response.send_message(mensagem, ephemeral=False)


    @ping.error
    @ram.error
    @cpu.error
    @sync.error
    @shard.error
    @uptime.error
    @status.error
    @logs.error
    @backup.error
    @configs.error
    async def erros(self, interaction: discord.Interaction, error):
        await comando_executado_erro(interaction, error, critical=True)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=False)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=False)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DevelopersCommands(bot))