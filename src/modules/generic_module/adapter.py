from . import commands as generic_module
import helpers


# the function docstrings get returned when the user uses the help function

def isbot(message):
    """
    Responds "yes".
    """
    return generic_module.isbot(message)


def ping(message):
    """
    Responds with "pong!"
    """
    return generic_module.ping(message)


def version(message):
    """
    Returns the version of the program. Does not work yet.
    """
    return generic_module.version()


def settings():
    """
    Does nothing for now
    """
    return generic_module.settings


def hello(message):
    """
    Says hello and your name
    """
    return generic_module.hello(message)


def commit(message):
    return generic_module.list_response(helpers.read_file("global_lists/commit.txt"))


def nut(message):
    return generic_module.list_response(helpers.read_file("global_lists/nut.txt"))


def extrathicc(message):
    thicc_dict = helpers.read_dict_from_file(
        "global_dicts/extrathicc.txt")
    return generic_module.translate(message, "extrathicc", thicc_dict, self)


def leet(message):
    leet_dict = helpers.read_dict_from_file("global_dicts/leet.txt")
    return generic_module.translate(message, "leet", leet_dict, self)


def keeb(message):
    """
    Responds with whether or not your message has any korean characters
    """
    return generic_module.keeb(message, helpers.read_file("global_dicts/korean.txt"))


def callme(message):
    """
    Sets your nickname - not to be confused with the discord nickname
    """
    return generic_module.set_name(message, [message.author], "callme", self)


def myname(message):
    """
    Gets your nickname - not to be confused with the discord nickname
    """
    return generic_module.get_name(message, [message.author], self)


def call(message):
    """
    Sets a user's nickname - not to be confused with the discord nickname
    """
    return generic_module.set_name(message, message.mentions, "call", self)


def name(message):
    """
    Gets a user's nickname - not to be confused with the discord nickname
    """
    return generic_module.get_name(message, message.mentions, self)


def deleteuser(message):
    return helpers.delete_user(message.guild, message.mentions)


def defexplicit(message):
    """
    The bot will respond to the given text with some other text
    """
    return generic_module.define(message, self.explicit_responses, "explicit_responses")


def defpattern(message):
    """
    Responds to a prompt. The prompt and its response must already be defined. Check `bb help define` for details.
    """
    return generic_module.define(message, self.pattern_responses, "pattern_responses")
