"""This module defines front-ends for controls.

Note: The actual rendering of the controls is left to the presentation layer."""

import gtk

class Stock:
    """Stock item."""

    def __init__ (self, stock_id, tooltip = None, shortcut = None):
        self.stock_id = stock_id
        self.tooltip = tooltip
        self.shortcut = shortcut

    def make_action (self, name):
        """Create a gtk action for this item."""
        return gtk.Action (name, None, self.tooltip, self.stock_id)

class Custom:
    """Custom item."""

    def __init__ (self, label, tooltip = None, shortcut = None):
        self.label = label
        self.tooltip = tooltip
        self.shortcut = shortcut

    def make_action (self, name):
        """Create a gtk action for this item."""
        return gtk.Action (name, self.label, self.tooltip, None)
