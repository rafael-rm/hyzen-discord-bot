import discord
from discord import app_commands
from discord.ext import commands
import logging
from src.functions.comando_executado import comando_executado
from src.functions.comando_executado import comando_executado_erro


class AvatarCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @app_commands.command(name='avatar', description='Exibe o seu avatar ou o de outro usuário.')
    @app_commands.describe(usuario='Usuário para exibir o avatar.')
    async def avatar(self, interaction: discord.Interaction, usuario: discord.User = None):
        if usuario is None:
            usuario = interaction.user

        embed = discord.Embed(
            title='',
            color=self.bot.color_embed_default,
        )

        avatar = usuario.avatar
        if avatar is None:
            embed.set_author(name='Avatar de ' + usuario.name)
            embed.description = 'Este usuário não possui um avatar.'
        else:
            embed.set_author(name='Avatar de ' + usuario.name)
            embed.description = f'[[Clique aqui para baixar]]({avatar})'
            embed.set_image(url=usuario.avatar)

        await interaction.response.send_message(embed=embed)
        await comando_executado(interaction, self.bot)


    @avatar.error
    async def erros(self, interaction: discord.Interaction, error):
        await comando_executado_erro(interaction, error, critical=False)
        await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=False)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AvatarCommand(bot))