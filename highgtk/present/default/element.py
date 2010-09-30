
import gtk

import highgtk.cell

def add_text (element):
    widget = getattr (element, "present_widget", None)
    if widget is None:
        element.present_widget = gtk.TextView (element.document.data)

def remove_text (element):
    widget = getattr (element, "present_widget", None)
    if widget is not None:
        del element.present_widget

def add_table (element):
    widget = getattr (element, "present_widget", None)
    if widget is None:
        element.present_widget = gtk.ScrolledWindow()
        view = gtk.TreeView (element.document.data)
        element.present_widget.add_with_viewport (view)
        element.present_columns = []
        index = 0
        for c in element.document.columns:
            if c.label is not None:
                column = gtk.TreeViewColumn (c.label)
                view.append_column (column)
                element.present_columns.append (column)
                renderer = highgtk.cell.get_cell_renderer (c)
                column.pack_start (renderer, True)
                column.set_attributes (renderer, text=index)
                index = index + 1
        reorder = getattr (element.document, "reorder", None)
        if reorder is not None:
            view.set_reorderable (True)
        view.show()

def remove_table (element):
    widget = getattr (element, "present_widget", None)
    if widget is not None:
        del element.present_widget
        del element.present_columns
