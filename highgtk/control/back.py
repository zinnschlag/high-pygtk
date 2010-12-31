"""This module defines back-ends for controls.

"""

import inspect


class Function:
    """Call a function

    The function may have other zero or one (entity) arguments.

    """

    def __init__ (self, function):
        self.function = function

    def execute (self, entity):
        if (len (inspect.getargspec (self.function)[0])==0 or
            inspect.getargspec (self.function)[0][0]=='self'):
            self.function()
        else:
            self.function (entity)
