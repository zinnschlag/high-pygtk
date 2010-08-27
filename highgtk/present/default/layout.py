"""This module generates layouts for data lists.
"""

import gtk

import highgtk.data

class PlainLayout:
    """Single column layout based on a VBox."""

    def __init__ (self, data):
        self.data = data

    def build (self, widget):
        """Insert layout into widget."""
        vbox = gtk.VBox()
        vbox.set_border_width (4)
        widget.add (vbox)
        self.widgets = {}
        for e, c in self.data:
            inner = gtk.VBox()
            vbox.pack_start (inner, expand=False, fill=False, padding=8)
            if e.label!="":
                label = gtk.Label (e.label)
                label.set_alignment (0, 0.5)
                inner.pack_start (label, expand=False, fill=False)
            if isinstance (e, highgtk.data.Text):
                entry = gtk.Entry()
                entry.set_max_length (e.max_len)
                if e.hint!="":
                    entry.set_tooltip (e.hint)
                inner.pack_start (entry, expand=False, fill=False)
                self.widgets[e.id_] = entry
                if c is not None:
                    for i in c:
                        i.configure (self.data, entry, e)

    def get_data (self):
        """Return dictionary with the data entered into the layout."""
        result = {}
        for e, k in self.data:
            if isinstance (e, highgtk.data.Text):
                result[e.id_] = self.widgets[e.id_].get_text()
        return result

    def get_error (self):
        """Return a constraint error or None."""
        result = self.get_data()
        for e, c in self.data:
            if c is not None:
                for i in c:
                    error = i.get_error (self.data, result, e)
                    if error is not None:
                        return error

def get_layout (data):
    """Return a layout suitable for data."""
    return PlainLayout (data)
