import discord
import os
from discord.ext import commands

client = commands.Bot('-')
client.remove_command('help')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send('loaded')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send('unloaded')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send('reloaded')


for filename in os.listdir(os.path.join(os.getcwd(), 'cogs')):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('NzUyMjMyNTI4NjcyMTk0NTcw.X1UpIg.bKoBzgJIl5zRKq62ZoR45Ub2wAQ')
