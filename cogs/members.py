import discord
from discord.ext import commands
import asyncio
import time as t

from .economy import UserAccount


class Members(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mint = 4126655
        self.mute_time = {}

    async def addCounter(self, member):
        for channel in member.guild.channels:
            print(channel.name)
            if 'e' in channel.name:
                print("changing")
                channel = await channel.edit(name='Members: {}'.format(
                    str(len([m for m in member.guild.members if not m.bot]))))
                print(channel)
                break
            else:
                channel = await member.guild.create_voice_channel("Members: {}".format(str(len([m for m in member.guild.members if not m.bot]))))
                break

    # LISTENERS
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name='Member')
        await member.add_roles(role)

        await self.addCounter(member)

        chan = await member.create_dm()
        await chan.send('Hello welcome to {}!'.format(member.guild))

    # COMMANDS
    @ commands.command()
    async def invite(self, ctx, *, memeber: discord.Member):
        """ Sends a dm with server invite to specified member """
        channel = await member.create_dm()
        await channel.send(await ctx.channel.create_invite())

    @ commands.command()
    async def roleadd(self, ctx, member: discord.Member, *, role):
        """ adds role to mentioned member """
        role = discord.utils.get(member.guild.roles, name=role)
        await member.add_roles(role)

    @ commands.command()
    async def rolerem(self, ctx, member: discord.Member, *, role):
        """ removes role to mentioned member """
        role = discord.utils.get(member.guild.roles, name=role)
        await member.remove_roles(role)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """ kicks memeber from server """
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """ bans member args: usr object """
        await member.ban(reason=reason, delete_message_days=2)

    @ commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """ unbans member args: name#tag """
        banned_users = await ctx.guild.bans()
        member_name, member_id = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_id):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}')

    @ commands.command()
    async def mute(self, ctx, member: discord.Member, time=0):
        """ mutes specified member for specified time """
        role = discord.utils.get(member.guild.roles, name='Muted')

        if not member:
            ctx.send('Give me someone to mute pls.')
            return

        if self.client.user != member:
            await member.add_roles(role)
            embed = (discord.Embed(
                title='Mute',
                colour=discord.Colour(self.mint)
            )
                .add_field(name=f'{ctx.author} muted', value='{}.'.format(member), inline=False)
                .add_field(name='Duration', value=str(time) + ' minutes', inline=False)
            )
            await ctx.send(embed=embed)

            if time > 0:
                self.mute_time[member.name +
                               str(member.discriminator)] = t.time() + time * 60
                print(self.mute_time)
                await asyncio.sleep(time * 60)
                await member.remove_roles(role, reason='Time\'s up')

        else:
            embed = discord.Embed(
                title='You can\'t mute me i am too comfy!',
                colour=discord.Colour(self.mint)
            )
            await ctx.send(embed=embed)
            pass

    @ commands.command()
    async def mutetime(self, ctx, *, member: discord.Member):
        try:
            await ctx.send(f'{member.name} is muted for {int(self.mute_time[member.name + str(member.discriminator)] - t.time())} seconds.')
            print(
                int((self.mute_time[member.name + str(member.discriminator)] - t.time())))
        except KeyError:
            await ctx.send(f'{member.name} is not muted.')

    # LOOPS


def setup(client):
    client.add_cog(Members(client))
