"""This module provides the entity tree."""

import gtk

import highgtk.present.current

class Entity:
    """This is the entity base class."""

    def __init__ (self):
        self.children = []
        self.parent = None

    def add (self, entity):
        """Make entity a child of self."""
        if entity.parent is not None:
            entity.remove (keep_children=True)
        entity.parent = self
        self.children.append (entity)
        self._show()

    def remove (self, remove_parent = True, keep_children = False):
        """Remove self from the entity graph."""
        self._hide()
        if not keep_children:
            for c in self.children:
                c.remove (False, keep_children)
            self.children = []
        if self.parent and remove_parent:
            self.parent.children.remove (self)
        self.parent = None

    def _show (self):
        self.show()
        for c in self.children:
            c._show()

    def _hide (self):
        self.hide()
        for c in self.children:
            c._hide()

    def show (self):
        """Show entity to user."""
        pass

    def hide (self):
        """Hide entity from user."""
        pass


class Application (Entity):
    """Entity that represents the whole application.

    Note: The root entity must be an application (either an instance of this class or
    a derived class.

    """

    def __init__ (self, name):
        """
        name: Applications name as presented to the user
        """
        Entity.__init__ (self)
        self.name = name
        self.presentation = highgtk.present.current.get()

    def run (self):
        """Run main loop (blocks until application is qutting)."""
        gtk.main()

    def terminate (self, error):
        """Terminate application with an error message."""
        self.presentation.terminate (self, error)


class Report (Entity):
    """Report: Application is passing out information to the user.
    """

    def __init__ (self, type_, primary = None, secondary = None):
        """
        type: info, warning, error
        primary: Primary message
        secondary: Secondary message
        """
        Entity.__init__ (self)
        self.type = type_
        self.primary = primary
        self.secondary = secondary
        self.presentation = highgtk.present.current.get()

    def show (self):
        """Show entity to user."""
        self.presentation.add_report (self)

    def hide (self):
        """Hide entity from user."""
        self.presentation.remove_inquiry (self)


class Inquiry (Entity):
    """Inquiry: Applications requesting input from user.

    Optional attributes:
    - title: string
    - ok_text: string or gtk stock item
    - ok_method: method of parent of self to be called in case of success (defaults to inquiry_okay)
    signature: f (self, inquiry, result_dict)
    - cancel_method: method of parent of self to be called in case of failure (no function called, if
    attribute is not pressent)
    signature: f (self, inquiry)

    """

    def __init__ (self, data):
        "data: a list of data entries"
        Entity.__init__ (self)
        self.data = data
        self.presentation = highgtk.present.current.get()
        self.error_report = Report ("error")

    def show (self):
        """Show entity to user."""
        self.presentation.add_inquiry (self)

    def hide (self):
        """Hide entity from user."""
        self.presentation.remove_inquiry (self)


def get_root (entity):
    """Return the root for the given entity."""
    assert entity is not None
    while entity.parent is not None:
        entity = entity.parent
    assert isinstance (entity, Application)
    return entity
