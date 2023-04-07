import discord
from discord import app_commands
from discord.ext import commands
from src.functions.comando_executado import comando_executado
from src.functions.comando_executado import comando_executado_erro
import random
import logging


@app_commands.guild_only()
class MixCommands(commands.GroupCog, name='mix', description='Comandos para organizar partidas de mix.'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @app_commands.command(name='sortear', description='Sortear os jogadores mencionados em 2 times.')
    @app_commands.describe(jogador_1='Jogador a ser sorteado.')
    @app_commands.describe(jogador_2='Jogador a ser sorteado.')
    @app_commands.describe(jogador_3='Jogador a ser sorteado.')
    @app_commands.describe(jogador_4='Jogador a ser sorteado.')
    @app_commands.describe(jogador_5='Jogador a ser sorteado.')
    @app_commands.describe(jogador_6='Jogador a ser sorteado.')
    @app_commands.describe(jogador_7='Jogador a ser sorteado.')
    @app_commands.describe(jogador_8='Jogador a ser sorteado.')
    @app_commands.describe(jogador_9='Jogador a ser sorteado.')
    @app_commands.describe(jogador_10='Jogador a ser sorteado.')
    async def sortear(self, interaction: discord.Interaction, jogador_1: discord.Member = None, jogador_2: discord.Member = None, jogador_3: discord.Member = None, jogador_4: discord.Member = None, jogador_5: discord.Member = None, jogador_6: discord.Member = None, jogador_7: discord.Member = None, jogador_8: discord.Member = None, jogador_9: discord.Member = None, jogador_10: discord.Member = None):
        jogadores = []
        time1 = []
        time2 = []

        if jogador_1 is not None:
            jogadores.append(jogador_1.mention)
        if jogador_2 is not None:
            jogadores.append(jogador_2.mention)
        if jogador_3 is not None:
            jogadores.append(jogador_3.mention)
        if jogador_4 is not None:
            jogadores.append(jogador_4.mention)
        if jogador_5 is not None:
            jogadores.append(jogador_5.mention)
        if jogador_6 is not None:
            jogadores.append(jogador_6.mention)
        if jogador_7 is not None:
            jogadores.append(jogador_7.mention)
        if jogador_8 is not None:
            jogadores.append(jogador_8.mention)
        if jogador_9 is not None:
            jogadores.append(jogador_9.mention)
        if jogador_10 is not None:
            jogadores.append(jogador_10.mention)

        random.shuffle(jogadores)

        for i in range(0, len(jogadores)):
            for j in range(0, len(jogadores)):
                if i != j and jogadores[i] == jogadores[j]:
                    await interaction.response.send_message('Um mesmo jogador não pode ser mencionado mais de uma vez.')
                    await comando_executado(interaction, self.bot)
                    return

        for i in range(0, len(jogadores)):
            if i % 2 == 0:
                time1.append(jogadores[i])
            else:
                time2.append(jogadores[i])
        if len(time1) == 0 or len(time2) == 0:
            await interaction.response.send_message('É necessário mencionar pelo menos 2 jogadores.')
        else:
            embed = discord.Embed(title='', description='Os dois times foram sorteados com sucesso.',  color=self.bot.color_embed_default)
            embed.set_author(name='Sorteio dos times', icon_url='https://i.imgur.com/IfI5eub.png')
            embed.add_field(name='Time 1', value='\n'.join(time1), inline=True)
            embed.add_field(name='Time 2', value='\n'.join(time2), inline=True)
            if interaction.user.avatar:
                embed.set_footer(text=f'Sorteio realizado por {interaction.user.name}', icon_url=interaction.user.avatar)
            else:
                embed.set_footer(text=f'Sorteio realizado por {interaction.user.name}', icon_url=interaction.user.default_avatar)
            await interaction.response.send_message(embed=embed)
        await comando_executado(interaction, self.bot)


    @sortear.error
    async def erros(self, interaction: discord.Interaction, error):
        await comando_executado_erro(interaction, error, critical=False)
        await interaction.response.send_message('Ocorreu um erro ao executar este comando. Por favor, tente novamente mais tarde.')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MixCommands(bot))