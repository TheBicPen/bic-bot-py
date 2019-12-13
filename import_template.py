from importlib import import_module

class Foo:
     import_ex = False
     os = None
     def __init__(self, imp):
             if imp:
                     self.import_ex = True
                     self.os = import_module('os')
     def do_thing(self):
             print("doing thing")
             if self.import_ex:
                    print(self.os.devnull)
print("running foo(false)")
f1=Foo(False)
f1.do_thing()
f2=Foo(True)
print("running foo(true)")
f2.do_thing()
