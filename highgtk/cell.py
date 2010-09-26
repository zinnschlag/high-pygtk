"""Data -> gtk treeview cell mapping."""

import highgtk.data

def get_type (data):
    if isinstance (data, highgtk.data.Text):
        return str
    raise Exception ("Unsupported data type in cell (model)")
