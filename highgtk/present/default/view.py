
import gtk

def add (view):
    window = getattr (view, "present_window", None)
    if window is None:
        view.present_window = gtk.Window()
        title = view.get_title()
        view.present_window.set_title (title)
        view.present_window.connect ("delete_event", delete_event, view)
        view.present_window.show_all()
    else:
        window.present()

def remove (view):
    window = getattr (view, "present_window", None)
    if window is not None:
        window.hide()
        del view.present_window

def delete_event (widget, event, view):
    close_request = getattr (view, "close_request", None)
    if close_request is None:
        return False
    close_request()
    return True
