import discord
from discord.ext import commands


class Basics(commands.Cog):

    def __init__(self, client):
        self.client = client

    # LISTENERS
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot Is Online')

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send('Uhm... You forgot to give me a required argument.')

    # COMMANDS

    @commands.command()
    async def ping(self, ctx):
        """ Returns latency of Comfy Bot """
        await ctx.send(f'{str(round(self.client.latency * 1000))}ms')

    @commands.command(aliases=['clear'])
    async def clean(self, ctx, amount=5):
        """ clean messages args: amount """
        await ctx.send(f'deleting {amount} messages')
        await ctx.channel.purge(limit=amount + 2)

    # @commands.command()
    # async def help(self, ctx):
    #     author = ctx.message.author

    #     embed = discord.Embed(
    #         colour=discord.Colour(4126655)
    #     )
    #     embed.set_author(name='Help')
    #     embed.add_field(
    #         name='-help:', value='Returns this help page', inline=False)
    #     embed.add_field(
    #         name='-ping:', value='Returns latency of the Comfy Bot', inline=False)
    #     embed.add_field(
    #         name='-clean:', value='Cleans \{amount\} messages', inline=False)
    #     embed.add_field(
    #         name='-clean:', value='Cleans \{amount\} messages', inline=False)

    #     await ctx.send(embed=embed)

    # LOOPS


def setup(client):
    client.add_cog(Basics(client))
