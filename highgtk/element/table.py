"""Table element.

Attention: Do not confuse this with the gtk table widget!
"""

import logging
import copy

import gtk

import highgtk.entity
import highgtk.present.current
import highgtk.cell

log = logging.getLogger ("highgtk.element")

class BaseDocumentElement (highgtk.entity.Entity):
    """Base class for table document elements."""

    def __init__ (self, columns):
        """columns: list of data entries. If label is None, the column is hidden.

        If the id of the column starts with a '+', it is expanded, if the presentation does
        support expanding.

        """

        highgtk.entity.Entity.__init__ (self)
        self.columns = columns
        types = []
        for c in columns:
            types.append (highgtk.cell.get_type (c))
        self.data = gtk.ListStore (*types)


class OrderedDocumentElement (BaseDocumentElement):
    """Table with ordered rows.

    Optional attributes:
    - reorder: if present (value not None), the table rows can be reordered via drag & drop
    (note: for forward compatibility purpose the attribute should be set to 0)

    """

    def update (self, content):
        """Update table content. If the table contains a column with the ID "ID" or "+ID",
        the table is updated, which will keep the selection status unmodified.
        Else the old table content is wiped and replaced by the new.

        content: list of rows (each row being a list)
        """
        columns = [c for c in self.columns if c.id_=="ID" or c.id_=="+ID"]
        if columns:
            self._update (content)
        else:
            self._set (content)

    def _update (self, content):
        n_list = [ i for i, c in enumerate (self.columns) if c.id_=="ID" or c.id_=="+ID" ]
        if not len (n_list) == 1:
            log.warning (
                "ID column in table element not unique -> skipping _update and using _set instead")
            self._set (content)
            return
        n = n_list[0]
        ids = [r[n] for r in self.data]
        # add and update
        new_ids = []
        for r in content:
            if r[n] in ids:
                ids.remove (r[n])
                for r2 in self.data:
                    if r2[n] == r[n]:
                        l = len (r)
                        for i in range (l):
                             r2[n] = copy.copy (r[n])
                        break
            else:
                self.data.append (r)
                new_ids.append (r[n])
        # remove
        it = self.data.get_iter_first()
        while it is not None and self.data.iter_is_valid (it):
            id_ = self.data.get_value (it, n)
            if id_ in ids:
                self.data.remove (it)
            else:
                it = self.data.iter_next (it)

    def _set (self, content):
        self.data.clear()
        for r in content:
            self.data.append (r)

class UnorderedDocumentElement (BaseDocumentElement):
    """Table with no inherent row order.

    """
    pass


class ViewElement (highgtk.entity.ViewElement):
    """View of a table element.

    Optional attributes:
    - search: if present (value not None), ID of the column used for searching
    """

    def __init__ (self, document):
        highgtk.entity.Entity.__init__ (self)
        self.document = document
        self.presentation = highgtk.present.current.get()

    def show_prepare (self):
        self.presentation.add_element_table (self)

    def hide (self):
        self.presentation.remove_element_table (self)
