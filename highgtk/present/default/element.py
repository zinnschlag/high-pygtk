
import gtk

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
        element.present_widget = gtk.TreeView (element.document.data)
        element.present_columns = []
        for c in element.document.columns:
            if c[1] is not None:
                column = gtk.TreeViewColumn (c[1])
                element.present_widget.append_column (column)
                element.present_columns.append (column)

def remove_table (element):
    widget = getattr (element, "present_widget", None)
    if widget is not None:
        del element.present_widget
        del element.present_columns
