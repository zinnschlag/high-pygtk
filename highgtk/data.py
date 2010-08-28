"""This module defines data entries."""

class Text:
    """Basic text entry."""

    def __init__ (self, id_, label, default_value = "", hint = ""):
        self.id_ = id_
        self.label = label
        self.default_value = default_value
        self.hint = hint
