import discord
from discord.ext import commands
import asyncio
import json
import os

from .economy import UserAccount
from .economy import Economy


class Filter(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.bad_words = ['neger', 'nigger',
                          'niger', 'dick', 'penis', 'pik', 'test']
        self.file = os.path.join('cogs', 'json', 'bank.json')
        self.mint = 4126655

    @commands.Cog.listener()
    async def on_message(self, message):
        for bad_word in self.bad_words:
            if bad_word in message.content.lower():
                await message.channel.send('That is not a comfy word.')
                await message.delete()

                await self.check_account(message.author)
                user = UserAccount(message.author)

                if user.mute_warning == 3 and user.mute_times == 0:
                    command = self.client.get_command('mute')
                    ctx = await self.client.get_context(message)
                    role = discord.utils.get(
                        message.author.guild.roles, name='Muted')
                    time = 5

                    await message.author.add_roles(role)
                    user.mute_times += 1
                    embed = await self.create_mute_embed(5, user)
                    await ctx.send(embed=embed)

                    await self.update_account(user)

                    if time > 0:
                        await asyncio.sleep(time * 60)
                        await message.author.remove_roles(role, reason='Time\'s up')

                else:
                    user.mute_warning += 1
                    await self.update_account(user)

    async def create_mute_embed(self, time, user):
        embed = (discord.Embed(
            title='Mute',
            colour=discord.Colour(self.mint)
        )
            .add_field(name=f'I muted', value='{}.'.format(user.name), inline=False)
            .add_field(name='Duration', value=str(time) + ' minutes', inline=False)
            .add_field(name='reason', value='Used multiple not comfy words', inline=True)
        )

        return embed

    async def update_account(self, user):
        user.users[user.entry]['bank'] = user.bank
        user.users[user.entry]['wallet'] = user.wallet
        user.users[user.entry]['excperience'] = user.exp
        user.users[user.entry]['level'] = user.level
        user.users[user.entry]['mute_warn'] = user.mute_warning
        user.users[user.entry]['mute_times'] = user.mute_times

        with open(user.file, 'w') as f:
            json.dump(user.users, f)

        user = UserAccount(user)

    async def check_account(self, user):

        with open(self.file, 'r') as f:
            users = json.load(f)

        username, userid = user.name, user.discriminator

        if (username + str(userid)) not in (users):  # if username + userid not in list users
            entry = username + str(userid)
            users[entry] = {}
            users[entry]['bank'] = 0
            users[entry]['wallet'] = 0
            users[entry]['excperience'] = 0
            users[entry]['level'] = 1
            users[entry]['mute_warn'] = 0
            users[entry]['mute_times'] = 0

            with open(self.file, 'w') as f:
                json.dump(users, f)

        else:
            pass


def setup(client):
    client.add_cog(Filter(client))
