import discord
from discord.ext import commands
import string
import random

import time
from datetime import datetime

import pymongo
from pymongo import MongoClient


cluster = MongoClient("MONGO_URI")

suggestions = cluster["mee9"]["suggestions"]


class mee9(commands.Cog, name='MEE9 Commands'):

  '''
  MEE9 Commands
  '''
  def __init__(self, bot):
      self.bot = bot

  @commands.command(
    brief='suggest a feature!',
    description='sends your suggestion to the <#809480477718085643> channel in the support server!')
  async def suggest(self, ctx, *, suggestion):
    user = ctx.author
  
    channel = await self.bot.fetch_channel(809480477718085643)

    embed=discord.Embed(title="New Suggestion:", description=suggestion, timestamp=datetime.utcnow(), color = random.randrange(0x1000000))

    embed.set_author(name=f"From {ctx.author}", icon_url=user.avatar_url)

    message = await channel.send('<@633307008879296512>', embed=embed)

    suggestionid = str(message.id)


    await message.add_reaction('✅')
    await message.add_reaction('❎')
    await ctx.message.add_reaction('✅')
    time.sleep(2)
    await ctx.message.delete()


  @commands.command(
    brief='report an issue',
    description='sends a message to the <#809911673271222284> channel in the support server')
  async def report(self, ctx, *, issue):
    user = ctx.author
    channell = await self.bot.fetch_channel(809911673271222284)
    embed=discord.Embed(title="Reported issue:", description=issue, timestamp=datetime.utcnow(), color = random.randrange(0x1000000))
    embed.set_author(name=f"From {ctx.author}", icon_url=user.avatar_url)
    
    await channell.send(embed)

    await ctx.message.add_reaction('✅')
    await ctx.send("Thanks for reporting the issue! ")
