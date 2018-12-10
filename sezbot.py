# import random, asyncio is required for discord.py
import random
import asyncio

# imports the required pieces from discord.py
from discord import Game
from discord.ext.commands import Bot

# imports for calling the pastebin api
from pbwrap import Pastebin

# imports for calling the giphy api
from pygiphy.client import GiphyClient

# imports for weather updates
from weather import Weather, Unit

# Bot Setup
BOT_PREFIX = "sez!"
TOKEN = ""  # discordapp.com/developers/applications/me
client = Bot(command_prefix=BOT_PREFIX)

# Pastebin Setup
pb_dev_key = ""
pb_dev_user = ""
pb_dev_pass = ""
pbapi = Pastebin(pb_dev_key)
my_key = pbapi.authenticate(pb_dev_user, pb_dev_pass)

# Giphy Setup
giphy_dev_key = ""
giphyapi = GiphyClient(giphy_dev_key)

# Weather Setup
weather = Weather(unit=Unit.FAHRENHEIT)

# print("Pastebin Key: " + str(my_key))

@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Magic 8Ball",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def _8ball(ctx, arg):
    possible_responses = [
        'It is certain',
        'It is decidedly so',
        'Without a doubt',
        'Yes - definitely',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook good',
        'Yes',
        'Signs point to yes',
        'Reply hazy, try again',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        'Don\'t count on it',
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful'
    ]
    await client.say(arg + '\n' + random.choice(possible_responses) + ", " + ctx.message.author.mention)


@client.command(name='roll',
                description="Rolls a dice with the number of sides given.",
                brief="Dice roll",
                aliases=['d', 'dice'],
                pass_context=True)
async def _roll(ctx, arg):
    result = random.randint(1, int(arg))
    await client.say('Rolling a d' + str(arg) + ': ' + str(result))


@client.command(name='pb',
                description="Posts given text to pastebin",
                brief="Pastebin",
                aliases=['pastebin', 'spoiler', 'spoilers'],
                pass_context=True)
async def _pastebin(ctx, arg):
    await client.delete_message(ctx.message)
    result = pbapi.create_paste(arg)
    await client.say('Pastebin: <' + str(result) + '>')


@client.command(name='gif',
                description="",
                brief="GIPHY Lookup",
                aliases=['giphy'],
                pass_context=True)
async def _giphy(ctx, arg):
    results = giphyapi.search.gifs(arg, only_urls=True)
    if len(results) > 0:
        await client.say(str(results[random.randint(0, len(results))]))
    else:
        await client.say("No results found for " + str(arg))

@client.command(name='weather',
                description="",
                brief="Weather lookup",
                aliases=['w'],
                pass_context=True)
async def _weather(ctx, arg):
    results = weather.lookup_by_location(arg)
    if results != None:
        await client.say("The weather for " + str(results.location.city) + "," + str(results.location.region) + " is " +
                     str(results.condition.temp) + "F (" + str(results.condition.text) + ") [" +
                     str(results.condition.date) + "]")
    else:
        await client.say("Could not find location " + str(arg))

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Command: sez!"))
    print("Logged in as " + client.user.name)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)