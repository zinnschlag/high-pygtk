"""This module defines data entries."""

class Text:
    """Basic text entry with optional length limit."""

    def __init__ (self, id_, label, default_value = "", max_len = 0, hint = ""):
        self.id_ = id_
        self.label = label
        self.default_value = default_value
        self.max_len = max_len
        self.hint = hint
