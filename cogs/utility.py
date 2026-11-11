import discord
from discord.ext import commands
from kutt import kutt

from datetime import datetime
import pytz
import random



class Utility(commands.Cog):

  '''
  Commands that do useful stuff
  '''
  def __init__(self, bot):
      self.bot = bot
      

  @commands.command(
  brief="shows information about the discord server.",
  description="displays detailed information about the current discord server."
)
  async def serverinfo(self, ctx):
      name = str(ctx.guild.name)
      description = str(ctx.guild.description)
      owner = str(ctx.guild.owner)
      id = str(ctx.guild.id)
      region = str(ctx.guild.region)
      memberCount = str(ctx.guild.member_count)
      icon = str(ctx.guild.icon_url)
      embed = discord.Embed(
          title=name + " Server Information",
          description=description,
          color = random.randrange(0x1000000),
          timestamp=datetime.utcnow()
        )
      embed.set_thumbnail(url=icon)
      embed.add_field(name="Owner", value=owner, inline=True)
      embed.add_field(name="Server ID", value=id, inline=True)
      embed.add_field(name="Region", value=region, inline=True)
      embed.add_field(name="Member Count", value=memberCount, inline=True)
      await ctx.send(embed=embed)


  @commands.command(
    brief="creates a poll",
    description="creates a poll with 2 (optional) custom options"
  )
  async def poll(self, ctx, question, option1=None, option2=None):
    if option1==None and option2==None:
      await ctx.channel.purge(limit=1)
      message = await ctx.send(f"```New poll: \n{question}```\n**✅ = Yes**\n**❎ = No**")
      await message.add_reaction('✅')
      await message.add_reaction('❎')
    elif option1==None:
      await ctx.channel.purge(limit=1)
      message = await ctx.send(f"```New poll: \n{question}```\n**✅ = {option1}**\n**❎ = No**")
      await message.add_reaction('✅')
      await message.add_reaction('❎')
    elif option2==None:
      await ctx.channel.purge(limit=1)
      message = await ctx.send(f"```New poll: \n{question}```\n**✅ = Yes**\n**❎ = {option2}**")
      await message.add_reaction('✅')
      await message.add_reaction('❎')
    else:
      await ctx.channel.purge(limit=1)
      message = await ctx.send(f"```New poll: \n{question}```\n**✅ = {option1}**\n**❎ = {option2}**")
      await message.add_reaction('✅')
      await message.add_reaction('❎')

  @commands.command(
     brief='shows the bot stats',
     description='shows the bots stats')
  async def botstats(self, ctx):
    servers = str(len(self.bot.guilds))
    embed=discord.Embed(title="Bot Stats", color = random.randrange(0x1000000), timestamp=datetime.utcnow())
    embed.add_field(name="API Version:", value=f"`{discord.__version__}`", inline=False)
    embed.add_field(name="Servers:", value=f"`{servers}`", inline=False)
    embed.add_field(name="Verification %:", value=f"`{servers}%`", inline=False)
    users = len(self.bot.users)
    embed.add_field(name="Users:", value=f"`{users}`", inline=True)
    embed.set_author(name="Made by cgd", icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif")
    await ctx.send(embed=embed)




  @commands.command(
    brief='embeds something',
    description='embeds a message')
  async def embed(self, ctx, text):
    embed=discord.Embed(title=text, color = 0x2f3136, timestamp=datetime.utcnow())
    await ctx.send(embed=embed)
    await ctx.message.delete()






  @commands.command(brief='get information about a user', description='usage: .whois [@user]')
  async def whois(self, ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author
        
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color = random.randrange(0x1000000), description=user.mention, timestamp=datetime.utcnow())
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    # members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    # embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)