import discord
import os
from discord.ext import commands

client = commands.Bot('-')
owners = ['D4rK_Honor', 'rankzy']
# client.remove_command('help')


@client.command()
async def load(ctx, extension):
    if ctx.message.author.name in owners:
        client.load_extension(f'cogs.{extension}')
        await ctx.send('loaded')
    else:
        await ctx.send('You are not my owner.')


@client.command()
async def unload(ctx, extension):
    if ctx.message.author.name in owners:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send('unloaded')
    else:
        await ctx.send('You are not my owner.')


@client.command()
async def reload(ctx):
    if ctx.message.author.name in owners:
        for filename in os.listdir(os.path.join(os.getcwd(), 'cogs')):
            if filename.endswith('.py'):
                client.unload_extension(f'cogs.{filename[:-3]}')
                client.load_extension(f'cogs.{filename[:-3]}')
        await ctx.send('reloaded')
    else:
        await ctx.send('You are not my owner.')


for filename in os.listdir(os.path.join(os.getcwd(), 'cogs')):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('NzUyMjMyNTI4NjcyMTk0NTcw.X1UpIg.bKoBzgJIl5zRKq62ZoR45Ub2wAQ')
