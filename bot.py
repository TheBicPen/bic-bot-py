# Work with Python 3.6
import discord

def read_file(file:str) -> list:
    """
    Returns the contents of the file. If the file does not exist, creates the file
    and returns an empty list.
    """
    try:
        file_IO = open(file, "r")
        contents = file_IO.read().splitlines()
        file_IO.close()
    except:
        file_IO = open(file, "w")
        file_IO.close()
        contents = []
    return contents

def parse_message(msg):
    if msg.startswith(command_str):
        msg = msg[len(command_str):]
    
    command_list = ["hello", "myname", "isbot", "ping", 
           " commit", "extrathicc","version", "callme"]

def initialize():
    default_settings = {
            command_str = "bb "
            }

    TOKEN = read_file("token.txt")[0]
    settings = read_file("settings.txt")
    client = discord.Client()

initialize()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith(command_str):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
