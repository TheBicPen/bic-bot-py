# from generic_module.commands_generic import *  # forgive me
import os
import urllib.request
import aiohttp
import asyncio
import re
import traceback
import collections
from importlib import import_module

from module_class import BicBotModule
from module_func import ModuleFunction
from message_response import MessageResponse
from discord.abc import Messageable
import discord
import helpers
import consts


class Parser:
    settings = {}
    modules = {}
    literal_matches = {}
    regex_matches = {}
    commands = {}
    any_message = {}

    def __init__(self, settings: dict, modules: list, literal_matches: dict, regex_matches: dict):
        if isinstance(settings, collections.Iterable):
            self.settings.update(settings)
        if isinstance(literal_matches, collections.Iterable):
            self.literal_matches.update(literal_matches)
        if isinstance(regex_matches, collections.Iterable):
            self.regex_matches.update(regex_matches)
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

                # add functions to handle any message
                if isinstance(module_items.any_message, collections.Callable):
                    self.any_message[module_items.name] = ModuleFunction(
                        module_items.any_matches, module_items.name)

                # add literal matches
                for command in module_items.literal_matches:
                    if command not in self.literal_matches:
                        self.literal_matches[command] = ModuleFunction(
                            module_items.literal_matches[command], module_items.name)

                # add literal matches
                for command in module_items.regex_matches:
                    if command not in self.regex_matches:
                        self.regex_matches[command] = ModuleFunction(
                            module_items.regex_matches[command], module_items.name)

                print("Imported module " + str(module))
        except Exception:
            print("Failed to import module " + str(module))
            traceback.print_exc()
            return None

    async def parse_message(self, message):
        msg = message.content
        if msg.startswith(self.settings["command_str"]):
            # strip the command string
            msg = msg[len(self.settings["command_str"]):]

            msg_list = msg.split()
            if len(msg_list) > 0:  # check for empty command string
                # command list
                content = self.parse_builtins(msg_list, message)
                if content:
                    return content

        # check for explicit responses
        elif msg in self.literal_matches:
            response = ""
            try:
                response = self.literal_matches[msg](message)
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
            for pattern in self.regex_matches:
                if pattern.match(message):
                    response = ""
                    try:
                        response = self.regex_matches[msg](message)
                    except Exception as e:
                        traceback.print_exc()
                        response = f"Module failed to handle pattern-matched message."
                    else:
                        pass
                    finally:
                        pass
                    return response
        # classify image if applicable
        # elif consts.ML_lib in self.modules and tf_sess is not None and len(message.attachments) > 0:
        #     return await self.modules[consts.ML_lib].image_appropriate(message, tf_sess, classifications)
        # else:
        #     return self.modules["commands_generic"].check_pattern(msg, self.regex_matches, help=cmd_help)

    async def send_response(self, message_response: MessageResponse, channel: discord.channel.TextChannel):
        if not isinstance(message_response, MessageResponse):
            raise TypeError("Message response is not the correct type")

        content = None
        files = message_response.files if message_response.files is not None and len(
            message_response.files > 1) else None
        file = message_response.files if message_response.files is not None and len(
            message_response.files == 1) else None

        if not message_response.message and message_response.debug and self.settings.get("send_debug", None):
            content = message_response.debug
        elif message_response.message and not message_response.debug:
            content = message_response.message
        elif self.settings.get("send_debug", None) and len(message_response.message) + len(message_response.debug) < 2000:
            content = str(message_response.message) + \
                          str(message_response.debug)
        if not content is None:
            try:
                if len(str(content)) > 2000:
                    content = "message too long: " + str(len(str(content)))
            except:
                helpers.log(
                    "Failed to process message of type " + str(type(content)))
        await channel.send(content=content, tts=message_response.tts, embed=message_response.embed, file=file, files=files, delete_after=message_response.delete_after)


    def parse_builtins(self, msg_list, message):
        help_str = self.settings.get("help_str", "help")
        if msg_list[0] == help_str:
            if len(msg_list) > 1:
                return helpers.func_doc(globals(), msg_list[1])
            else:
                return consts.cmd_list

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
                with os.popen(consts.IP_command) as stream:
                    ip_string = stream.read()
                    return ip_string
            else:
                return "Insufficient permissions. Must be server owner."
        elif msg_list[0] == "modules":
            if message.author == message.guild.owner:
                # evaluate the message only if the message author is the owner
                return self.modules
            else:
                return "Insufficient permissions. Must be server owner."

        elif msg_list[0] in self.commands.keys():
            return self.commands[msg_list[0]].function(message)

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
