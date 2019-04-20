from helpers_generic import * #forgive me
import os
from image_classification import image_classify as ic
import urllib.request
import aiohttp
import asyncio


    
def get_user_property(server:str, user:str, prop:str):
    user_to_property = read_dict_from_file("servers/{1}/user data/{0}".format(user, server), {})
    return user_to_property.get(prop)
    
def set_user_property(server:str, user:str, prop:str, val):
    user_to_property = read_dict_from_file("servers/{1}/user data/{0}".format(user, server))
    user_to_property.update({prop: val})
    write_dict_to_file(user_to_property, "servers/{1}/user data/{0}".format(user, server))

def delete_user(server:str, user_mentions:str):
    out = ""
    for user in user_mentions:
        try:
            os.remove("servers/{1}/user data/{0}".format(user, server))
            out += "Deleted {0}'s info.\n".format(user)
        except:
            out += "Failed to delete.\n"
    return out
    
def get_generic_dict(d:dict, d_name, key):
    d = read_dict_from_file("global_dicts/{0}".format(d_name), {})
    return d.get(key)

def set_generic_dict(d:dict, d_name, key, val):
    get_generic_dict(d, d_name, key)
    d.update({key: val})
    write_dict_to_file(d, "global_dicts/{0}".format(d_name))

settings = {}
explicit_responses = {}
pattern_responses = {}
tf_sess = None
classifications = None

async def parse_message(message):
    msg = message.content
    if msg.startswith(settings["command_str"]): 
        msg = msg[len(settings["command_str"]):] #strip the command string
        msg_list = msg.split()
        if len(msg_list) > 0: #check for empty command string
            #command list

            if msg_list[0] == "isbot":
                return isbot(message)
            elif msg_list[0] == "ping":
                return ping(message)
            elif msg_list[0] == "version":
                return version()
            elif msg_list[0] == "settings":
                return settings # (settings) <- no longer necessary
            elif msg_list[0] == "hello":
                return hello(message)
            elif msg_list[0] == "commit":
                return list_response(read_file("global_lists/commit.txt"))
            elif msg_list[0] == "nut":
                return list_response(read_file("global_lists/nut.txt"))
            elif msg_list[0] == "extrathicc":
                thicc_dict = read_dict_from_file("global_dicts/extrathicc.txt")
                return translate(message, "extrathicc", thicc_dict)
            elif msg_list[0] == "leet":
                leet_dict = read_dict_from_file("global_dicts/leet.txt")
                return translate(message, "leet", leet_dict)
            elif msg_list[0] == "keeb":
	            return keeb(message, read_file("global_dicts/korean.txt"))
            elif msg_list[0] == "callme":
                return set_name(message, [message.author], "callme")
            elif msg_list[0] == "myname":
                return get_name(message, [message.author])
            elif msg_list[0] == "call":
                return set_name(message, message.mentions, "call")
            elif msg_list[0] == "name":
                return get_name(message, message.mentions)
            elif msg_list[0] == "deleteuser":
                return delete_user(message.server, message.mentions)
            elif msg_list[0] == "defexplicit":
                return define(message, explicit_responses, "explicit_responses")
            elif msg_list[0] == "defpattern":
                return define(message, pattern_responses, "pattern_responses")
            elif msg_list[0] == "imagecat":
                return await image_category(message, tf_sess, classifications)
            elif msg_list[0] == "tfstop":
                return stop_tf()
            #admin-only
            elif msg_list[0] == "tfstart":
                if message.author == message.server.owner:
                    return start_tf()
                else:
                    return "Insufficient permissions. Must be server owner."

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
    #classify image if applicable
    elif tf_sess is not None and len(message.attachments) > 0:
        return await image_category(message, tf_sess, classifications)
    else:
        return check_pattern(msg, pattern_responses)



    

        




#no params, simple text
def isbot(message):
    return "yes"

def ping(message):
    return "pong!"

#no params, other
def version():
    """
    Returns the version of the program, but I'm oo lazy to implement this.
    """
    return "uh I don't really do that at this point"

# def get_settings(setting_to_val):
#     """
#     returns the value passed as an argument. Intended to be used to return the
#     dict containing the settings.
#     """
#     return setting_to_val

#params: message only
def hello(message):
    return 'Hello {0.author.mention}'.format(message)

def start_tf():
    global tf_sess
    global classifications
    classifications = ic.get_classifications()
    if tf_sess is not None:
        print("tensorFlow session already exists")
        return tf_sess
    tf_sess = ic.main()
    return tf_sess

def stop_tf():
    global tf_sess
    global classifications
    tf_sess.close()
    classifications = None
    return "ended TensorFlow session"

async def image_category(message, tf_sess, classifications):
    if classifications is None:
        return "image classifications not found"
    if tf_sess is None:
        return "TensorFlow session not found"
    if len(message.attachments) == 0:
        return "no valid images in message"

    #check image using image-classification
    url = message.attachments[0]['url']
    print("message contains image at:{0}".format(url))
    #img = urllib.request.urlretrieve(url)
    async with aiohttp.get(url) as response:
        print(response)
        if response.status != 200:
            return "unable to retrieve image"
        img = await response.read()
        print(type(img))
        result = ic.classify_image(img, tf_sess, classifications)
    return "image is a {0}. {1:.2f} % confident".format(result[0], result[1])

#params: global_lists only
def list_response(l:list):
    import random
    return l[random.randrange(len(l))]

def keeb(message, korean_list: list):
	for letter in message.content:
		if letter in korean_list:
			return True
	return False

#params: message and global_lists
def translate(message:str, key:str, trans_dict:dict, convert_text=1):
    if trans_dict == {}:
        read_dict_from_file("global_dicts/{0}.txt".format(key), trans_dict)
    out = ""
    msg = strip2(strip2(message.content, settings["command_str"]), key)
    msg = convert_string(msg, convert_text)
    for ch in msg: #dict contains uppercase letters
        out += trans_dict.get(ch, ch)
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
        set_user_property(message.server, user, "nickname", nickname)
        out += "{0}, I will call you {1}. ".format(user.mention, get_user_property(message.server, user, "nickname"))
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
        user_nick = get_user_property(message.server, user, "nickname")
        if user_nick is None:
            out += "{0}, you have no name. ".format(user.mention)
        else:
            out += "{0}, your name is {1}. ".format(user.mention, user_nick)
    return out

def define(message, d:dict, d_name):
   # try:
    command = message.content.split('"')
    set_generic_dict(d, d_name, command[1], command[3])
    #except:
       # return "invalid response format"
    return "I will respond to \"{0}\" with \"{1}\". ".format(command[1], command[3])

def check_pattern(msg:str, pattern_responses:dict):
    if pattern_responses == {}:
        read_dict_from_file("global_dicts/pattern_responses", pattern_responses)
    for key in pattern_responses.keys():
        if msg[:len(key)] == key:
            param = msg[len(key):]
            return pattern_responses[key].format(param)