
from src import module_class
import adapter


def module():

    return module_class.BicBotModule("Base module",
                                     "This is the base module. It contains commands for managing the bot, and demonstrating some of its functionality",
                                     None,
                                     None,
                                     {
                                         "isbot": adapter.isbot,
                                         "ping": adapter.ping,
                                         "version": adapter.version,
                                         "settings": adapter.settings,
                                         "hello": adapter.hello,
                                         "commit": adapter.commit,
                                         "nut": adapter.nut,
                                         "extrathicc": adapter.extrathicc,
                                         "leet": adapter.leet,
                                         "keeb": adapter.keeb,
                                         "callme": adapter.callme,
                                         "myname": adapter.myname,
                                         "call": adapter.call,
                                         "name": adapter.name,
                                         "deleteuser": adapter.deleteuser,
                                         "defexplicit": adapter.defexplicit,
                                         "defpattern": adapter.defpattern})
