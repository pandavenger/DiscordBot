# Work with Python 3.7
import random
import asyncio

from discord import Game
from discord.ext.commands import Bot
from pbwrap import Pastebin

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

print("Pastebin Key: " + str(my_key))

@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Magic 8Ball",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def _8ball(ctx, arg):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(arg + '/n' + random.choice(possible_responses) + ", " + ctx.message.author.mention)


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
                aliases=['pastebin', 'spoiler'],
                pass_context=True)
async def _pastebin(ctx, arg):
    await client.delete_message(ctx.message)
    result = pbapi.create_paste(arg)
    await client.say('Pastebin: <' + str(result) + '>')

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="sez!"))
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