"""This module provides the entity tree."""

import gtk

import highgtk.present.current

class Entity:
    """This is the entity base class."""

    def __init__ (self):
        self.children = []
        self.parent = None

    def is_linked (self):
        """Is entity linked to an application root?"""
        parent = self
        while parent.parent is not None:
            parent = parent.parent
            if isinstance (parent, Application):
                return True
        return False

    def add (self, entity):
        """Make entity a child of self."""
        if entity.parent is not None:
            entity.remove (keep_children=True)
        entity.parent = self
        self.children.append (entity)
        if self.is_linked():
            self._show()

    def remove (self, remove_parent = True, keep_children = False):
        """Remove self from the entity graph."""
        self._hide()
        if not keep_children:
            for c in self.children:
                c.remove (False, keep_children)
            self.children = []
        if self.parent and remove_parent:
            self.parent._remove_child (self)
        self.parent = None

    def _remove_child (self, child):
        """Remove child.

        Important: The entity can't refuse to remove the child at this point.
        """
        self.children.remove (child)

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

    def get_title (self, child = None):
        """Return title for child or for self if child is None.

        Calls get_title function of parent instead, if available.

        """
        if self.parent is not None:
            parent = getattr (self.parent, "get_title", None)
            if parent is not None:
                return parent (self)
        return "Unnamed"


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

    def get_title (self, child = None):
        """Return title for child or application title if child is None."""
        return self.name

    def done (self):
        gtk.main_quit()


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


class DocumentGroup (Entity):
    """Collection of documents of the same type.

    primary: if True, DocumentGroup will call done function of parent (if available) when
    the last document is removed from the group.

    """

    def __init__ (self, primary):
        Entity.__init__ (self)
        self.primary = primary

    def _remove_child (self, child):
        Entity._remove_child (self, child)
        if not [d for x in self.children if isinstance (x, Document)]:
            if self.parent is not None:
                done = getattr (self.parent, "done", None)
                if done is not None:
                    done()

class Document (Entity):
    """Document: Collection of data.

    """

    def __init__ (self, persistent = False):
        """persistent: keep document after the last view is closed."""
        Entity.__init__ (self)
        self.persistent = persistent

    def close_child_request (self, child):
        """User requested to close a child of this document."""
        child.remove()
        if not [d for x in self.children if isinstance (x, View)]:
            self.remove()

    def get_title (self, child = None):
        """Return title for child or for this document if child is None.

        Calls get_title function of parent instead, if available.

        """
        if self.parent is not None:
            parent = getattr (self.parent, "get_title", None)
            if parent is not None:
                return parent (self)
        return "Document"


class View (Entity):
    """View: Entity that allows the user to view and interact with a document.

    """

    def __init__ (self):
        Entity.__init__ (self)
        self.presentation = highgtk.present.current.get()

    def show (self):
        """Show entity to user."""
        self.presentation.add_view (self)

    def hide (self):
        """Hide entity from user."""
        self.presentation.remove_view (self)

    def close_request (self):
        """User requested to close this view.

        Calls close_child_request function of parent instead, if available.

        """
        if self.parent is not None:
            parent = getattr (self.parent, "close_child_request", None)
            if parent is not None:
                parent (self)
                return
        self.remove()

    def get_title (self, child = None):
        """Return title for this view.

        Calls get_title function of parent instead, if available.

        """
        if self.parent is not None:
            parent = getattr (self.parent, "get_title", None)
            if parent is not None:
                return parent (self)
        return "View"


def get_root (entity):
    """Return the root for the given entity."""
    assert entity is not None
    while entity.parent is not None:
        entity = entity.parent
    assert isinstance (entity, Application)
    return entity
