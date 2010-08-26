"""This module generates layouts for data lists.
"""

import gtk

import highgtk.data

class PlainLayout:
    """Single column layout based on a VBox."""

    def __init__ (self, data):
        self.data = data

    def build (self, widget):
        vbox = gtk.VBox()
        vbox.set_border_width (4)
        widget.add (vbox)
        self.widgets = {}
        for e in self.data:
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

    def get_data (self):
        result = {}
        for e in self.data:
            if isinstance (e, highgtk.data.Text):
                result[e.id_] = self.widgets[e.id_].get_text()
        return result

def get_layout (data):
    return PlainLayout (data)
