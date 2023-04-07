import logging
from firebase_admin import db
import discord
from discord.ext import commands
from discord import app_commands


# TODO: Adicionar o ID da shard em que o comando foi executado nas mensagens de log de execução de comandos.


async def comando_executado(comando, bot):
    if type(comando) is discord.Interaction: 
        autor = comando.user
    else:
        autor = comando.author

    if comando.guild is None: 
        local = 'via DM'
    else:
        local = f'no servidor {comando.guild.id}' 

    logging.info(f'Comando \'{comando.command.name}\' executado por {autor.id} {local}.')
    await contador_comandos(bot)


async def comando_executado_erro(comando, erro, critical):
    if type(comando) is discord.Interaction: 
        autor = comando.user
    else:
        autor = comando.author

    if comando.guild is None: 
        local = 'via DM'
    else:
        local = f'no servidor {comando.guild.id}' 

    msg = f'Ocorreu um erro durante a execução do comando \'{comando.command.name}\'. O comando havia sido executado por {autor.id} {local}.'

    if isinstance(erro, commands.CheckFailure) or isinstance(erro, commands.MissingPermissions) or isinstance(erro, app_commands.CheckFailure):
        msg = f'O usuário {autor.id} tentou executar o comando \'{comando.command.name}\' {local}, mas não possui permissão para isso.'
        logging.info(msg)
        if critical:
            await tentativa_comando_critico(comando)
    else:
        msg = f'Ocorreu um erro durante a execução do comando \'{comando.command.name}\'. O comando havia sido executado por {autor.id} {local}.'
        logging.warning(msg)
        logging.error(f'{erro}')


async def tentativa_comando_critico(comando):
        if type(comando) is discord.Interaction: 
            autor = comando.user
        else:
            autor = comando.author

        if comando.guild is None: 
            local = 'via DM'
        else:
            local = f'no servidor {comando.guild.id}' 

        logging.warn(f'Tentativa de execução de comando crítico ({comando.command.name}) por {autor.id} {local}.')


async def contador_comandos(bot):  
    bot.cache_comandos_executados += 1 
    if bot.cache_comandos_executados >= 5:
        request = db.reference('/global/comandos-executados')
        if request.get() is None:
            request.set(bot.cache_comandos_executados)
        else:
            request.set(request.get() + bot.cache_comandos_executados)
        bot.cache_comandos_executados = 0