"""This module defines data entries."""

class Text:
    """Basic text entry."""

    def __init__ (self, id_, label, default_value = "", hint = ""):
        self.id_ = id_
        self.label = label
        self.default_value = default_value
        self.hint = hint

class HiddenText:
    """Text entry, that must not be shown on the screen."""

    def __init__ (self, id_, label, default_value = "", hint = ""):
        self.id_ = id_
        self.label = label
        self.default_value = default_value
        self.hint = hint

class Boolean:
    """Boolean value (True or False)."""

    def __init__ (self, id_, label, default_value = False, hint = ""):
        self.id_ = id_
        self.label = label
        self.default_value = default_value
        self.hint = hint
