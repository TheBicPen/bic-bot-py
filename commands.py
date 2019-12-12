from commands_generic import * #forgive me
import os
import urllib.request
import aiohttp
import asyncio


import commands_generic
    
def get_user_property(server:str, user:str, prop:str):
    user_to_property = read_dict_from_file("servers/{1}/user_data/{0}".format(user, server), {})
    return user_to_property.get(prop)
    
def set_user_property(server:str, user:str, prop:str, val):
    user_to_property = read_dict_from_file("servers/{1}/user_data/{0}".format(user, server))
    user_to_property.update({prop: val})
    write_dict_to_file(user_to_property, "servers/{1}/user_data/{0}".format(user, server))

def delete_user(server:str, user_mentions:str):
    out = ""
    for user in user_mentions:
        try:
            os.remove("servers/{1}/user_data/{0}".format(user, server))
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
modules = {}
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
                return commands_generic.isbot(message)
            elif msg_list[0] == "ping":
                return commands_generic.ping(message)
            elif msg_list[0] == "version":
                return commands_generic.version()
            elif msg_list[0] == "settings":
                return commands_generic.settings # (settings) <- no longer necessary
            elif msg_list[0] == "hello":
                return commands_generic.hello(message)
            elif msg_list[0] == "commit":
                return commands_generic.list_response(read_file("global_lists/commit.txt"))
            elif msg_list[0] == "nut":
                return commands_generic.list_response(read_file("global_lists/nut.txt"))
            elif msg_list[0] == "extrathicc":
                thicc_dict = read_dict_from_file("global_dicts/extrathicc.txt")
                return commands_generic.translate(message, "extrathicc", thicc_dict)
            elif msg_list[0] == "leet":
                leet_dict = read_dict_from_file("global_dicts/leet.txt")
                return commands_generic.translate(message, "leet", leet_dict)
            elif msg_list[0] == "keeb":
	            return commands_generic.keeb(message, read_file("global_dicts/korean.txt"))
            elif msg_list[0] == "callme":
                return commands_generic.set_name(message, [message.author], "callme")
            elif msg_list[0] == "myname":
                return commands_generic.get_name(message, [message.author])
            elif msg_list[0] == "call":
                return commands_generic.set_name(message, message.mentions, "call")
            elif msg_list[0] == "name":
                return commands_generic.get_name(message, message.mentions)
            elif msg_list[0] == "deleteuser":
                return delete_user(message.guild, message.mentions)
            elif msg_list[0] == "defexplicit":
                return commands_generic.define(message, explicit_responses, "explicit_responses")
            elif msg_list[0] == "defpattern":
                return commands_generic.define(message, pattern_responses, "pattern_responses")

            #image classification
            elif "ML" in modules:
                from image_classification import image_classify_helpers
                if msg_list[0] == "imagecat":
                    return await image_classify_helpers.image_category(message, tf_sess, classifications)
                elif msg_list[0] == "tfstop":
                    return image_classify_helpers.stop_tf()
                #admin-only
                elif msg_list[0] == "tfstart":
                    if message.author == message.guild.owner:
                        return image_classify_helpers.start_tf()
                    else:
                        return "Insufficient permissions. Must be server owner."

            elif msg_list[0] == "eval":
                if message.author == message.guild.owner:
                    #evaluate the message only if the message author is the owner
                    return eval(strip2(message.content, "eval"))
                else:
                    return "Insufficient permissions. Must be server owner."
            elif msg_list[0] == "exec":
                if message.author == message.guild.owner:
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
    elif "ML" in modules and tf_sess is not None and len(message.attachments) > 0:
        from image_classification import image_classify_helpers
        return await image_classify_helpers.image_appropriate(message, tf_sess, classifications)
    else:
        return commands_generic.check_pattern(msg, pattern_responses)