from . import commands as generic_module
import helpers


# the function docstrings get returned when the user uses the help function

def isbot(message, settings=None):
    """
    Responds "yes".
    """
    return generic_module.isbot(message)


def ping(message, settings=None):
    """
    Responds with "pong!"
    """
    return generic_module.ping(message)


def version(message, settings=None):
    """
    Returns the version of the program. Does not work yet.
    """
    return generic_module.version()


# def settings(message, settings=None):
#     """
#     Does nothing for now
#     """
#     return generic_module.settings


def hello(message, settings=None):
    """
    Says hello and your name
    """
    return generic_module.hello(message)


def commit(message, settings=None):
    return generic_module.list_response(helpers.read_file("global_lists/commit.txt"))


def nut(message, settings=None):
    return generic_module.list_response(helpers.read_file("global_lists/nut.txt"))


def extrathicc(message, settings=None):
    thicc_dict = helpers.read_dict_from_file(
        "global_dicts/extrathicc.txt")
    return generic_module.translate(message, "extrathicc", thicc_dict, settings)


def leet(message, settings=None):
    leet_dict = helpers.read_dict_from_file("global_dicts/leet.txt")
    return generic_module.translate(message, "leet", leet_dict, settings)


def keeb(message, settings=None):
    """
    Responds with whether or not your message has any korean characters
    """
    return generic_module.keeb(message, helpers.read_file("global_dicts/korean.txt"))


def callme(message, settings=None):
    """
    Sets your nickname - not to be confused with the discord nickname
    """
    return generic_module.set_name(message, [message.author], "callme", settings)


def myname(message, settings=None):
    """
    Gets your nickname - not to be confused with the discord nickname
    """
    return generic_module.get_name(message, [message.author], settings)


def call(message, settings=None):
    """
    Sets a user's nickname - not to be confused with the discord nickname
    """
    return generic_module.set_name(message, message.mentions, "call", settings)


def name(message, settings=None):
    """
    Gets a user's nickname - not to be confused with the discord nickname
    """
    return generic_module.get_name(message, message.mentions, settings)


def deleteuser(message, settings=None):
    return helpers.delete_user(message.guild, message.mentions)


def defexplicit(message, settings=None):
    """
    The bot will respond to the given text with some other text
    """
    return generic_module.define(message, settings.explicit_responses, "explicit_responses")


def defpattern(message, settings=None):
    """
    Responds to a prompt. The prompt and its response must already be defined. Check `bb help define` for details.
    """
    return generic_module.define(message, settings.pattern_responses, "pattern_responses")
