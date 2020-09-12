import discord
import os
from discord.ext import commands

client = commands.Bot('-')
owners = ['D4rK_Honor', 'rankzy']
folders = ['cogs', 'economy']
# client.remove_command('help')


@client.command()
async def load(ctx, extension):
    if ctx.message.author.name in owners:
        for folder in folders:
            try:
                client.load_extension(f'cogs.{extension}')
            except:
                pass

        await ctx.send('loaded')
    else:
        await ctx.send('You are not my owner.')


@client.command()
async def unload(ctx, extension):
    if ctx.message.author.name in owners:
        for folder in folders:
            try:
                client.unload_extension(f'{folder}.{extension}')
            except:
                pass

        await ctx.send('unloaded')
    else:
        await ctx.send('You are not my owner.')


@client.command()
async def reload(ctx):
    if ctx.message.author.name in owners:
        for folder in folders:
            for filename in os.listdir(os.path.join(os.getcwd(), folder)):
                if filename.endswith('.py'):
                    try:
                        client.unload_extension(f'{folder}.{filename[:-3]}')
                        client.load_extension(f'{folder}.{filename[:-3]}')
                    except Exception as e:
                        print(e)

        await ctx.send('reloaded')
    else:
        await ctx.send('You are not my owner.')


for folder in folders:
    for filename in os.listdir(os.path.join(os.getcwd(), folder)):
        if filename.endswith('.py'):
            try:
                client.load_extension(f'{folder}.{filename[:-3]}')
            except:
                pass

client.run('NzUyMjMyNTI4NjcyMTk0NTcw.X1UpIg.bKoBzgJIl5zRKq62ZoR45Ub2wAQ')
