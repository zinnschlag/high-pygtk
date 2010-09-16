"""Text elements."""

import gtk

import highgtk.entity
import highgtk.present.current

class DocumentElement (highgtk.entity.Entity):
    """Model of a text element."""

    def __init__ (self):
        highgtk.entity.Entity.__init__ (self)
        self.data = gtk.TextBuffer()


class ViewElement (highgtk.entity.ViewElement):
    """View of a text element."""

    def __init__ (self, document):
        highgtk.entity.Entity.__init__ (self)
        self.document = document
        self.presentation = highgtk.present.current.get()

    def show_prepare (self):
        self.presentation.add_element_text (self)

    def hide (self):
        self.presentation.remove_element_text (self)
