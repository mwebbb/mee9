import os
import asyncio
import os.path
import random
import shutil  # to save it locally
import string
import subprocess
import time
import urllib.request
from datetime import datetime
from time import sleep as s
import base64
import aiohttp
import discord
import mystbin
import pymongo
import requests

import statcord
from discord.ext import commands
from discord.ext.commands.cooldowns import MaxConcurrency
from discord_slash import SlashCommand, SlashContext
from discord_webhook import DiscordEmbed, DiscordWebhook
from pymongo import MongoClient
from termcolor import colored
from replit import db

from cogs.fun import Fun
from cogs.mee9 import mee9
from cogs.moderation import moderation
from cogs.owner_only import owner_only
from cogs.utility import Utility
from jokes import allJokes
from words import words
import jishaku


mystbin_client = mystbin.Client()

from pymongo import MongoClient
client = MongoClient()



webhook = DiscordWebhook(
    url='WEBHOOK_URL')


# from simplegist import SimpleGist


intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='~',
                   case_insensitive=True,
                   owner_id=633307008879296512,
                   intents=intents)


slash = SlashCommand(
    bot, sync_commands=True)  # Declares slash commands through the client.

description = '''MEE9 is a cool discord bot for cool poggers gamers B)'''

searchURL = 'https://api.gosnipe.tech/api/status/name/'


class helpcommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            color = random.randrange(0x1000000)

            embed = discord.Embed(
                description=page, timestamp=datetime.utcnow(), color=color)
            await destination.send(embed=embed)

bot.load_extension('jishaku')

key = "STATCORD-KEY"
api = statcord.Client(bot, key)
api.start_loop()

bot.add_cog(Utility(bot))
bot.add_cog(Fun(bot))
bot.add_cog(owner_only(bot))
bot.add_cog(moderation(bot))
bot.add_cog(mee9(bot))


# nav = Navigation("◀", "▶", "🗑")

bot.help_command = helpcommand()
# bot.help_command = PrettyHelp(navigation=nav, color=discord.Color.blurple(), active_time=30, no_category="Commands", show_index=True)

extensions = [
    'cogs.utility',
    'cogs.fun',
    'cogs.owner_only',
]

# @bot.command(
#     brief='coming soon',
#     description='coming soon')
# async def premium(ctx):
#   embed=discord.Embed(title="MEE9 Premium", description="Price: `$5`\nFeatures: `Coming Soon`")
#   embed.set_author(name="Made by cgd", icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif", url="https://cgd.pw")
#   await ctx.reply(embed=embed)

# @bot.event
# async def on_command_error(error)

@bot.command(aliases=["namemc", "nameinfo"])
async def search(ctx, username):
    srch = searchURL + username
    r = requests.get(srch)
    result = r.json()
    namemc = result["namemc"]
    searches = str(namemc["searches"])
    if result["status"] == "taken":
        views = str(namemc["views"])
        linked = namemc["linked"]
        uid = result["id"]
        # mojangData = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uid}").json()
        # properties = mojangData["properties"]
        # encoded = properties["value"]
        # decoded = base64.b64decode(encoded).json()
        # skin = decoded["SKIN"]
        # skinurl = skin["url"]
        skinLink = 'https://visage.surgeplay.com/full/720/' + uid

        embed = discord.Embed(title=f"{username} - TAKEN", description=f"Searches: `{searches}`\nProfile views: `{views}`\nUUID: `{uid}`\n", url=f"https://namemc.com/{username}", color=0x2f3136)
        embed.set_image(url=skinLink)
        
        await ctx.send(embed=embed)
    elif result["status"] == "soon":

        availableWhen = result["time"]
        # mojangData = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uid}").json()
        # properties = mojangData["properties"]
        # encoded = properties["value"]
        # decoded = base64.b64decode(encoded).json()
        # skin = decoded["SKIN"]
        # skinurl = skin["url"]

        embed = discord.Embed(title=f"{username} - TAKEN", description=f"Searches: `{searches}`\nAvailable at: {availableWhen}", url=f"https://namemc.com/{username}", color=0x2f3136)
        
        await ctx.send(embed=embed)

    else:
        await ctx.send("name is available")


