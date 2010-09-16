
import gtk

def add_text (element):
    widget = getattr (element, "present_widget", None)
    if widget is None:
        element.present_widget = gtk.TextView (element.document.data)

def remove_text (element):
    widget = getattr (element, "present_widget", None)
    if widget is not None:
        del element.present_widget
