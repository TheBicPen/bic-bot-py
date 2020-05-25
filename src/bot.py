# Work with Python 3.6
import discord
import message_parser as parser
import helpers
import consts
from message_response import MessageResponse
from sys import argv
#import log

def main():
    TOKEN = helpers.read_file("credentials/discord_token.txt")
    if len(TOKEN) > 0:
        TOKEN = TOKEN[0]
    else:
        helpers.log("Unable to read Discord token")

    settings = helpers.read_dict_from_file("settings.txt", {})
    if not settings:
        print("Settings not found. Writing defaults to file.")
        settings = helpers.read_dict_from_file("settings.txt", consts.default_settings)
        helpers.write_dict_to_file(settings, "settings.txt")

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
        # we do not want the bot to read its own messages
        if message.author == client.user:
            return
        else:
            try:
                msg = await message_parser.parse_message(message)
                if msg and isinstance(msg, MessageResponse):
                    await message_parser.send_response(msg, message.channel)
                elif msg:
                    await message.channel.send(msg)
            except Exception as e:
                print(e)


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