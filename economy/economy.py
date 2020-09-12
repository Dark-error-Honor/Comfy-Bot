import discord
from discord.ext import commands

import json
import os


class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def account(self, user):
        print('open account')
        with open('./bank.json', 'r') as f:
            users = json.load(f)
        print(users)

        if str(user.id) in users:
            return

        else:
            users[str(user.id)]['wallet'] = 0
            users[str(user.id)]['bank'] = 0

        with open('bank.json', 'w') as f:
            json.dump(users, f)

    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        print('balance command')
        await self.account(ctx.message.author)


def setup(client):
    client.add_cog(Economy(client))
