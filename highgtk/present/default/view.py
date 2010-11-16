
import gtk

def add (view):
    window = getattr (view, "present_window", None)
    if window is None:
        view.present_window = gtk.Window()
        title = view.get_title()
        view.present_window.set_title (title)
        view.present_window.connect ("delete_event", delete_event, view)
        view.present_layout = gtk.VBox()
        view.present_window.add (view.present_layout)

def show (view):
    if getattr (view, "present_shown", None) is not None:
        view.present_window.present()
    else:
        view.present_window.show_all()
        view.present_shown = True

def remove (view):
    window = getattr (view, "present_window", None)
    if window is not None:
        window.hide()
        del view.present_window
        del view.present_layout
        if getattr (view, "present_shown", None) is not None:
            del view.present_shown

def delete_event (widget, event, view):
    close_request = getattr (view, "close_request", None)
    if close_request is None:
        return False
    close_request()
    return True
