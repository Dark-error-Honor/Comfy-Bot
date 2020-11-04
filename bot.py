import discord
import os
import config
from discord.ext import commands

client = commands.Bot('-')
owners = ['D4rK_Honor']
# client.remove_command('help')


@client.command()
async def load(ctx, extension):
    if ctx.message.author.name in owners:
        try:
            client.load_extension(f'cogs.{extension}')
        except Exception as e:
            print(e)

        await ctx.send('loaded')
    else:
        await ctx.send('You are not my owner.')


@client.command()
async def unload(ctx, extension):
    if ctx.message.author.name in owners:
        try:
            client.unload_extension(f'cogs.{extension}')
        except Exception as e:
            print(e)

        await ctx.send('unloaded')
    else:
        await ctx.send('You are not my owner.')


@client.command()
async def reloadall(ctx):
    if ctx.message.author.name in owners:
        for filename in os.listdir(os.path.join(os.getcwd(), 'cogs')):
            if filename.endswith('.py'):
                try:
                    client.unload_extension(f'cogs.{filename[:-3]}')
                    client.load_extension(f'cogs.{filename[:-3]}')
                except Exception as e:
                    print(e)

        await ctx.send('reloaded')
    else:
        await ctx.send('You are not my owner.')


@client.command()
async def reload(ctx, extension):
    if ctx.message.author.name in owners:
        try:
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
            print(f'reloaded {extension}')
        except:
            pass

        await ctx.send(f'reloaded {extension}')
    else:
        await ctx.send('You are not my owner.')


for filename in os.listdir(os.path.join(os.getcwd(), 'cogs')):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'cogs.{filename[:-3]}')
        except Exception as e:
            print(e)

client.run(config.token)
