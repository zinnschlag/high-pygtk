"""Table element.

Attention: Do not confuse this with the gtk table widget!
"""

import gtk

import highgtk.entity
import highgtk.present.current
import highgtk.cell

class BaseDocumentElement (highgtk.entity.Entity):
    """Base class for table document elements."""

    def __init__ (self, columns):
        """columns: list of data entries. If label is None, the column is hidden.
        """

        highgtk.entity.Entity.__init__ (self)
        self.columns = columns
        types = []
        for c in columns:
            types.append (highgtk.cell.get_type (c))
        self.data = gtk.TreeStore (*types)

class OrderedDocumentElement (BaseDocumentElement):
    """Table with ordered rows.

    Optional attributes:
    - reorder: if present (value not None), the table rows can be reordered via drag & drop
    (note: for forward compatibility purpose the attribute should be set to 0)

    """
    pass

class UnorderedDocumentElement (BaseDocumentElement):
    pass

class ViewElement (highgtk.entity.ViewElement):
    """View of a table element."""

    def __init__ (self, document):
        highgtk.entity.Entity.__init__ (self)
        self.document = document
        self.presentation = highgtk.present.current.get()

    def show_prepare (self):
        self.presentation.add_element_table (self)

    def hide (self):
        self.presentation.remove_element_table (self)
