import discord
from discord.ext import commands
import asyncio

from .economy import UserAccount
from .economy import Economy


class Filter(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.bad_words = ['neger', 'dick', 'penis', 'test', 'nigger', 'niger']
        self.mint = 4126655

    @commands.Cog.listener()
    async def on_message(self, message):
        for bad_word in self.bad_words:
            if bad_word in message.content.lower():
                await message.channel.send('That is not a comfy word.')
                await message.delete()

                user = UserAccount(message.author)

                # command = self.client.get_command('mute')
                # ctx = await self.client.get_context(message)
                # role = discord.utils.get(
                #     message.author.guild.roles, name='Muted')
                # time = 5

                # await message.author.add_roles(role)
                # embed = (discord.Embed(
                #     title='Mute',
                #     colour=discord.Colour(self.mint)
                # )
                #     .add_field(name=f'I muted', value='{}.'.format(message.author), inline=False)
                #     .add_field(name='Duration', value=str(time) + ' minutes', inline=False)
                #     .add_field(name='reason', value='Used a not comfy word', inline=True)
                # )
                # await ctx.send(embed=embed)

                if time > 0:
                    await asyncio.sleep(time * 60)
                    await member.remove_roles(role, reason='Time\'s up')


def setup(client):
    client.add_cog(Filter(client))
