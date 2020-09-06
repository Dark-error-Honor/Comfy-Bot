import discord
from discord.ext import commands


class Basics(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot Is Online')


def setup(client):
    client.add_cog(Basics(client))
