
import gtk

import highgtk.entity
import highgtk.present.default.layout

def add (inquiry):
    window = getattr (inquiry, "present_window", None)
    if window is None:
        inquiry.present_window = gtk.Dialog()
        title = getattr (inquiry, "title", None)
        if title is None:
            root = highgtk.entity.get_root (inquiry)
            title = "Inquiry from %s" % root.name
        inquiry.present_window.add_button (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        ok_text = getattr (inquiry, "ok_text", gtk.STOCK_OK)
        inquiry.present_window.add_button (ok_text, gtk.RESPONSE_OK)
        inquiry.present_window.set_default_response (gtk.RESPONSE_OK)
        inquiry.present_window.connect ("response", response, inquiry)
        inquiry.present_window.connect ("delete_event", delete_event, inquiry)
        inquiry.present_window.set_title (title)
        inquiry.present_window.set_position (gtk.WIN_POS_CENTER)
        inquiry.present_layout = highgtk.present.default.layout.get_layout (inquiry.data)
        inquiry.present_layout.build (inquiry.present_window.get_content_area())
        inquiry.present_report = gtk.Label()
        inquiry.present_report.set_line_wrap (True)
        inquiry.present_report.set_alignment (0.0, 0.5)
        inquiry.present_window.get_content_area().pack_end (inquiry.present_report)
        inquiry.present_window.show_all()
    else:
        window.present()

def remove (inquiry):
    window = getattr (inquiry, "present_window", None)
    if window is not None:
        window.hide()
        del inquiry.present_window

def cancel (inquiry):
    method_name = getattr (inquiry, "cancel_method", None)
    if method_name is not None:
        method = getattr (inquiry.parent, method_name)
        method (inquiry)
    inquiry.remove (inquiry)

def okay (inquiry):
    method_name = getattr (inquiry, "ok_method", "inquiry_okay")
    error = inquiry.present_layout.get_error()
    if error is not None:
        inquiry.error_report.primary = error
        inquiry.add (inquiry.error_report)
    else:
        method = getattr (inquiry.parent, method_name)
        method (inquiry, inquiry.present_layout.get_data())
        inquiry.remove (inquiry)

def response (widget, response_id, inquiry):
    if response_id==gtk.RESPONSE_OK:
        okay (inquiry)
    elif response_id==gtk.RESPONSE_CANCEL:
        cancel (inquiry)
    return True

def delete_event (widget, event, inquiry):
    cancel (inquiry)
    return True
