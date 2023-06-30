from discord.ext import commands
import discord
from firebase_admin import db
import logging


class AutoRoleEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            request = db.reference('/servidores/' + str(member.guild.id) + '/autorole').get()
            if request is not None:
                cargos = []
                for i in range(0, len(request)):
                    cargo = member.guild.get_role(int(request[i]))
                    if cargo is not None:
                        cargos.append(cargo)
                await member.add_roles(*cargos, reason='Cargo automático.')

                for i in range(0, len(cargos)):
                    logging.info(
                        f'O autorole setou o cargo {cargos[i].id} para o usuário {member.id} no servidor {member.guild.id}.')
        except Exception as e:
            logging.error(f'Erro ao setar o autorole para o usuário {member.id} no servidor {member.guild.id}.')
            logging.error(e)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoRoleEvent(bot))
