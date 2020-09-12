import discord
from discord.ext import commands


class Default(commands.Cog):

    def __init__(self, client):
        self.client = client

    # LISTENERS
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot Is Online')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Uhm... You forgot to give me a required argument.')

        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send('You are not comfy enough to do that.')

    # COMMANDS

    @commands.command()
    async def ping(self, ctx):
        """ Returns latency of Comfy Bot """
        await ctx.send(f'{str(round(self.client.latency * 1000))}ms')

    @commands.command(aliases=['clear'])
    async def clean(self, ctx, amount=50):
        """ clean messages args: amount """
        await ctx.send(f'deleting {amount} messages')
        await ctx.channel.purge(limit=amount + 2)

    # LOOPS


def setup(client):
    client.add_cog(Default(client))
