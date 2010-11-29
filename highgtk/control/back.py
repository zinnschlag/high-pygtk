"""This module defines back-ends for controls.

"""

import inspect


class Function:
    "Call a functino."

    def __init__ (self, function):
        self.function = function

    def execute (self, entity):
        if len (inspect.getargspec (self.function)[0])==0:
            self.function()
        else:
            self.function (entity)
