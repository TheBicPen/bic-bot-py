

class ModuleFunction:

    function = None
    module = ""
    help_string = ""
    def __init__(self, function, module_name, help_string = ""):
        if callable(function):
            self.function = function
        else:
            raise TypeError("Object passed in as function must be callable")
        self.module = module_name
        self,help_string = help_string

