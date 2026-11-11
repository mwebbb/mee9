import discord
from discord.ext import commands
import string
import random
from discord.utils import get
import pymongo
from datetime import datetime
from pymongo import MongoClient


cluster = MongoClient("MONGO_URI")

suggestions = cluster["mee9"]["suggestions"]


class moderation(commands.Cog, name='Moderation'):

  '''
  MEE9 Commands
  '''
  def __init__(self, bot):
      self.bot = bot

  @commands.command(
    brief='deletes the specified messages',
    description='deletes the specified messages')
  @commands.has_permissions(manage_messages = True)
  async def purge(self, ctx, amt: int):
    await ctx.message.delete()
    if amt > 50:
      await ctx.send("To prevent API abuse, the maximum amount of messages you can delete is 50.")
    await ctx.channel.purge(limit=amt)
    amount = str(amt)
    embed=discord.Embed(title="Purge Successful", description=f"**{amount} messages** were successfully purged by {ctx.message.author}", color=0x00ff6e, timestamp=datetime.utcnow())
    await ctx.send(embed=embed)

  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx, member: discord.Member, *, reason=None):

      await member.kick(reason=reason)

      embed=discord.Embed(title="**Kicked**", description=f"{member} was kicked from the server by {ctx.author.name}!", timestamp=datetime.utcnow(), color = random.randrange(0x1000000))
      embed.set_author(name="Made by cgd", icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif")
      embed.set_thumbnail(url=member.avatar_url)
      await ctx.send(embed=embed)


  # @commands.command(
  #   brief='',
  #   description='')
  # async def mute(self, ctx, member: discord.Member):
  #   server = ctx.message.guild
  #   perms = discord.Permissions(send_messages=False, read_messages=True)
  #   await server.create_role(name='Muted', permissions=perms)
  #   role = get(member.server.roles, name="Muted")
  #   await self.bot.add_roles(member, role)

  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def ban(self, ctx, *, member: discord.Member, reason=None):

      await member.ban(reason=reason)

      embed=discord.Embed(title="**Banned**", description=f"{member} was banned from the server by {ctx.author.name}!", timestamp=datetime.utcnow(), color = random.randrange(0x1000000))
      embed.set_author(name="Made by cgd", icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif")
      embed.set_thumbnail(url=member.avatar_url)
      await ctx.send(embed=embed)

