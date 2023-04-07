import discord
from discord import app_commands
from discord.ext import commands
import logging
from src.functions.comando_executado import comando_executado
from src.functions.comando_executado import comando_executado_erro


class SayCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @app_commands.command(name='say', description='Enviar embed com uma mensagem através do bot.')
    @app_commands.describe(mensagem='Mensagem a ser enviada através do bot.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(embed_links=True, send_messages=True)
    async def say(self, interaction: discord.Interaction, *, mensagem: str):
        embed = discord.Embed(
            title = '',
            description = mensagem,
            color = self.bot.color_embed_default,
            timestamp = interaction.created_at,
        )

        if interaction.user.avatar:
            embed.set_footer(text=f'Enviado por {interaction.user.name}#{interaction.user.discriminator}', icon_url=interaction.user.avatar)
        else:
            embed.set_footer(text=f'Enviado por {interaction.user.name}#{interaction.user.discriminator}', icon_url=interaction.user.default_avatar)

        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Comando executado com sucesso!", ephemeral=True, delete_after=3)

        await comando_executado(interaction, self.bot)
        logging.info(f'Conteúdo enviado através do comando \'say\' executado por {interaction.user.id} no servidor {interaction.guild.id} no canal {interaction.channel.id}: "{mensagem}"')


    @say.error
    async def erros(self, interaction: discord.Interaction, error):
        await comando_executado_erro(interaction, error, critical=False)
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("O bot não tem permissão para executar esse comando, verifique se ele tem a permissão `Enviar mensagens` e `Inserir links`.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SayCommand(bot))