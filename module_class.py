
# a class for new modules to make instances of


class Bic_bot_command_module:
    triggers = []
    functions = []
    function_help_docs = []
    module_help_string = "This is what a module sould look like. If you are seeing this, then the help info has not been set properly"

    def __init__(self, module_help_string):
        super().__init__()
        if module_help_string is not None:
            self.module_help_string = module_help_string

    def add_func(self, trigger, function, help_string):
        self.triggers.append(trigger)
        self.functions.append(function)
        self.function_help_docs.append(help_string)