@bot.command(
    brief='shows information about any minecraft server',
    description='uses an api to see information about any minecraft server. usage: .srvinfo [IP]'
)
async def mcsrv(ctx, *, arg):
    response = "retrieving data  from " + arg + ". this may take up to 10 seconds!"
    await ctx.reply(response, mention_author=False)
    async with aiohttp.ClientSession() as session:
        async with session.get(
                'https://mcstatus.snowdev.com.br/api/query/v2/' + arg) as r:
            if r.status == 200:
                js = await r.json()
                if str(js["Online"]) == 'true':
                    await response.edit("server is online 🥱🥱🙄")
                else:
                    await response.edit("server is offline :pensive:")



# @bot.command(
#     brief='submit code to github',
#     description='submit code to github')
# async def ghgist(ctx, *, code):


#   letters = string.ascii_letters

#   filename = ''.join(random.choice(letters) for i in range(16))

#   ghGist = SimpleGist(username='mee9bot', api_token='GITHUB_API_TOKEN')

#   ghGist.create(name=filename, description='uploaded using mee9 discord bot https://mee9.dev', public=1, content=code)


@bot.command(brief='gives a role to the typed user',
             description='usage: `.giverole [user] [role]`',
             pass_context=True)
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    embed = discord.Embed(
        title="Success!",
        description=f"{user.name} has been given the {role.name} role",
        color=random.randrange(0x1000000))
    embed.set_author(
        name="Made by cgd",
        icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif",
        url="https://cgd.pw")
    await ctx.reply(embed=embed, mention_author=False)


@bot.command(
    brief='guess a number for, well.. nothing I guess.',
    description='guess a number')
async def guess(ctx):

    channel = ctx.channel

    number = random.randrange(1, 20)
    num = str(number)
    startEmbed = discord.Embed(title="Guess the random number!", description="I'm thinking of a number between 1 and 20. Try to guess what it is, and you'll get, well.. nothing.",
                               color=random.randrange(0x1000000), timestamp=datetime.utcnow())
    # statusEmbed = discord.Embed(title="Number game", description=f"You currently have {}", color=random.randrange(0x1000000), timestamp=datetime.utcnow())
    await channel.send(embed=startEmbed)

    firstInput = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    correctMSG = discord.Embed(
        title="Correct!", description="That was the number! Nice job, you won nothing!", color=0x00FF00, timestamp=datetime.utcnow())

    failedEmbed = discord.Embed(
        title="You lost.", description=f"You lost, the number was {num}.", timestamp=datetime.utcnow())

    if firstInput.content == num:

        await ctx.send(embed=correctMSG)

    else:
        embed = discord.Embed(title="Incorrect", description="That wasn't the correct answer.\nGuesses left: `3`",
                              color=random.randrange(0x1000000), timestamp=datetime.utcnow())
        await ctx.send(embed=embed)

        secondInput = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

        if secondInput.content == num:

            await ctx.send(embed=correctMSG)

        else:

            embed = discord.Embed(title="Incorrect", description="That wasn't the correct answer either.\nGuesses left: `2`",
                                  color=random.randrange(0x1000000), timestamp=datetime.utcnow())
            await ctx.send(embed=embed)

            # taking the third input
            thirdInput = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

            # starting to check what it was

            if thirdInput.content == num:
                await ctx.send(embed=correctMSG)

            else:
                embed = discord.Embed(title="Incorrect", description="That wasn't the correct answer either.\nGuesses left: `1`",
                                  color=random.randrange(0x1000000), timestamp=datetime.utcnow())
                await ctx.send(embed=embed)
                lastInput = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

                if lastInput.content == num:

                    await ctx.send(embed=correctMSG)

                else:
                    embed = discord.Embed(title="Incorrect", description="That wasn't the correct answer either.\nGuesses left: `0`", color=random.randrange(
                        0x1000000), timestamp=datetime.utcnow())

                    await ctx.send(embed=failedEmbed)


