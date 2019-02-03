import os

#helper functions
def strip1(text: str, strip_text: str): #useless wtf
    """
    Returns a string with strip_text stripped from the beginning of text.
    """
    return text.lstrip(strip_text)

def strip2(text: str, strip_text: str):
    """
    Returns a string with everything up to and including the first occurence
    of strip_text and 1 additional character stripped from text. 
    If strip_text is not in text, return text[-1]
    """
    index = text.find(strip_text) + len(strip_text) + 1 # accounts for the space
    return text[index:]

def make_directory(dir):
    if not os.path.exists(dir) and dir != '':
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

def read_dict_from_file(file:str, d={}):
    """
    Reads a file where each line has 2 words separated 
    by a space, and appends these words to dict as key-value
    pairs. 
    Precondition: each key is present in the file only once.
    """
    contents = read_file(file)
    for line in contents:
        words = line.split()
        if len(words) > 1:
            d.update({words[0]:" ".join(words[1:])})
    return d

def write_dict_to_file(d:dict, fl:str):
    """
    Writes the key-value pairs in d as space-separated words
    in file. Each pair is on its own line.
    """
    file_obj = open(fl, "w+")
    for key, value in d.items():
        file_obj.write("{0} {1}\n".format(key, value))
    file_obj.close()
    
def get_property(user:str, prop:str):
    user_to_property = read_dict_from_file("user data/{0}".format(user), {})
    return user_to_property.get(prop)
    
def set_property(user:str, prop:str, val):
    user_to_property = read_dict_from_file("user data/{0}".format(user))
    user_to_property.update({prop: val})
    write_dict_to_file(user_to_property, "user data/{0}".format(user))

def get_generic_dict(d:dict, d_name, key):
    d = read_dict_from_file("generic/{0}".format(d_name), {})
    return d.get(key)

def set_generic_dict(d:dict, d_name, key, val):
    get_generic_dict(d, d_name, key)
    d.update({key: val})
    write_dict_to_file(d, "generic/{0}".format(d_name))

settings = {}
explicit_responses = {}

def parse_message(message):
    msg = message.content
    if msg.startswith(settings["command_str"]): 
        msg = msg[len(settings["command_str"]):] #strip the command string
        msg_list = msg.split()
        if len(msg_list) > 0: #check for empty command string
            #command list

            #no params, simple text
            if msg_list[0] == "isbot":
                return isbot(message)
            elif msg_list[0] == "ping":
                return ping(message)
            #no params, other
            elif msg_list[0] == "version":
                return version()
            elif msg_list[0] == "settings":
                return settings # (settings) <- no longer necessary
            #params: message only
            elif msg_list[0] == "hello":
                return hello(message)
            #params: command text only
            elif msg_list[0] == "commit":
                return commit(read_file("command text/commit.txt"))
            #params: command text and message
            elif msg_list[0] == "extrathicc":
                thicc_dict = read_dict_from_file("dictionary text/extra thicc.txt")
                return extrathicc(message, thicc_dict)
            elif msg_list[0] == "keeb":
	            return keeb(message, read_file("dictionary text/korean.txt"))
            #params: message and user data
            elif msg_list[0] == "callme":
                return set_name(message, [message.author], "callme")
            elif msg_list[0] == "myname":
                return get_name(message, [message.author])
            elif msg_list[0] == "call":
                return set_name(message, message.mentions, "call")
            elif msg_list[0] == "name":
                return get_name(message, message.mentions)
            elif msg_list[0] == "defexplicit":
                return define(message, explicit_responses)
            #admin-only
            elif msg_list[0] == "eval":
                if message.author == message.server.owner:
                    #evaluate the message only if the message author is the owner
                    return eval(strip2(message.content, "eval"))
                else:
                    return "Insufficient permissions. Must be server owner."
            elif msg_list[0] == "exec":
                if message.author == message.server.owner:
                    #evaluate the message only if the message author is the owner
                    exec(strip2(message.content, "exec"))
                    return #exec doesn't return anything, so we return to not send an empty message
                else:
                    return "Insufficient permissions. Must be server owner."
            else:
                return "invalid command"
    #check for explicit responses
    elif msg in explicit_responses:
        return explicit_responses[msg]




#no params, simple text
def isbot(message):
    return "yes"

def ping(message):
    return "pong!"

#no params, other
def version():
    """
    Returns the version of the program, but python doesn't really have 
    program versions, unlike C#, so it just returns a placeholder string.
    """
    return "uh python doesn't really do that"

# def get_settings(setting_to_val):
#     """
#     returns the value passed as an argument. Intended to be used to return the
#     dict containing the settings.
#     """
#     return setting_to_val

#params: message only
def hello(message):
    return 'Hello {0.author.mention}'.format(message)

#params: command text only
def commit(commit_list:list):
    import random
    return commit_list[random.randrange(len(commit_list))]
	
def keeb(message, korean_list: list):
	for letter in message.content:
		if letter in korean_list:
			return True
	return False

#params: message and command text
def extrathicc(message, thicc_dict:dict):
    out = ""
    msg = strip2(message.content.upper(), "extrathicc")
    for ch in msg: #dict contains uppercase letters
        out += thicc_dict.get(ch, "")
    return out
#params: message and user data

def set_name(message, user_list, trigger_string): #not to be confused with discord nickname
    if settings.get("annoyed_everyone", True) and message.mention_everyone:
        return settings.get("everyone_string", "no u")
    elif message.mention_everyone:
        for member in message.server.members:
            user_list.append(member)
        nickname = strip2(message.content, "@everyone")
    elif user_list == [message.author]: # prevents unnecessary stripping
        nickname = strip2(message.content, trigger_string)
    elif len(user_list) == 0:
        return "No valid user mentions."
    else:
        for user in user_list:
            nickname = strip2(message.content, str(user.mention))
    out = ""
    #not necessary, since there will be at least 1 mention following it
    #nickname = strip2(message.content, trigger_string) #command_text must be separate from the command by a space
    for user in user_list:
        set_property(user, "nickname", nickname)
        out += "{0}, I will call you {1}. ".format(user.mention, get_property(user, "nickname"))
    return out

def get_name(message, user_list):
    if settings.get("annoyed_everyone", True) and message.mention_everyone:
        return settings.get("everyone_string", "no u")
    elif message.mention_everyone:
        for member in message.server.members:
            user_list.append(member)
    elif len(user_list) == 0:
        return "No valid user mentions."
    out = "" 
    for user in user_list:
        user_nick = get_property(user, "nickname")
        if user_nick is None:
            out += "{0}, you have no name. ".format(user.mention)
        else:
            out += "{0}, your name is {1}. ".format(user.mention, user_nick)
    return out

def define(message, explicit_responses:dict):
    try:
        command = [message.content.split('"')[1], message.content.split('"')[3]]
    except:
        return "invalid response format"
    set_generic_dict(explicit_responses, "explicit_responses", command[0], command[1])
    return "will respond to \"{0}\" with \"{1}\". ".format(command[0], command[1])
