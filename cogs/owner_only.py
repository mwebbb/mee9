import discord
from discord.ext import commands
import os, shutil
from time import sleep as s
from datetime import datetime
import random


from replit import db

class owner_only(commands.Cog, name="Dev commands"):

  '''
  Owner only commands
  '''
  def __init__(self, bot):
      self.bot = bot

  
  @commands.command(
    brief='sets what the bot is watching',
    description='sets what the bot is watching')
  async def watch(self, ctx, *, arg):
    if ctx.message.author.id == 633307008879296512:
      await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=arg))
      embed=discord.Embed(title="Success!", description="Changed the watching status to `" + arg + "`!" , color = random.randrange(0x1000000), timestamp=datetime.utcnow())
      await ctx.send(embed=embed)
    else:
      embed=discord.Embed(title="Error:", description="You aren't allowed to do that!", color = random.randrange(0x1000000))
      await ctx.send(embed=embed)

  @commands.command()
  async def delfiles(self, ctx):
    if ctx.message.author.id == 633307008879296512:
      folder = 'cdn'
      for filename in os.listdir(folder):
          file_path = os.path.join(folder, filename)
          try:
              if os.path.isfile(file_path) or os.path.islink(file_path):
                  os.unlink(file_path)
              elif os.path.isdir(file_path):
                  shutil.rmtree(file_path)
          except Exception as e:
              await ctx.send('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
      await ctx.send("no lmao")

  @commands.command(
    brief='sets what the bot is watching',
    description='sets what the bot is watching')
  async def play(self, ctx, *, arg):
    if ctx.message.author.id == 633307008879296512:
      await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=arg))
      embed=discord.Embed(title="Success!", description="Changed the playing status to `" + arg + "`!" , color = random.randrange(0x1000000), timestamp=datetime.utcnow())
      await ctx.send(embed=embed)
    else:
      embed=discord.Embed(title="Error:", description="You aren't allowed to do that!", color = random.randrange(0x1000000), timestamp=datetime.utcnow())
      await ctx.send(embed=embed)


  @commands.command(
    brief='sets what the bot is streaming',
    description='sets what the bot is streaming')
  async def stream(self, ctx, url, *, arg):
    if ctx.message.author.id == 633307008879296512:
      await self.bot.change_presence(activity=discord.Streaming(name=arg, url=url))
      embed=discord.Embed(title="Success!", description="Changed the streaming status to `" + arg + "`!" , color = random.randrange(0x1000000), timestamp=datetime.utcnow())
      await ctx.send(embed=embed)
    else:
      embed=discord.Embed(title="Error:", description="You aren't allowed to do that!", color = random.randrange(0x1000000))
      await ctx.send(embed=embed)

  @commands.command(
    brief='sets what the bot is streaming',
    description='sets what the bot is streaming')

  async def listen(self, ctx, *, arg):
    if ctx.message.author.id ==633307008879296512:
      await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=arg))  
      embed=discord.Embed(title="Success!", description="Changed the listening status to `" + arg + "`!" , color = random.randrange(0x1000000), timestamp=datetime.utcnow())
      await ctx.send(embed=embed)
      

    else:
      embed=discord.Embed(title="Error:", description="You aren't allowed to do that!", color = random.randrange(0x1000000))
      await ctx.send(embed=embed)

  @commands.command(
    brief='sets what the bot is competing in',
    description='sets what the bot is competing in')

  async def compete(self, ctx, *, arg):
    if ctx.message.author.id == 633307008879296512:
      await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=arg))  
      embed=discord.Embed(title="Success!", description="Changed the competing status to `" + arg + "`!" , color = random.randrange(0x1000000))
      await ctx.send(embed=embed)
      

    else:
      embed=discord.Embed(title="Error:", description="You aren't allowed to do that!", color = random.randrange(0x1000000))
      await ctx.send(embed=embed)


  @commands.command(
    brief='gives the mentioned user  credits',
    description='gives the mentioned user  credits')

  async def addcredits(self, ctx, member: discord.Member, amount):
    if ctx.message.author.id == 633307008879296512:
      membercredits = str(member.id) + "_" + "credits"


      creditamt = int(amount)


      # oldcredits = db.find({})

      # newcredits = oldcredits + creditamt


      # db[membercredits] = newcredits

      embed=discord.Embed(title="Success!", description=f"Gave {member} {amount} credits!", color = random.randrange(0x1000000), timestamp=datetime.utcnow())
      await ctx.send(embed=embed)
      

    else:
      embed=discord.Embed(title="Error:", description="You aren't allowed to do that!", color = random.randrange(0x1000000))
      await ctx.send(embed=embed)


  @commands.command(
    brief='gives the mentioned user  credits',
    description='gives the mentioned user  credits')

  async def takecredits(self, ctx, member: discord.Member, amount):
    if ctx.message.author.id == 633307008879296512:
      membercredits = str(member.id) + "_" + "credits"

      
      creditamt = int(amount)
  

      oldcredits = db[membercredits]

      newcredits = oldcredits - creditamt


      db[membercredits] = newcredits

      embed=discord.Embed(title="Success!", description=f"Took {amount} credits away from {member}.", color = random.randrange(0x1000000), timestamp=datetime.utcnow())
      await ctx.send(embed=embed)
      

    else:
      embed=discord.Embed(title="Error:", description="You aren't allowed to do that!", color = random.randrange(0x1000000))
      await ctx.send(embed=embed)






  @commands.command(
    brief="check the user's credits",
    description="check the user's credits")

  async def credits(self, ctx, member: discord.Member):

    membercredits = str(member.id) + "_" + "credits"


    

    credits = db[membercredits]

    if membercredits == None:
      balance = '0'
    else:
      balance = credits

    await ctx.send(balance)
      




  @commands.command(
      brief='evaluates input',
      description='evaluates input')
  async def eval(self, ctx, *, input):
    if ctx.message.author.id == 633307008879296512:

      result = eval(input)

      await ctx.send(f"```{result}```")
      

    else:
      embed=discord.Embed(title="Error:", description="You aren't allowed to do that!", color = random.randrange(0x1000000))
      await ctx.send(embed=embed)

  @commands.command(
    brief='accepts a suggestion',
    description='accepts a suggestion')
  async def accept(self, ctx, message, *, response):
    if ctx.message.author.id == 633307008879296512:


      suggestion = db[message]

      description = "**Suggestion:** " + suggestion + "\n**Response:** " + response


      embed=discord.Embed(title="Suggestion accepted", description=description, color=0x1eff00)
      embed.set_author(name="Made by cgd", icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif")
      channel = await self.bot.fetch_channel(810591278113751082)
      await channel.send(embed=embed)
      await ctx.message.delete()
    else:
      embed=discord.Embed(title="Error:", description="You aren't allowed to do that!", color = random.randrange(0x1000000))
      await ctx.send(embed=embed)

  @commands.command(
    brief='denies a suggestion D: ',
    description='denies a suggestion')

  async def deny(self, ctx, message, *, response):
    if ctx.message.author.id == 633307008879296512:



      suggestion = db[message]
      
      description = "**Suggestion:** " + suggestion + "\n**Response:** " + response



      embed=discord.Embed(title="Suggestion denied", description=description, color = random.randrange(0x1000000))
      embed.set_author(name="Made by cgd", icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif")
      channel = await self.bot.fetch_channel(810591278113751082)
      await channel.send(embed=embed)
      await ctx.message.delete()


      
  @commands.command(
      brief='force-sends a message',
      description='force-sends a message')
  async def forcesend(self, ctx, channel, *, message):
    if ctx.message.author.id == 633307008879296512:
      
      channelid = int(channel)

      channel2 = await self.bot.fetch_channel(channelid)

      initiate = await ctx.send("<a:loading:813578482717556787> Attempting to send message.")

      s(0.4)
      await channel2.send(message) # sending the message

      embed=discord.Embed(title="Success!", description=f"Sent '{message}' to <#{channel}>!", color = random.randrange(0x1000000))

      await initiate.edit(content=None, embed = embed)

  # @commands.command(
  #   brief='sets the mentioned users credits',
  #   description='sets the mentioned users credits')

  # async def setcredits(self, ctx, member: discord.Member, amount):
  #   if ctx.message.author.id == 633307008879296512:

      
  #     membercredits = str(member.id) + "_" + "credits"


  #     creditamt = int(amount)



  #     newcredits = creditamt
    

  #     db[membercredits] = newcredits

  #     embed=discord.Embed(title="Success!", description=f"Set {member}'s credits to {amount}", color = random.randrange(0x1000000))
  #     await ctx.send(embed=embed)
      

  #   else:
  #     embed=discord.Embed(title="Error:", description="You aren't allowed to do that!", color = random.randrange(0x1000000))
  #     await ctx.send(embed=embed)

  @commands.command(description='sends a message to every server the bot is in')
  async def broadcast(self, ctx, *, msg):
      if ctx.message.author.id == 633307008879296512:

        for guild in self.bot.guilds:
            for channel in guild.channels:
                try:
                    await channel.send(msg)
                except Exception:
                    continue
                else:
                    break

  



# @commands.command(brief='deletes a users data from the database', description='deletes a users data from the database')
# async def deluser(self, ctx, member: discord.Member, name='deluser'):
#   if ctx.message.author.id == 633307008879296512:
#     id = str(member.id)
#     progress = await ctx.send(f"<a:loading:813578482717556787> Deleting user data for id {id} (<@{id}>...)")
#     s(3)
#     del db[f"{id}_credits"]
#     await progress.edit(content=f"<a:check:737485693525426257> Successfully deleted user data for id `{id}` (<@{id}>)")
#   else:
#     embed=discord.Embed(title="Error:", description="You aren't allowed to do that!",color = random.randrange(0x1000000))
#     await ctx.send(embed=embed)