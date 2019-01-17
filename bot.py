# Work with Python 3.6
import discord
import commands
import os


def make_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def read_file(file:str) -> list:
    """
    Returns the contents of the file. If the file does not exist, creates the file
    and returns an empty list.
    #precondition: the directory exists
    """
    try:
        file_IO = open(file, "r")
        contents = file_IO.read().splitlines()
    except:
        dir = os.path.split(file)[0]
        make_directory(dir)
        file_IO = open(file, "x")
        contents = []
    finally:
        file_IO.close()
    return contents

def read_dict_from_file(file:str):
    """
    Reads a file where each line has 2 words separated 
    by a space, and appends these words to dict as key-value
    pairs. 
    Precondition: each key is present in the file only once.
    """
    d = {}
    contents = read_file(file)
    for line in contents:
        words = line.split()
        if len(words) > 1:
            d.update({words[0]:" ".join(words[1:])})
    return d

def write_dict_to_file(d:dict, file:str):
    """
    Writes the key-value pairs in d as space-separated words
    in file. Each pair is on its own line.
    """
    file_obj = open(file, "w+")
    for key, value in d.items():
        file_obj.write("{0} {1}\n".format(key, value))
    file_obj.close()

def parse_message(message):
    out = ""
    msg = message.content
    if msg.startswith(settings["command_str"]): 
        msg = msg[len(settings["command_str"]):] #strip the command string
        msg_list = msg.split()
        if len(msg_list) > 0: #check for empty command string
            skip_send = False
            #command list

            #no params, simple text
            if msg_list[0] == "isbot":
                out = commands.isbot(message)
            elif msg_list[0] == "ping":
                out = commands.ping(message)
            #no params, other
            elif msg_list[0] == "version":
                out = commands.version()
            elif msg_list[0] == "settings":
                out = commands.settings(settings) #redundant, but consistent
            #params: message only
            elif msg_list[0] == "hello":
                out = commands.hello(message)
            #params: command text only
            elif msg_list[0] == "commit":
                out = commands.commit(read_file("command text/commit.txt"))
            #params: command text and message
            elif msg_list[0] == "extrathicc":
                thicc_dict = read_dict_from_file("dictionary text/extra thicc.txt")
                out = commands.extrathicc(message, thicc_dict)
            elif msg_list[0] == "keeb":
	            out = commands.keeb(message, read_file("dictionary text/korean.txt"))
            #params: message and user data
            elif msg_list[0] == "callme":
                user_to_property = read_dict_from_file("user data/{0}".format(message.author))
                out = commands.callme(message, user_to_property)
                write_dict_to_file(user_to_property, "user data/{0}".format(message.author))
            elif msg_list[0] == "myname":
                user_to_property = read_dict_from_file("user data/{0}".format(message.author))
                out = commands.myname(message, user_to_property)
            #admin-only
            elif msg_list[0] == "eval":
                if message.author == message.server.owner:
                    #evaluate the message only if the message author is the owner
                    out = eval(commands.strip2(message.content, "eval"))
                else:
                    msg = "Insufficient permissions. Must be server owner."
            elif msg_list[0] == "exec":
                if message.author == message.server.owner:
                    #evaluate the message only if the message author is the owner
                    out = exec(commands.strip2(message.content, "exec"))
                    return #exec doesn't return anything, so we return to not send an empty message
                else:
                    msg = "Insufficient permissions. Must be server owner."
            else:
                out = "invalid command"
				
    return out

#initialize
#default settings
settings = {
        "command_str": "bb "
        }

TOKEN = read_file("token.txt")[0]
settings = read_dict_from_file("settings.txt")
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
        msg = parse_message(message)

    try:
        msg_len = getattr(msg,"__len__")
        if msg_len == 0:
            return
    except:
        pass
    finally:
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
