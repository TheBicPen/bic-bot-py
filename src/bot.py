# Work with Python 3.6
import discord
from . import message_parser as parser
from . import helpers
from . import consts
from sys import argv
#import log

def main():
    TOKEN = helpers.read_file("credentials/discord_token.txt")
    if len(TOKEN) > 0:
        TOKEN = TOKEN[0]
    else:
        helpers.log("Unable to read Discord token")

    settings = helpers.read_dict_from_file("settings.txt", consts.default_settings)
    # explicit_responses = helpers.read_dict_from_file(
    #     "global_dicts/explicit_responses")
    # pattern_responses = helpers.read_dict_from_file(
    #     "global_dicts/pattern_responses")
    explicit_responses = None
    pattern_responses = None
    modules = ["generic_module"]

    # parse arguments
    if "--tf" in argv:
        modules.append(consts.ML_lib)
    message_parser = parser.Parser(
        settings, modules, explicit_responses, pattern_responses)
    client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    elif message.content.startswith("!debug"):
        msg = 'Hello {0.author.mention}. The command string is {1}'.format(
            message, settings["command_str"])

    else:
        msg = await message_parser.parse_message(message)

    if not msg is None:
        try:
            if len(str(msg)) > 2000:
                helpers.log("message too long: " + str(len(str(msg))))
                await message.channel.send("message too long: " + str(len(str(msg))))
            elif len(str(msg)) > 0:
                await message.channel.send(msg)
        except:
            helpers.log("Failed to process message of type " + str(type(msg)))


@client.event
async def on_ready():
    helpers.log('Logged in as')
    helpers.log(client.user.name)
    helpers.log(client.user.id)
    helpers.log('------')
if type(TOKEN) == type(""):
    client.run(TOKEN)
else:
    helpers.log("Invalid token type: " + str(type(TOKEN)))


if __name__ == "__main__":
    main()