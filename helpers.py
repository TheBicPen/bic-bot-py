import os
from datetime import datetime


# helper functions
# def strip1(text: str, strip_text: str): #useless wtf
#     """
#     Returns a string with strip_text stripped from the beginning of text.
#     """
#     return text.lstrip(strip_text)

def strip2(text: str, strip_text: str):
    """
    Returns a string with everything up to and including the first occurence
    of strip_text and 1 additional character stripped from text. 
    If strip_text is not in text, strip the length of strip_text + 1 chars from
    text and return the rest.
    """
    index = text.find(strip_text) + len(strip_text) + \
        1  # accounts for the space
    return text[index:]


def make_directory(dir):
    if not os.path.exists(dir) and dir != '':
        os.makedirs(dir)


def read_file(file: str) -> list:
    """
    Returns the lines of a utf-8 formatted file. If the file does not exist, creates the file
    and returns an empty list.
    #precondition: the directory exists. the file name is valid.
    """
    try:
        file_IO = open(file, "r", encoding="utf8")
        contents = file_IO.read().splitlines()
    except:
        dir = os.path.split(file)[0]
        make_directory(dir)
        file_IO = open(os.path.normpath(file), "x")
        contents = []
    finally:
        file_IO.close()
    return contents


def write_file(file: str, contents: str):
    """
    Checks that the file exists, then writes contents to it
    """
    read_file(file)
    file_IO = open(file, "w")
    file_IO.write(contents)
    file_IO.close


def read_dict_from_file(file: str, d={}):
    """
    Reads a file where each line has 2 words separated 
    by a space, and appends these words to dict as key-value
    pairs. 
    Precondition: each key is present in the file only once.
    """
    contents = read_file(file)
    for line in contents:
        num_semicolons = line.count(";")
        if num_semicolons == 0:
            print("line in file formatted improperly\n")
            return d
        elif num_semicolons == 1:  # no semicolons in text
            words = line.split(";")
            d.update({words[0]: words[1]})
        else:  # semicolons in text
            for ch_index in range(len(line)):
                if line[ch_index] == ";" and line[ch_index-1: ch_index] != "\\":
                    split_index = ch_index
            words = [line[:split_index], line[split_index + 1:]]
            words[0] = words[0].replace("\\", "")
            words[1] = words[1].replace("\\", "")
            d.update({words[0]: words[1]})

    return d


def write_dict_to_file(d: dict, fl: str):
    """
    Writes the key-value pairs in d as space-separated words
    in file. Each pair is on its own line.
    """
    file_obj = open(fl, "w+")
    for key, value in d.items():
        key = key.replace(";", "\\;")
        value = value.replace(";", "\\;")
        file_obj.write("{0};{1}\n".format(key, value))
    file_obj.close()

# def get_trans(fl:str, d:dict):
#     if d != {}:


def convert_string(text: str, conversion: int):
    # convert to desired format
    if conversion == 1:  # to upper
        text = text.upper()
    elif conversion == 2:  # to lower
        text = text.lower()
    elif text == 3:  # aggressively to lower
        text = text.casefold()
    return text


def check_admin(message):
    """
    Returns true only is the message sender is the owner of the server.
    Returns false if an error occurs or if the sender is not the server owner
    """
    if message is None:
        return 0
    try:
        return message.guild.owner == message.author
    except:
        return 0


def get_user_property(server: str, user: str, prop: str, help=False):
    user_to_property = read_dict_from_file(
        "servers/{1}/user_data/{0}".format(user, server), {})
    return user_to_property.get(prop)


def set_user_property(server: str, user: str, prop: str, val, help=False):
    user_to_property = read_dict_from_file(
        "servers/{1}/user_data/{0}".format(user, server))
    user_to_property.update({prop: val})
    write_dict_to_file(
        user_to_property, "servers/{1}/user_data/{0}".format(user, server))


def delete_user(server: str, user_mentions: str, help=False):
    out = ""
    for user in user_mentions:
        try:
            os.remove("servers/{1}/user_data/{0}".format(user, server))
            out += "Deleted {0}'s info.\n".format(user)
        except:
            out += "Failed to delete.\n"
    return out


def get_generic_dict(d: dict, d_name, key, help=False):
    d = read_dict_from_file("global_dicts/{0}".format(d_name), {})
    return d.get(key)


def set_generic_dict(d: dict, d_name, key, val, help=False):
    get_generic_dict(d, d_name, key)
    d.update({key: val})
    write_dict_to_file(d, "global_dicts/{0}".format(d_name))


def func_doc(funcs, func):
    """
    Returns the docstring for a function by name
    """
    if funcs is not None:
        return funcs[func].__doc__
    return globals()[func].__doc__

# logging


def init_log():
    file_name = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
    read_file(file_name)
    log_file = open(file_name, "a+", encoding='utf8')
    log_file.write("Begin logging.\n")
    return log_file


# idk what else to do here
if __name__ != "__main__":
    log_file = init_log()


def log(log_string: str):
    log_file.write(str(log_string) + "\n")
    log_file.flush()
    print(log_string)
