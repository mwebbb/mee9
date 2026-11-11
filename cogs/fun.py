import discord
from discord.ext import commands
import string
import random
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from art import *
import time
import nekos
import urllib.parse
import xkcd
from datetime import datetime


class Fun(commands.Cog):

  '''
  Fun commands
  '''
  def __init__(self, bot):
      self.bot = bot


    
  @commands.command(
    brief='generates a random nitro code', 
    description='generates a random nitro gift (note: this is a joke dont expect it to work)')
  async def nitro(self, ctx):
    letters = string.ascii_letters
    nitro = "discord.gift/" + ''.join(random.choice(letters) for i in range(16))
    await ctx.send(nitro)

  @commands.command(
      brief='random cat image ',
      description='random cat image')
  async def cat(self, ctx):
    await ctx.send(nekos.cat())



  @commands.command(
      brief='makes emojis out of words',
      description='makes emojis out of words')
  async def emojify(self, ctx, *, text):
    step1 = text.lower()
    step2 = "".join([f":regional_indicator_{letter}:" for letter in step1])

    finalized = step2.replace(':regional_indicator_ :', ' ')


    await ctx.send(finalized)

  @commands.command(
      brief='asciifies text',
      description='turns your text into ascii')
  async def asciify(self, ctx, font=None, *, text):

    if font == None:
      
      Art=text2art(text, font='standard')



      await ctx.send(f'```\n{Art}\n```')

    else:

      asciifont = font.lower()


      Art=text2art(text, font=asciifont)



      await ctx.send(f'```\n{Art}\n```')

  @commands.command(
      brief='',
      description='')
  async def face(self, ctx):
    face = art("random")
    await ctx.send(f'`{face}`')

  @commands.command(
      brief='all ascii fonts with examples',
      description='all ascii fonts with examples')
  async def fonts(self, ctx):
    file = discord.File("fonts.txt", filename="fonts.txt")
    await ctx.send('heres the file', file=file)



  @commands.command(
      brief='generates a minecraft-style achievement!',
      description='generates a minecraft-style achievement!')
  async def achievement(self, ctx, *, text):


    iconint = random.randint(1, 39)

    icon = str(iconint)


    encoded = urllib.parse.quote(text)


    achievement = 'https://minecraftskinstealer.com/achievement/' + icon + '/Achievement+get!' + '/' + encoded
    


    embed=discord.Embed(color = random.randrange(0x1000000), timestamp=datetime.utcnow())

    embed.set_image(url=achievement)
    await ctx.send(embed=embed)


  @commands.command(
      brief='gets a random comic from https://xkcd.com',
      description='gets a random comic from https://xkcd.com')
  async def xkcd(self, ctx):
    comic = xkcd.getRandomComic()
    url = comic.getImageLink()
    title = comic.getTitle()


    embed=discord.Embed(title=title, color = random.randrange(0x1000000), timestamp=datetime.utcnow())
    embed.set_image(url=url)
    await ctx.send(embed=embed)
