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
        assert entity.parent is None
        entity.parent = self
        self.children.append (entity)

    def remove (self, remove_parent = True, keep_children = False):
        """Remove self from the entity graph."""
        if not keep_children:
            for c in self.children:
                c.remove (False, keep_children)
            self.children = []
        self.hide()
        if self.parent and remove_parent:
            self.parent.children.remove (self)
        self.parent = None

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

def get_root (entity):
    """Return the root for the given entity."""
    assert entity is not None
    while entity.parent is not None:
        entity = entity.parent
    assert isinstance (entity, Application)
    return entity
