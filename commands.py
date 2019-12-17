from commands_generic import *  # forgive me
import os
import urllib.request
import aiohttp
import asyncio
import consts

from importlib import import_module


def get_user_property(server: str, user: str, prop: str):
    user_to_property = read_dict_from_file(
        "servers/{1}/user_data/{0}".format(user, server), {})
    return user_to_property.get(prop)


def set_user_property(server: str, user: str, prop: str, val):
    user_to_property = read_dict_from_file(
        "servers/{1}/user_data/{0}".format(user, server))
    user_to_property.update({prop: val})
    write_dict_to_file(
        user_to_property, "servers/{1}/user_data/{0}".format(user, server))


def delete_user(server: str, user_mentions: str):
    out = ""
    for user in user_mentions:
        try:
            os.remove("servers/{1}/user_data/{0}".format(user, server))
            out += "Deleted {0}'s info.\n".format(user)
        except:
            out += "Failed to delete.\n"
    return out


def get_generic_dict(d: dict, d_name, key):
    d = read_dict_from_file("global_dicts/{0}".format(d_name), {})
    return d.get(key)


def set_generic_dict(d: dict, d_name, key, val):
    get_generic_dict(d, d_name, key)
    d.update({key: val})
    write_dict_to_file(d, "global_dicts/{0}".format(d_name))


class parser:
    settings = {}
    modules = {}
    explicit_responses = {}
    pattern_responses = {}

    def __init__(self, settings: dict, modules: list, explicit_responses: dict, pattern_responses: dict):
        self.settings = settings
        self.explicit_responses = explicit_responses
        self.pattern_responses = pattern_responses
        for module in modules:
            try:
                self.modules[module] = import_module(module)
                print("Imported module " + str(module))
            except Exception as e:
                print("Failed to import module " + str(module))
                print(str(e))
                return None

    async def parse_message(self, message):
        msg = message.content
        if msg.startswith(self.settings["command_str"]):
            # strip the command string
            msg = msg[len(self.settings["command_str"]):]
            msg_list = msg.split()
            if len(msg_list) > 0:  # check for empty command string
                # command list

                if msg_list[0] == "isbot":
                    return self.modules["commands_generic"].isbot(message)
                elif msg_list[0] == "ping":
                    return self.modules["commands_generic"].ping(message)
                elif msg_list[0] == "version":
                    return self.modules["commands_generic"].version()
                elif msg_list[0] == "settings":
                    # (settings) <- no longer necessary
                    return self.modules["commands_generic"].settings
                elif msg_list[0] == "hello":
                    return self.modules["commands_generic"].hello(message)
                elif msg_list[0] == "commit":
                    return self.modules["commands_generic"].list_response(read_file("global_lists/commit.txt"))
                elif msg_list[0] == "nut":
                    return self.modules["commands_generic"].list_response(read_file("global_lists/nut.txt"))
                elif msg_list[0] == "extrathicc":
                    thicc_dict = read_dict_from_file(
                        "global_dicts/extrathicc.txt")
                    return self.modules["commands_generic"].translate(message, "extrathicc", thicc_dict)
                elif msg_list[0] == "leet":
                    leet_dict = read_dict_from_file("global_dicts/leet.txt")
                    return self.modules["commands_generic"].translate(message, "leet", leet_dict)
                elif msg_list[0] == "keeb":
                    return self.modules["commands_generic"].keeb(message, read_file("global_dicts/korean.txt"))
                elif msg_list[0] == "callme":
                    return self.modules["commands_generic"].set_name(message, [message.author], "callme")
                elif msg_list[0] == "myname":
                    return self.modules["commands_generic"].get_name(message, [message.author])
                elif msg_list[0] == "call":
                    return self.modules["commands_generic"].set_name(message, message.mentions, "call")
                elif msg_list[0] == "name":
                    return self.modules["commands_generic"].get_name(message, message.mentions)
                elif msg_list[0] == "deleteuser":
                    return delete_user(message.guild, message.mentions)
                elif msg_list[0] == "defexplicit":
                    return self.modules["commands_generic"].define(message, explicit_responses, "explicit_responses")
                elif msg_list[0] == "defpattern":
                    return self.modules["commands_generic"].define(message, pattern_responses, "pattern_responses")

                # image classification
                elif msg_list[0] == "imagecat":
                    if consts.ML_lib not in self.modules:
                        return "Image classification module inactive"
                    else:
                        return await self.modules[consts.ML_lib].image_category(message, tf_sess, classifications)
                elif msg_list[0] == "tfstop":
                    if consts.ML_lib not in self.modules:
                        return "Image classification module inactive"
                    else:
                        return self.modules[consts.ML_lib].stop_tf()
                # admin-only
                elif msg_list[0] == "tfstart":
                    if message.author != message.guild.owner:
                        return "Insufficient permissions. Must be server owner."
                    elif consts.ML_lib not in self.modules:
                        return "Image classification module inactive"
                    else:
                        return self.modules[consts.ML_lib].start_tf()

                # static debug/admin commands
                elif msg_list[0] == "eval":
                    if message.author == message.guild.owner:
                        # evaluate the message only if the message author is the owner
                        return eval(strip2(message.content, "eval"))
                    else:
                        return "Insufficient permissions. Must be server owner."
                elif msg_list[0] == "exec":
                    if message.author == message.guild.owner:
                        # evaluate the message only if the message author is the owner
                        exec(strip2(message.content, "exec"))
                        return  # exec doesn't return anything, so we return to not send an empty message
                    else:
                        return "Insufficient permissions. Must be server owner."
                elif msg_list[0] == "ip":
                    if message.author == message.guild.owner:
                        # evaluate the message only if the message author is the owner
                        stream = os.popen(consts.IP_command)
                        ip_string = stream.read()
                        stream.close()
                        return ip_string
                    else:
                        return "Insufficient permissions. Must be server owner."
                elif msg_list[0] == "modules":
                    if message.author == message.guild.owner:
                        # evaluate the message only if the message author is the owner
                        return self.modules
                    else:
                        return "Insufficient permissions. Must be server owner."
                else:
                    return "invalid command"
        # check for explicit responses
        elif msg in self.explicit_responses:
            return self.explicit_responses[msg]
        # classify image if applicable
        elif consts.ML_lib in self.modules and tf_sess is not None and len(message.attachments) > 0:
            return await self.modules[consts.ML_lib].image_appropriate(message, tf_sess, classifications)
        else:
            return self.modules["commands_generic"].check_pattern(msg, pattern_responses)
