from discord.ext import commands
from src.functions.comando_executado import comando_executado
from src.functions.comando_executado import comando_executado_erro
from src.functions.permissoes import permissao_desenvolvedor
import logging


class SyncCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')

    @staticmethod
    def permissao_usar_cmd():
        def verificar_permissaoes(ctx: commands.Context) -> bool:
            return permissao_desenvolvedor(ctx.author.id)

        return commands.check(verificar_permissaoes)

    @commands.command(name='sync', description='Sincroniza os comandos da aplicação.')
    @permissao_usar_cmd()
    async def sync(self, ctx: commands.Context):
        await comando_executado(ctx, self.bot)
        await ctx.send('Sincronizando aplicação com o Discord...')
        logging.info('Sincronizando aplicação com o Discord...')
        await ctx.bot.tree.sync()
        await ctx.send('Aplicação sincronizada com o Discord.')
        logging.info('Aplicação sincronizada com o Discord.')

    @sync.error
    async def erros(self, ctx: commands.Context, error):
        await comando_executado_erro(ctx, error, critical=True)
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Você não tem permissão para executar este comando.')
        else:
            await ctx.send('Ocorreu um erro ao executar este comando.')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SyncCommand(bot))
