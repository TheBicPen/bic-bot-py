# Work with Python 3.6
import discord
import commands
from helpers_generic import log, init_log
#import log


#initialize
#default settings

TOKEN = commands.read_file("credentials/discord_token.txt")[0]

default_settings = {
        "command_str": "bb ",
        "annoyed_everyone": True,
        "everyone_string": "no u"
        }
settings = commands.read_dict_from_file("settings.txt", default_settings)
commands.settings = settings
commands.explicit_responses = commands.read_dict_from_file("global_dicts/explicit_responses", commands.explicit_responses)
client = discord.Client()

#command_str = settings["command_str"]

#TOKEN = None
#settings = None
#client = None

#initialize()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith("!debug"):
        msg = 'Hello {0.author.mention}. The command string is {1}'.format(message, settings["command_str"])

    else:
        msg = commands.parse_message(message)

    # if not msg is None:
    #     try:
    #         msg_len = getattr(msg,"__len__")
    #         print(msg_len)
    #         if msg_len == 0:
    #             return

    #         if len(msg) == 0:
    #             print("msg: {0}\n".format(msg))
    #             msg = "Unable to send empty message."
    #         print("msg: {0}\n".format(msg))
    #         await client.send_message(message.channel, msg)
    #     except:
    #         print("some kind of attribute error in the message or something")
    # else:
    #     print("null message")
    if not msg is None:
        try:
            if len(str(msg)) > 2000:
                log("message too long: " + str(len(str(msg))))
                await client.send_message(message.channel, "message too long: " + str(len(str(msg))))
            elif len(str(msg)) > 0: 
                await client.send_message(message.channel, msg)
        except:
            log("Unable to convert message of type " + str(type(msg)))

@client.event
async def on_ready():
    log('Logged in as')
    log(client.user.name)
    log(client.user.id)
    log('------')
client.run(TOKEN)