@bot.command(brief='Vote for MEE9', description='Vote for MEE9')
async def vote(ctx):
    embed = discord.Embed(
        title="Vote for MEE9!",
        url="https://vote.mee9.dev",
        description="Click [here](https://vote.mee9.dev) to vote for MEE9!",
        timestamp=datetime.utcnow(),
        color=random.randrange(0x1000000))
    embed.set_thumbnail(url="https://mee9.dev/images/logo.png")
    embed.set_author(
        name="Made by cgd",
        icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif",
        url="https://cgd.pw")
    await ctx.reply(embed=embed)


@bot.event
async def on_reaction_add(reaction, member):
    channel = discord.utils.get(reaction.message.guild.channels, name="starboard")
    

    
    if (reaction.emoji == '⭐') and (reaction.count >= 3):
        embed = discord.Embed(color = 0xffcf00, title="Starboard", description=f"[Jump to message]({reaction.message.jump_url})")
        embed.set_author(name = reaction.message.author.name, icon_url = reaction.message.author.avatar_url)
        embed.add_field(name = "Message:", value = reaction.message.content)
        
        if len(reaction.message.attachments) > 0:
            embed.set_image(url = reaction.message.attachments[0].url)
        
        embed.set_footer(text = f" ⭐ {reaction.count} | #{reaction.message.channel.name}")
        embed.timestamp = datetime.utcnow()
        await channel.send(embed = embed)
        

# snipe_message_content = None
# snipe_message_author = None
# snipe_message_id = None

# @bot.command(
#     brief='',
#     description='')
# async def command(ctx):
#   embed=discord.Embed(title="Booster perks!", description="Here you will find all the available perks for boosting the server!", color=0xff00d4)
#   embed.add_field(name="Exclusive Roles", value="You get a role with the color and name of your choice, plus the exclusive <@&736717191113605251> role!", inline=False)
#   embed.add_field(name="Use external emotes", value="You get access to emotes from other servers!", inline=False)
#   embed.add_field(name="Secret channel", value="You get access to the #︱booster-chat channel!", inline=False)
#   embed.add_field(name="More coming soon", value="If you have any more ideas for booster perks, DM <@633307008879296512> or send your ideas in <#776134222154170378>!", inline=False)
#   embed.set_footer(text="imagine not boosting :flushed:")
#   await ctx.reply(embed=embed)

# @bot.event
# async def on_message_delete(message):

#     global snipe_message_content
#     global snipe_message_author
#     global snipe_message_id

#     snipe_message_content = message.content
#     snipe_message_author = message.author.id
#     snipe_message_id = message.id
#     await asyncio.sleep(60)

#     if message.id == snipe_message_id:
#         snipe_message_author = None
#         snipe_message_content = None
#         snipe_message_id = None

# @bot.command(
#     brief='link to the new dashboard!',
#     description='')
# async def dashboard(ctx):
#    await ctx.reply(
#         'https://2no.co/2khyJ5'
#     )

# @bot.command()
# async def snipe(message):
#     if snipe_message_content == None:
#         await message.channel.send("Theres nothing to snipe.")
#     else:
#         embed = discord.Embed(description=f"{snipe_message_content}")
#         embed.set_footer(
#             text=
#             f"Sniped by {message.author.name}#{message.author.discriminator}",
#             icon_url=message.author.avatar_url)
#         embed.set_author(name=f"<@{snipe_message_author}>")
#         await message.channel.send(embed=embed)
#         return

@bot.command()
async def reminder(ctx, seconds: int, *, reason):
    await ctx.send(f"Ok, set a timer for {str(seconds)} seconds!")
    await asyncio.sleep(seconds)

    for i in range(3):
        await ctx.reply(f"TIMERS UP (REASON: {reason})")


@bot.command(
    brief='sends your avatar in chat',
    description='This command sends the mentioned users avatar in chat.')
