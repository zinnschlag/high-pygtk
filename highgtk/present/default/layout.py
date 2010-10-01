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
        if isinstance (widget, gtk.Box):
            widget.pack_start (vbox, expand=False, fill=False)
        else:
            widget.add (vbox)
        self.widgets = {}
        for e, c in self.data:
            inner = gtk.VBox()
            vbox.pack_start (inner, expand=False, fill=False, padding=8)
            if e.label!="" and not isinstance (e, highgtk.data.Boolean):
                label = gtk.Label (e.label)
                label.set_alignment (0, 0.5)
                inner.pack_start (label, expand=False, fill=False)
            if isinstance (e, highgtk.data.Text):
                entry = gtk.Entry()
                if e.hint!="":
                    entry.set_tooltip (e.hint)
                inner.pack_start (entry, expand=False, fill=False)
                self.widgets[e.id_] = entry
            elif isinstance (e, highgtk.data.HiddenText):
                entry = gtk.Entry()
                entry.set_visibility (False)
                if e.hint!="":
                    entry.set_tooltip (e.hint)
                inner.pack_start (entry, expand=False, fill=False)
                self.widgets[e.id_] = entry
            elif isinstance (e, highgtk.data.Boolean):
                entry = gtk.CheckButton (e.label)
                if e.hint!="":
                    entry.set_tooltip (e.hint)
                inner.pack_start (entry, expand=False, fill=False)
                self.widgets[e.id_] = entry
            else:
                raise Exception ("unsupported data type")
            if c is not None:
                for i in c:
                    i.configure (self.data, entry, e)

    def get_data (self):
        """Return dictionary with the data entered into the layout."""
        result = {}
        for e, k in self.data:
            if isinstance (e, highgtk.data.Text):
                result[e.id_] = self.widgets[e.id_].get_text()
            elif isinstance (e, highgtk.data.HiddenText):
                result[e.id_] = self.widgets[e.id_].get_text()
            if isinstance (e, highgtk.data.Boolean):
                result[e.id_] = self.widgets[e.id_].get_active()
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
