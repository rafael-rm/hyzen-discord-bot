import discord
from discord import app_commands
from discord.ext import commands
from src.functions.comando_executado import comando_executado
from src.functions.comando_executado import comando_executado_erro
from firebase_admin import db
import logging


@app_commands.guild_only()
class AutoRoleCommands(commands.GroupCog, name="autorole", description="Comandos do cargo automático"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @app_commands.command(name='adicionar', description='Adiciona um cargo ao autorole.')
    @app_commands.describe(cargo='Cargo que será adicionado ao autorole.')
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def adicionar(self, interaction: discord.Interaction, cargo: discord.Role):
        if cargo.id == interaction.guild.id:
            await interaction.response.send_message('Não posso adicionar o cargo **everyone** no autorole.')
            await comando_executado(interaction, self.bot)
            return

        if cargo.managed or cargo.is_bot_managed():
            await interaction.response.send_message('Não posso adicionar um cargo de bot no autorole.')
            await comando_executado(interaction, self.bot)
            return

        if cargo.position >= interaction.guild.me.top_role.position:
            await interaction.response.send_message('O cargo que deseja adicionar no autorole é maior ou igual ao meu cargo. Não posso adicionar.')
            await comando_executado(interaction, self.bot)
            return

        if cargo.position > interaction.user.top_role.position and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message('O cargo que deseja adicionar no autorole é maior que o seu cargo. Não posso adicionar.')
            await comando_executado(interaction, self.bot)
            return

        request = db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').get()

        cargo_ja_adicionado = False
        if request is not None:
            for i in range(0, len(request)):
                if request[i] == str(cargo.id):
                    cargo_ja_adicionado = True

        if request is None:
            request = []

        if cargo_ja_adicionado:
            await interaction.response.send_message('O cargo já se encontra adicionado ao autorole.')
        else:
            request.append(str(cargo.id))
            db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').set(request)
            await interaction.response.send_message('Cargo adicionado com sucesso.')

        await comando_executado(interaction, self.bot)


    @app_commands.command(name='remover', description='Remove um cargo ao autorole.')
    @app_commands.describe(cargo='Cargo que será removido do autorole.')
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def remover(self, interaction: discord.Interaction, cargo: discord.Role):
        request = db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').get()
        cargo_encontrado = False
        if request is not None:
            for i in range(0, len(request)):
                if request[i] == str(cargo.id):
                    cargo_encontrado = True
                    request.pop(i)
                    db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').set(request)
                    await interaction.response.send_message('Cargo removido do autorole com sucesso.')
        else:
            await interaction.response.send_message('Nenhum cargo foi adicionado ao autorole.')

        if not cargo_encontrado:
            await interaction.response.send_message('O cargo não se encontra adicionado ao autorole.')

        await comando_executado(interaction, self.bot)


    @app_commands.command(name='listar', description='Lista os cargos do autorole.')
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def listar(self, interaction: discord.Interaction):
        request = db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').get()
        if request is None:
            await interaction.response.send_message('Não há cargos no autorole.')
        else:
            cargos = ''
            for i in range(0, len(request)):
                cargos += f'<@&{request[i]}>\n'
            embed = discord.Embed(title='', description=cargos, color=self.bot.color_embed_default)
            embed.set_author(name='Cargos configurados para serem adicionados quando um novo usuário entrar no servidor.')
            await interaction.response.send_message(embed=embed)
        await comando_executado(interaction, self.bot)


    @adicionar.error
    @remover.error
    @listar.error
    async def erros(self, interaction: discord.Interaction, error):
        await comando_executado_erro(interaction, error, critical=False)
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=False)
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("A aplicação não tem permissões suficientes para executar esse comando, verifique se a permissão de `Gerenciar Cargos` está ativada.", ephemeral=False)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=False)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoRoleCommands(bot))