async def avatar(
        ctx,
        *,
        member: discord.Member = None):  # set the member object to None
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    userAvatar = member.avatar_url
    embed = discord.Embed(title="Here is the avatar of that user!",
                          color=random.randrange(0x1000000),
                          timestamp=datetime.utcnow())
    embed.set_image(url=userAvatar)
    embed.set_author(
        name="Made by cgd",
        icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif"
    )
    await ctx.reply(embed=embed)


@bot.command(brief='invite me to your server',
             description='this command lets you send invite me to your server')
async def invite(ctx):
    author = ctx.message.author
    authorProfile = author.avatar_url
    embed = discord.Embed(
        title="Invite me to your server!",
        url="https://discord.com/api/oauth2/authorize?client_id=782009166150500382&permissions=8&scope=bot",
        description="I dont know why but if you do for some reason want to add me, i wont stop you.",
        timestamp=datetime.utcnow(),
        color=random.randrange(0x1000000))
    embed.set_author(name=author, icon_url=authorProfile)
    embed.set_footer(text="made by yeetmeister")
    await ctx.reply(embed=embed)


@bot.command(brief='sends annoying message',
             description='annoyifies your message with spoilers',
             pass_context=True)
async def spoiler(ctx, *, arg):
    if len(arg) > 45:
        embed = discord.Embed(
            title="Error:",
            description="Your message has too many letters!  the max is 45!",
            color=random.randrange(0x1000000))
        embed.set_footer(text="made by yeetmeister")
        await ctx.reply(embed=embed)
        await ctx.message.delete()
    else:
        await ctx.reply("".join([f"||{i}||" for i in arg]))
        await ctx.message.delete()


@bot.event
async def on_command(ctx):
    api.command_run(ctx)


@bot.command(brief='sends random dad joke',
             description='dad jokes are the best jokes')
async def dadjoke(ctx):
    author = ctx.message.author
    authorProfile = author.avatar_url
    joke = random.choice(allJokes)
    embed = discord.Embed(title="Your dad joke:",
                          description=joke,
                          color=random.randrange(0x1000000),
                          timestamp=datetime.utcnow())
    await ctx.reply(embed=embed)


# @bot.command(
#     brief='dont do it', description='i said dont do this commanmd plsplspls')
# async def shampoe(ctx):
#     embed = discord.Embed(
#         title="HEY SUB TO SHAMPOE OR BAD",
#         url=
#         "https://www.youtube.com/channel/UCzYv6dYxU7Xw_tiF91Mmm8g?sub_confirmation=1",
#         color=0xffa200)
#     embed.set_thumbnail(url="https://i.imgur.com/1qIH6Gx.png")
#     embed.add_field(
#         name=
#         "subnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnow",
#         value="you dont even know how long it took me to get that image",
#         inline=True)
#     embed.add_field(
#         name=
#         "subnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnow",
#         value=
#         "subnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnow",
#         inline=True)
#     embed.add_field(
#         name=
#         "subnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnow",
#         value=
#         "subnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnow",
#         inline=True)
#     embed.add_field(
#         name=
#         "subnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnow",
#         value=
#         "subnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnowsubnow",
#         inline=True)
#     embed.set_footer(text="made by cgd")
#     await ctx.reply(embed=embed)


@bot.command(
    brief='randomly generates a meme',
    description='randomly generates a meme using memegen.link and a little randomness!')
async def meme(ctx):
    lineOne = random.choice(words) + '_' + random.choice(words)
    lineTwo = random.choice(words) + '_' + random.choice(
        words) + '_' + random.choice(words)
    memeType = random.choice([
        'both', 'doge', 'ds', 'buzz', 'fry', 'blb', 'chosen', 'elf', 'icanhas',
        'keanu', 'interesting', 'wonka', 'philosoraptor'
    ])
    if memeType == 'both':
        lineOne = random.choice(words) + '_' + 'or' + '_' + random.choice(
            words)
        lineTwo = 'why_not_both~q'
        meme = 'https://api.memegen.link/images/' + \
            memeType + '/' + lineOne + '/' + lineTwo + '.png'
    else:
        meme = 'https://api.memegen.link/images/' + \
            memeType + '/' + lineOne + '/' + lineTwo + '.png'

    await ctx.reply(meme)


