import discord
from discord import app_commands
from discord.ext import commands
import logging
from src.functions.comando_executado import comando_executado
from src.functions.comando_executado import comando_executado_erro


class ClearCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @app_commands.command(name='clear', description='Limpar mensagens do canal.')
    @app_commands.describe(quantidade='Quantidade de mensagens a serem excluídas.', usuario='Usuário que terá as mensagens excluídas.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, quantidade: int, usuario: discord.Member = None):
        await interaction.response.defer()

        mensagens_apagar = []

        if quantidade > 500:
            await interaction.followup.send(content="Você não pode excluir mais de **500** mensagens de uma vez!")
        else:
            async for mensagem in interaction.channel.history(limit=quantidade+1):
                if ((interaction.created_at - mensagem.created_at).days <= 14 and interaction.created_at > mensagem.created_at):
                    if usuario is None: 
                        mensagens_apagar.append(mensagem)
                    elif usuario == mensagem.author:
                        mensagens_apagar.append(mensagem)

            if len(mensagens_apagar) == 0:
                await interaction.followup.send(content="Nenhuma mensagem foi excluída deste canal, pois todas as mensagens são mais antigas que **14** dias.")
            
            if len(mensagens_apagar) != quantidade:
                await interaction.channel.delete_messages(mensagens_apagar)
                await interaction.followup.send(content=f"Apenas **{len(mensagens_apagar)}** mensagens foram excluídas deste canal, pois as outras foram enviadas a mais de **14** dias.")
            else:
                await interaction.channel.delete_messages(mensagens_apagar)
                await interaction.followup.send(content=f"**{len(mensagens_apagar)}** mensagens foram excluídas deste canal.")
        
        await comando_executado(interaction, self.bot)


    @clear.error
    async def erros(self, interaction: discord.Interaction, error):
        await comando_executado_erro(interaction, error, critical=False)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=False)
        elif isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message("O bot não tem permissão para executar esse comando, verifique se ele tem a permissão `Gerenciar mensagens`.", ephemeral=False)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=False)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ClearCommand(bot))