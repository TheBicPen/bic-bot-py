# from generic_module.commands_generic import *  # forgive me
import os
import urllib.request
import aiohttp
import asyncio
import consts
import re
import traceback
import collections
from importlib import import_module

# import sys
# print(sys.path)
# from modules import generic_module


# import generic_module.commands
from module_class import BicBotModule
from module_func import ModuleFunction
import helpers


class Parser:
    settings = {}
    modules = {}
    explicit_responses = {}
    pattern_responses = {}
    commands = {}

    def __init__(self, settings: dict, modules: list, explicit_responses: dict, pattern_responses: dict):
        if isinstance(settings, collections.Iterable):
            self.settings.update(settings)
        if isinstance(explicit_responses, collections.Iterable):
            self.explicit_responses.update(explicit_responses)
        if isinstance(pattern_responses, collections.Iterable):
            self.pattern_responses.update(pattern_responses)
        for module in modules:
            self.add_module(module)

    def add_module(self, module):
        try:
            self.modules[module] = import_module(f"modules.{module}.module")
            module_items = self.modules[module].module()
            if not isinstance(module_items, BicBotModule):
                error = f"Module {module} is of incorrect type {type(module)}"
                print(error)
                raise ImportError(error)
            else:
                # add command matches
                for command in module_items.command_matches:
                    module_function = ModuleFunction(
                        module_items.command_matches[command], module_items.name)
                    if command not in self.commands:
                        self.commands[command] = module_function
                    else:
                        new_name = f"{module_items.name}.{command}"
                        existing_module = self.commands[command]["module"]
                        print(
                            f"Command {command} already loaded from module {existing_module}. Loading as {new_name} instead")
                        self.commands[new_name] = module_function
                print("Imported module " + str(module))
        except Exception as e:
            print("Failed to import module " + str(module))
            traceback.print_exc()
            return None

    async def parse_message(self, message):
        cmd_help = False
        help_str = "help"
        msg = message.content
        if msg.startswith(self.settings["command_str"]):
            # strip the command string
            msg = msg[len(self.settings["command_str"]):]

            # # check whether the message is for help with a command
            # if msg.startswith(help_str):
            #     cmd_help = True
            #     msg = msg[len(help_str):]

            msg_list = msg.split()
            if len(msg_list) > 0:  # check for empty command string
                # command list

                if msg_list[0] == help_str:
                    if len(msg_list) > 1:
                        return helpers.func_doc(globals(), msg_list[1])
                    else:
                        return consts.cmd_list

                elif msg_list[0] in self.commands.keys():
                    self.commands[msg_list[0]](message)

                # # image classification
                # elif msg_list[0] == "imagecat":
                #     if consts.ML_lib not in self.modules:
                #         return "Image classification module inactive"
                #     else:
                #         return await self.modules[consts.ML_lib].image_category(message, tf_sess, classifications, help=cmd_help)
                # elif msg_list[0] == "tfstop":
                #     if consts.ML_lib not in self.modules:
                #         return "Image classification module inactive"
                #     else:
                #         return self.modules[consts.ML_lib].stop_tf(help=cmd_help)
                # # admin-only
                # elif msg_list[0] == "tfstart":
                #     if message.author != message.guild.owner:
                #         return "Insufficient permissions. Must be server owner."
                #     elif consts.ML_lib not in self.modules:
                #         return "Image classification module inactive"
                #     else:
                #         return self.modules[consts.ML_lib].start_tf(help=cmd_help)

                # static debug/admin commands
                elif msg_list[0] == "eval":
                    if message.author == message.guild.owner:
                        # evaluate the message only if the message author is the owner
                        return eval(helpers.strip2(message.content, "eval"))
                    else:
                        return "Insufficient permissions. Must be server owner."
                elif msg_list[0] == "exec":
                    if message.author == message.guild.owner:
                        # evaluate the message only if the message author is the owner
                        exec(helpers.strip2(message.content, "exec"))
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
            response = ""
            try:
                response = self.explicit_responses[msg](message)
            except Exception as e:
                traceback.print_exc()
                response = f"Module failed to handle message."
            else:
                pass
            finally:
                pass
            return response

        # match regexes
        else:
            for pattern in self.pattern_responses:
                if pattern.match(message):
                    response = ""
            try:
                response = self.pattern_responses[msg](message)
            except Exception as e:
                traceback.print_exc()
                response = f"Module failed to handle regex-matched message."
            else:
                pass
            finally:
                pass
            return response
        # classify image if applicable
        # elif consts.ML_lib in self.modules and tf_sess is not None and len(message.attachments) > 0:
        #     return await self.modules[consts.ML_lib].image_appropriate(message, tf_sess, classifications)
        # else:
        #     return self.modules["commands_generic"].check_pattern(msg, self.pattern_responses, help=cmd_help)