@bot.command(brief='cool meme', description='very cool meme')
async def faxpuffy(ctx):
    await ctx.reply(
        'https://api.memegen.link/images/buzz/fax_puffy/enthusiastic_string_rod.png'
    )


# @slash.slash(name="ping")
# async def _ping(ctx): # Defines a new "context" (ctx) command called "ping."
#     await ctx.respond()
#     await ctx.reply(f"Pong! ({bot.latency*1000}ms)", hidden=True)


@slash.slash(name="command")
async def _command(
        ctx):  # Defines a new "context" (ctx) command called "ping."
    await ctx.respond()
    await ctx.send("e", hidden=True)


@slash.slash(name="invite")
async def _invite(ctx):  # Defines a new "context" (ctx) command called "ping."
    await ctx.respond()
    await ctx.reply(
        "Invite MEE9 here! https://discord.com/oauth2/authorize?client_id=782009166150500382&permissions=8&scope=bot%20applications.commands",
        hidden=True)


@bot.command()
async def react(ctx, id, text):

    loading = await ctx.send(f"Trying to find message with id `{id}`...")

    message = await ctx.channel.fetch_message(int(id))

    await asyncio.sleep(1)

    step1 = text.lower()

    step2 = "".join([f"\:regional_indicator_{letter}:" for letter in step1])

    finalized = step2.replace(':regional_indicator_ :', ' ')

    for reaction in finalized:
        await message.add_reaction(reaction)

    await loading.edit("Done!")


# @bot.command(name="github-stats", aliases=["gh-stats", "ghstats", "githubstats"])
# async def github_stats(ctx, username):
#     embed = discord.Embed(title=f"{username}'s GitHub Stats", color=random.randrange(0x100000), timestamp=datetime.utcnow())
#     embed.set_image(url="https://github-readme-stats.vercel.app/api?username=Mubbington&show_icons=true")
#     await ctx.send(embed=embed)

@bot.command(name="gsetup", aliases=["gstart", "gcreate"])
async def gsetup(ctx):
    await ctx.send("welcome to the interactive giveaway setup! ")
    await ctx.send("i didn't do this yet :flushed:")
@bot.command()
async def clyde(ctx, *, message):
    async with ctx.typing():
        curl = "https://nekobot.xyz/api/imagegen?type=clyde&text=" + message

        cletters = string.ascii_letters

        cfilename = ''.join(random.choice(cletters) for i in range(6))


        response = requests.get(curl).json()



        # setting filename and image URL
        image_url = response['message']

        embed = discord.Embed(title="clyde", description="", color=random.randrange(0x100000), timestamp=datetime.utcnow())
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)




        # wget.download(cmmjson['message'], out=output)




@slash.slash(name="support")
async def _support(
        ctx):  # Defines a new "context" (ctx) command called "ping."
    await ctx.respond()
    await ctx.send(
        "Need help? Join the support server here! discord.gg/dSdzGHW9",
        hidden=True)


@bot.command(
    brief='exactly what you think',
    description='make sure to use quotes around the message or it doesnt work!'
)
async def say(ctx, *, arg):
    await ctx.reply(arg)
    await ctx.message.delete()


@bot.command(brief='get the head of any player',
             description='gets the minecraft head of any player using an API')
async def mchead(ctx, *, arg):
    headLink = 'https://cravatar.eu/helmhead/' + arg + '/528.png'
    embed = discord.Embed(title="Here is the Minecraft head of that player!",
                          color=random.randrange(0x1000000))
    embed.set_image(url=headLink)
    embed.set_author(
        name="Made by cgd",
        icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif"
    )
    await ctx.reply(embed=embed)


@bot.command(brief='get the skin of any player',
             description='gets the minecraft skin of any player using an API')
