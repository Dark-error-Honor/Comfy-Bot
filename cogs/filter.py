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
        self.bad_words = ['neger', 'nigger', 'niger',
                          'dick', 'penis', 'pik', 'test', 'fuck']
        self.file = os.path.join('cogs', 'json', 'bank.json')
        self.mint = 4126655
        self.mute_length = [5, 15, 30, 'forever']
        self.admin_roles = ['Owner', 'Admins', 'Helper']

    @commands.Cog.listener()
    async def on_message(self, message):

        for i in self.admin_roles:
            role = discord.utils.get(message.guild.roles, name=i)

            if role in message.author.roles:
                return

        for bad_word in self.bad_words:
            if bad_word in message.content.lower():

                mute = discord.utils.get(
                    message.author.guild.roles, name='Muted')
                await message.author.add_roles(mute)

                await message.channel.send('That is not a comfy word.')
                await message.delete()

                await self.check_account(message.author)
                user = UserAccount(message.author)

                if user.mute_warning == 2 and user.mute_times == 0:
                    await self.mute_timer(
                        time=self.mute_length[0], message=message, user=user)

                elif user.mute_warning == 4 and user.mute_times == 1:
                    await self.mute_timer(
                        time=self.mute_length[1], message=message, user=user)

                elif user.mute_warning == 7 and user.mute_times == 2:
                    await self.mute_timer(
                        time=self.mute_length[2], message=message, user=user)

                elif user.mute_warning == 9 and user.mute_times == 3:
                    await self.mute_timer(
                        time=None, message=message, user=user)

                else:
                    user.mute_warning += 1
                    embed = await self.create_warning_embed(message=message, user=user)
                    await message.channel.send(embed=embed)
                    await self.update_account(user)

                await message.author.remove_roles(mute)

    async def create_warning_embed(self, message, *, user):
        if user.mute_times == 0:
            until_mute = 3 - user.mute_warning

        elif user.mute_times == 1:
            until_mute = 5 - user.mute_warning

        elif user.mute_times == 2:
            until_mute = 8 - user.mute_warning

        elif user.mute_times == 3:
            until_mute = 10 - user.mute_warning

        await message.channel.send(message.author.mention)
        embed = (discord.Embed(
            title='Warning',
            colour=discord.Colour.orange()
        )
            .add_field(name='{}.'.format(user.name), value='You are warned.', inline=False)
            .add_field(name='Why?', value='You have been warned because you used uncomfy words.', inline=False)
            .add_field(name='Until Mute', value=f'U will be muted for {self.mute_length[user.mute_times]} minutes if you use: {until_mute} more uncomfy words.', inline=False)
        )

        return embed

    async def create_mute_embed(self, time, user):
        embed = (discord.Embed(
            title='Mute',
            colour=discord.Colour(self.mint)
        )
            .add_field(name=f'I muted', value='{}.'.format(user.name), inline=False)
            .add_field(name='Duration', value=time, inline=False)
            .add_field(name='reason', value='Used multiple not comfy words', inline=True)
        )

        return embed

    async def mute_timer(self, time, message, *, user):

        if time:
            command = self.client.get_command('mute')
            ctx = await self.client.get_context(message)
            mute = discord.utils.get(
                message.author.guild.roles, name='Muted')

            user.mute_times += 1
            await message.author.add_roles(mute)
            embed = await self.create_mute_embed(str(time) + ' minutes', user)
            await ctx.send(embed=embed)

            await self.update_account(user)

            if time > 0:
                await asyncio.sleep(time * 60)
                await message.author.remove_roles(mute, reason='Time\'s up')

        else:
            mute = discord.utils.get(
                message.author.guild.roles, name='Muted')
            ctx = await self.client.get_context(message)
            await message.author.add_roles(mute)

            embed = await self.create_mute_embed('forever', user)
            await ctx.send(embed=embed)

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
