"""Data -> gtk treeview cell mapping."""

import gtk

import highgtk.data

def get_type (data):
    if isinstance (data, highgtk.data.Text):
        return str
    raise Exception ("Unsupported data type in cell (model)")

def get_cell_renderer (data):
    if isinstance (data, highgtk.data.Text):
        return gtk.CellRendererText()
    raise Exception ("Unsupported data type in cell (view)")