async def mcskin(ctx, *, arg):
    skinLink = 'https://minecraftskinstealer.com/api/v1/skin/render/fullbody/' + arg + '/700'
    embed = discord.Embed(title="Here is the Minecraft skin of that player!",
                          color=random.randrange(0x1000000))
    embed.set_image(url=skinLink)
    embed.set_author(
        name="Made by cgd",
        icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif"
    )
    await ctx.reply(embed=embed)

def get_spaces(ctx, cmd, prefix):
    if (p := cmd.parent) is None:
        syntax = f"{prefix}{cmd.name} {cmd.signature}"
    else:
        syntax = f"{prefix}{p.name} {cmd.name} {cmd.signature}"

    syntax = syntax.split("<")

    chars = len(syntax[0])
    return " " * chars
    
def full_syntax(ctx, cmd, prefix):
    if (p := cmd.parent) is None:
        return f"{prefix}{cmd.name} {cmd.signature}"
    else:
        return f"{prefix}{p.name} {cmd.name} {cmd.signature}"

@bot.command()
async def servericon(ctx, *, arg):
    serverIcon = 'https://mcstatus.snowdev.com.br/api/favicon/' + arg + '/favicon.png'
    embed = discord.Embed(title="Here is the Minecraft icon of that server!",
                          color=random.randrange(0x1000000))
    embed.set_image(url=serverIcon)
    embed.set_author(
        name="Made by cgd",
        icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif"
    )
    await ctx.reply(embed=embed)

@bot.event
async def on_command_missing_argument(ctx, prefix, perms, param):
    spaces = get_spaces(ctx, ctx.command, prefix)
    carets = f"^" * (len(str(param).replace(' is a required argument that is missing.', ' ')) + 1)

    missing = f"\`\`\`\n{full_syntax(ctx, ctx.command, prefix)}\n{spaces}{carets}\n\`\`\`"
    embed = discord.Embed(title="Required Argument Missing", description=f"You are missing the **{str(param).replace(' is a required argument that is missing.', ' ')}** Argument\n{missing}")

    await ctx.send(perms, embed=embed)


@bot.event
async def on_command_error(ctx, error):
    
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You dont have permission to do that!",
            color=0xff0000)
        embed.set_author(
            name="Made by cgd",
            icon_url="https://images-ext-2.discordapp.net/external/CuZ0gNZukzcx1g5oFiycwbP0v_oZQxXVi_pgHhnjUd0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/633307008879296512/a_74af15e9e78edb963537d89b3c6545f1.gif",
            url="https://cgd.pw")
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title="Error:",
                              description=f"```{error}```",
                              color=random.randrange(0x1000000))
        embed.set_author(name="Made by cgd", url="https://cgd.pw")
        embed.set_footer(
            text="Error information sent via webhook. This issue will be fixed soon!")
# --------------------------------------------------------------------------------
        debugInfo = f"Error: {error}\nUsername: {ctx.author}\nServer name: {ctx.guild.name}\nChannel id: {ctx.channel.id}"
        webhookembed = DiscordEmbed(
            title='An error occured!', description=debugInfo, color=random.randrange(0x1000000))
        webhookembed.set_timestamp()
        webhook.add_embed(webhookembed)
        response = webhook.execute()
        await ctx.reply(embed=embed, mention_author=False)






@bot.command(description="mutes somebody.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole,
                                          speak=False,
                                          send_messages=False,
                                          read_message_history=True,
                                          read_messages=False)
    embed = discord.Embed(title="muted",
                          description=f"{member.mention} was muted ",
                          colour=discord.Colour.light_gray(),
                          timestamp=datetime.utcnow())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.reply(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f"you have been muted in: {guild.name} reason: {reason}")


@bot.command(description="unmutes somebody")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await member.send(f" you have unmutedd from: - {ctx.guild.name}")
    embed = discord.Embed(title="unmute",
                          description=f" unmuted-{member.mention}",
                          colour=discord.Colour.light_gray(),
                          timestamp=datetime.utcnow())
    await ctx.reply(embed=embed, mention_author=False)

