import discord
from discord.ext import commands

import json
import os
import datetime


class BankAccount():
    def __init__(self, user):

        self.file = os.path.join('cogs', 'bank.json')
        with open(self.file, 'r') as f:
            self.users = json.load(f)

        self.user = user
        self.name = user.name
        self.discriminator = user.discriminator
        self.entry = self.name + self.discriminator
        self.bank = self.users[self.entry]['bank']
        self.wallet = self.users[self.entry]['wallet']
        self.exp = self.users[self.entry]['excperience']
        self.level = self.users[self.entry]['level']


class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.file = os.path.join('cogs', 'bank.json')

    # LISTENERS
    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.check_account(member)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        else:

            await self.check_account(message.author)

            member = BankAccount(message.author)

            await self.update_account(member)
            await self.add_excperience(member, 5)
            await self.level_up(member, message.channel)

    # HELP COMMANDS
    async def update_account(self, user):

        user.users[user.entry]['bank'] = user.bank
        user.users[user.entry]['wallet'] = user.wallet
        user.users[user.entry]['excperience'] = user.exp
        user.users[user.entry]['level'] = user.level

        with open(user.file, 'w') as f:
            json.dump(user.users, f)

        user = BankAccount(user)

    async def check_account(self, user):

        with open(self.file, 'r') as f:
            users = json.load(f)

        username, userid = user.name, user.discriminator

        if (username + str(userid)) not in (users):
            entry = username + str(userid)
            users[entry] = {}
            users[entry]['bank'] = 0
            users[entry]['wallet'] = 0
            users[entry]['excperience'] = 0
            users[entry]['level'] = 1

            with open(self.file, 'w') as f:
                json.dump(users, f)

        else:
            pass

    async def add_excperience(self, user, xp):
        user.exp += xp
        await self.update_account(user)

    async def level_up(self, user, channel):

        lvl_start = user.level
        lvl_end = int(user.exp ** (1/4))

        if lvl_start < lvl_end:
            await channel.send(f'{user.user.mention}\'s comfyness has leveled up to {lvl_end}')

        user.level = lvl_end
        await self.update_account(user)

    # COMMANDS

    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        with open(self.file, 'r') as f:
            users = json.load(f)

        await self.check_account(ctx.message.author)

    @commands.command()
    async def level(self, ctx, *, member: discord.Member = None):
        try:
            if not member:
                member = BankAccount(ctx.message.author)
            else:
                member = BankAccount(member)
            await ctx.send(f'{member.user.mention} is level: {member.level}')

        except KeyError:
            if member.name == 'Comfy Bot':
                await ctx.send(f'{member.name} has an infinite comfy level')
            else:
                await ctx.send(f'{member.name} has no comfy level')


def setup(client):
    client.add_cog(Economy(client))
