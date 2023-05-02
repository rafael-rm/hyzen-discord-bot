import discord
from discord import app_commands
from discord.ext import commands
import logging
from src.functions.comando_executado import comando_executado
from src.functions.comando_executado import comando_executado_erro


class InviteCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @app_commands.command(name='invite', description='Convidar o bot para o seu servidor.')
    async def invite(self, interaction: discord.Interaction):

        invite_bot = f'https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands'
        invite_guild = self.bot.config.get('INVITES', 'SUPPORT_SERVER')

        mensagem = f'Olá, eu sou o **{self.bot.user.name}** e estou aqui para te ajudar a gerenciar seu servidor!\n' \
                   f'Para me **adicionar** em seu servidor, clique [aqui]({invite_bot}).'

        embed = discord.Embed(
            title='',
            description=mensagem,
            color=self.bot.color_embed_default,
        )
        embed.set_author(name='Convite')

        guilds = len(self.bot.guilds)
        embed.set_footer(text=f'Atualmente me encontro em {guilds} servidores.')

        await interaction.response.send_message(embed=embed)
        await comando_executado(interaction, self.bot)


    @invite.error
    async def erros(self, interaction: discord.Interaction, error):
        await comando_executado_erro(interaction, error, critical=False)
        await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=False)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(InviteCommand(bot))