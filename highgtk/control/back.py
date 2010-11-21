"""This module defines back-ends for controls.

"""

import inspect


class Method:
    "Call a member functino."

    def __init__ (self, object_, function):
        self.object_ = object_
        self.function = function

    def execute (self, entity):
        function = getaatr (object_, function)
        if len (inspect.getargspec (function)[0])==1:
            function()
        else:
            function (entity)


class Function:
    "Call a functino."

    def __init__ (self, function):
        self.function = function

    def execute (self, entity):
        if len (inspect.getargspec (self.function)[0])==0:
            self.function()
        else:
            self.function (entity)
