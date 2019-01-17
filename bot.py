# Work with Python 3.6
import discord
import commands


#initialize
#default settings


TOKEN = commands.read_file("token.txt")[0]

default_settings = {
        "command_str": "bb ",
        "annoyed_everyone": True,
        "everyone_string": "no u"
        }
settings = commands.read_dict_from_file("settings.txt", default_settings)
commands.settings = settings
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

    if not msg is None:
        try:
            msg_len = getattr(msg,"__len__")
            if msg_len == 0:
                return
        except:
            pass
        finally:
            print("msg: {0}\n".format(msg))
            await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
