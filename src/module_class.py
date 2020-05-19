
# a class for new modules to make instances of

default_help_string = "This is what a module sould look like. If you are seeing this, then the module info has not been set properly"


class BicBotModule:

    name = ""
    help_string = ""

    # triggers for functions
    literal_matches = {}  # message contains literal string
    regex_matches = {}  # message matches regex
    command_matches = {}  # bot commands

    def __init__(self, name: str = "Module", module_help_string: str = default_help_string,
                 literal_matches: dict = {}, regex_matches: dict = {}, command_matches: dict = {}):

        self.module_help_string = module_help_string
        self.name = name # name is used as an additional command keyword in case of command name conflicts
        self.literal_matches = literal_matches
        self.regex_matches = regex_matches
        self.command_matches = command_matches