@bot.command()
async def changemymind(ctx, *, message):
    async with ctx.typing():

        cmmurl = "https://nekobot.xyz/api/imagegen?type=changemymind&text=" + message
        
        letters = string.ascii_letters

        cmmjson = requests.get(cmmurl).json()

        # setting filename and image URL
        image_url = cmmjson['message']


        embed = discord.Embed(title="i wonder whats in the cup 🤔", description="", color=random.randrange(0x100000), timestamp=datetime.utcnow())
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)

        # wget.download(cmmjson['message'], out=output)

        print('downloaded file')

        

@bot.event
async def on_ready():
    print("me when")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="~help"))


@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member: discord.Member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.reply(f'Unbanned {user.mention}', mention_author=False)
            return


@bot.command(
    brief='get the skin source for any player',
    description='this commands pulls from an API to get the skin source a minecraft player. if the player does not exist, it will show up as steve.'
)
async def skinsrc(ctx, *, arg):
    imageLink = 'https://minotar.net/skin/' + arg
    await ctx.reply(imageLink, mention_author=False)


@bot.command()
async def paste(ctx, language, *, content):
    paste = await mystbin_client.post(content, syntax=language)
    link = str(paste)
    embed = discord.Embed(title="Success!", description=f'Uploaded to [Mystb.in]({link} "Powered by Mystb.in")', color=random.randrange(
        0x1000000), timestamp=datetime.utcnow())
    embed.set_footer(text="Uploaded")
    await ctx.reply(embed=embed, mention_author=False)


@bot.command()
async def trumptweet(ctx, *, message):
    async with ctx.typing():
        baseurl = "https://nekobot.xyz/api/imagegen?type=trumptweet&text=" + message
        
        letters = string.ascii_letters

        filename = ''.join(random.choice(letters) for i in range(6))
        output = '/cdn/' + filename + '.png'


        response = requests.get(baseurl).json()


        print('downloading file...')

        # setting filename and image URL
        image_url = response['message']

        r = requests.get(image_url, stream=True, headers={'User-agent': 'Mozilla/5.0'})


        embed = discord.Embed(title="twitter moment", description="", color=random.randrange(0x100000), timestamp=datetime.utcnow())
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
        

@bot.command()
async def deepfry(ctx, *, imageurl):
    async with ctx.typing():
        dfbaseurl = "https://nekobot.xyz/api/imagegen?type=deepfry&image=" + imageurl
        
        fileletters = string.ascii_letters

        dffilename = ''.join(random.choice(fileletters) for i in range(6))
        dfoutput = '/cdn/' + dffilename + '.png'


        response = requests.get(dfbaseurl).json()



        # setting filename and image URL
        imageurl = response['message']

        embed = discord.Embed(title="successfully baked image", description="", color=random.randrange(0x100000), timestamp=datetime.utcnow())
        embed.set_image(url=imageurl)
        await ctx.send(embed=embed)




@bot.command()
async def googoobaby(ctx):
    await ctx.send(":middle_finger::baby::middle_finger:")


@bot.command(aliases=["eco-start", "start-eco"])
async def ecostart(ctx):
    embed = discord.Embed(title="Successfully created your economy profile!", description="Earn money by doing `~beg` every now and then.", color=random.randrange(0x100000), timestamp=datetime.utcnow())
    await ctx.send("gaming")

from datetime import datetime

@bot.command()
async def status(ctx, status):
  if ctx.message.author.id == 633307008879296512:
    channel = await bot.fetch_channel(815701876640186418)
    embed=discord.Embed(title="Bot status", description=f"The bot status has been changed to **{status}**.", color=0x2f3136, timestamp=datetime.utcnow())
    message = await channel.send(embed=embed)
    await message.publish()
  else:
    await ctx.send("no perms :flushed:")


token = "TOKEN"

bot.run(token)  # Starts the bot
