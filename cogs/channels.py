import discord
from discord.ext import commands


class Channels(commands.Cog):

    def __init__(self, client):
        self.client = client

    # LISTENERS

    # COMMANDS

    @commands.command()
    async def makec(self, ctx, *args):
        """make new channel args: 1: name 2: category 3: type 4: nsfw"""

        guild = ctx.message.guild
        for category in guild.categories:
            if category.name == args[1]:  # check if category matches 2nd argument
                if args[2] in 'text Text':
                    # make text channel
                    await guild.create_text_channel(args[0], category=category, nsfw=args[3])
                elif args[2] in 'Voice voice talk Talk':
                    # make voice channel
                    await guild.create_voice_channel(args[0], category=category)
                else:
                    await ctx.send('what the hell do you want me to make?')

    @commands.command()
    async def removec(self, ctx, name):
        """remove channel args: name"""

        for guild in self.client.guilds:
            for channel in guild.text_channels:
                if channel.name == name:
                    await channel.delete()

    # LOOPS


def setup(client):
    client.add_cog(Channels(client))
