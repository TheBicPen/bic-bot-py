

from helpers_generic import *  # forgive me

# no params, simple text


def isbot(message):
    return "yes"


def ping(message):
    return "pong!"

# no params, other


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

# params: message only


def hello(message):
    return 'Hello {0.author.mention}'.format(message)


async def move_message(message, new_channel):
    await message.delete()
    new_channel.send("This message sent by {0} has been moved from {1}. Original message: {2}"
                     .format(message.author, message.channel, message.content), message.attachments)


# params: global_lists only
def list_response(l: list):
    import random
    return l[random.randrange(len(l))]


def keeb(message, korean_list: list):
    for letter in message.content:
        if letter in korean_list:
            return True
    return False

#params: message and global_lists


def translate(message: str, key: str, trans_dict: dict, convert_text=1):
    if trans_dict == {}:
        read_dict_from_file("global_dicts/{0}.txt".format(key), trans_dict)
    out = ""
    msg = strip2(strip2(message.content, settings["command_str"]), key)
    msg = convert_string(msg, convert_text)
    for ch in msg:  # dict contains uppercase letters
        out += trans_dict.get(ch, ch)
    return out
#params: message and user_data


def set_name(message, user_list, trigger_string):  # not to be confused with discord nickname
    if settings.get("annoyed_everyone", True) and message.mention_everyone:
        return settings.get("everyone_string", "no u")
    elif message.mention_everyone:
        for member in message.guild.members:
            user_list.append(member)
        nickname = strip2(message.content, "@everyone")
    elif user_list == [message.author]:  # prevents unnecessary stripping
        nickname = strip2(message.content, trigger_string)
    elif len(user_list) == 0:
        return "No valid user mentions."
    else:
        for user in user_list:
            nickname = strip2(message.content, str(user.mention))
    out = ""
    # not necessary, since there will be at least 1 mention following it
    # nickname = strip2(message.content, trigger_string) #command_text must be separate from the command by a space
    for user in user_list:
        set_user_property(message.guild, user, "nickname", nickname)
        out += "{0}, I will call you {1}. ".format(
            user.mention, get_user_property(message.guild, user, "nickname"))
    return out


def get_name(message, user_list):
    if settings.get("annoyed_everyone", True) and message.mention_everyone:
        return settings.get("everyone_string", "no u")
    elif message.mention_everyone:
        for member in message.guild.members:
            user_list.append(member)
    elif len(user_list) == 0:
        return "No valid user mentions."
    out = ""
    for user in user_list:
        user_nick = get_user_property(message.guild, user, "nickname")
        if user_nick is None:
            out += "{0}, you have no name. ".format(user.mention)
        else:
            out += "{0}, your name is {1}. ".format(user.mention, user_nick)
    return out


def define(message, d: dict, d_name):
   # try:
    command = message.content.split('"')
    set_generic_dict(d, d_name, command[1], command[3])
    # except:
    # return "invalid response format"
    return "I will respond to \"{0}\" with \"{1}\". ".format(command[1], command[3])


def check_pattern(msg: str, pattern_responses: dict):
    if pattern_responses == {}:
        read_dict_from_file(
            "global_dicts/pattern_responses", pattern_responses)
    for key in pattern_responses.keys():
        if msg[:len(key)] == key:
            param = msg[len(key):]
            return pattern_responses[key].format(param)
