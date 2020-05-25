import os
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
    """
    A class that handles discord messages and BicBotModules.
    Parses incoming messges and sends the message to the correct handler loaded by a BicBotModule.
    """

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

    def add_module(self, module: BicBotModule):
        """
        Adds a module to self - it adds the literal_matches, regex_matches, commands, 
        and any_message to the list of things the parser checks each message for.
        Also adds the module itself to modules, with its filename as the key
        Module must be a BicBotModule.

        Todo: make BicBotModule have a list of ModuleFunctions isntead of creating them here
        """
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
        """
        Deals with an incoming message. Checks for a function to handle the message in builtin commands, 
        module commands, literal matches, regex matches, then any_matches in that order.

        Returns the result of the command either as a string or as a MessageResponse. 
        MesasgeResponse is a class that contains everything a discord Messageable can have.
        """
        msg = message.content
        if msg.startswith(self.settings["command_str"]):
            # strip the command string
            msg = msg[len(self.settings["command_str"]):]

            msg_list = msg.split()
            if len(msg_list) > 0:  # check for empty command string
                # command list
                try:
                    content = self.parse_builtins(msg_list, message)
                    if content:
                        return content
                except Exception as e:
                    return "Failed to execute builtin command: " + str(e)

                if msg_list[0] in self.commands.keys():
                    response = ""
                    try:
                        response = self.commands[msg_list[0]].function(
                            message, settings=self.settings)
                    except Exception as e:
                        traceback.print_exc()
                        response = f"Module failed to run command {msg_list[0]}."
                    return response

                else:
                    help_str = self.settings.get("help_str", "help")
                    return f"'{msg_list[0]}' is not a valid command. Try '{help_str}'"

        # check for explicit responses
        elif msg in self.literal_matches:
            response = ""
            try:
                response = self.literal_matches[msg](message)
            except Exception as e:
                traceback.print_exc()
                response = f"Module failed to handle message."
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
                    return response

    async def send_response(self, message_response: MessageResponse, channel: discord.channel.TextChannel):
        """
        Sends a MessageResponse message_response to channel.
        Performs some validation about the message content and formats it such that discord will probably not throw an error.
        
        It may or may not send debug information in the response, and it may or may not log it.
        The logic there is a bit wonky. To be honest this thing needs to be redesigned.
        """
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
        """
        Executes built-in commands that should not be part of a module.
        Why are they here instead of in a module?? I don't know. Security maybe??
        """
        help_str = self.settings.get("help_str", "help")
        if msg_list[0] == help_str:
            if len(msg_list) > 1:
                return helpers.func_doc(globals(), msg_list[1])
            else:
                return consts.cmd_list
        elif msg_list[0] == "commands":
            return "Commands: " + ", ".join(self.commands.keys())

        # static debug/admin commands
        elif msg_list[0] == "eval":
            if message.author == message.guild.owner:
                return eval(helpers.strip2(message.content, "eval"))
            else:
                return "Insufficient permissions. Must be server owner."

        elif msg_list[0] == "exec":
            if message.author == message.guild.owner:
                exec(helpers.strip2(message.content, "exec"))
                return  # exec doesn't return anything, so we return to not send an empty message
            else:
                return "Insufficient permissions. Must be server owner."

        elif msg_list[0] == "ip":
            if message.author == message.guild.owner:
                with os.popen(consts.IP_command) as stream:
                    ip_string = stream.read()
                    return ip_string
            else:
                return "Insufficient permissions. Must be server owner."

        elif msg_list[0] == "modules":
            if message.author == message.guild.owner:
                return "Modules: " + ", ".join(self.modules.keys())
            else:
                return "Insufficient permissions. Must be server owner."
