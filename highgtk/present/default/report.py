
import gtk

def add (report):
    window = getattr (report, "present_window", None)
    if window is None:
        parent = getattr (report.parent, "present_report", None)
        if parent:
            prefix = ""
            if report.type=="warning":
                prefix = "Warning: "
            elif report.type=="error":
                prefix = "Error: "
            if report.secondary is None:
                parent.set_text ("%s%s" % (prefix, report.primary))
            else:
                parent.set_text ("%s%s (%s)" % (prefix, report.primary, report.secondary))
        else:
            type_ = None
            if report.type=="info":
                type_ = gtk.MESSAGE_INFO
            elif report.type=="warning":
                type_ = gtk.MESSAGE_WARNING
            elif report.type=="error":
                type_ = gtk.MESSAGE_ERROR
            else:
                raise Exception ("Unknown message type: %s" % report.type)
            report.present_window = gtk.MessageDialog (type=type_, message_format=report.primary)
            if report.secondary is not None:
                report.present_window.format_secondary_text (report.secondary)
            report.present_window.add_button (gtk.STOCK_OK, gtk.RESPONSE_OK)
            report.present_window.set_default_response (gtk.RESPONSE_OK)
            report.present_window.connect ("response", close, report)
            report.present_window.connect ("delete_event", close, report)
            report.present_window.set_position (gtk.WIN_POS_CENTER)
            report.present_window.show_all()
    else:
        window.present()

def remove (report):
    window = getattr (report, "present_window", None)
    if window is not None:
        window.hide()
        del inquiry.present_window
    else:
        parent = getattr (report.parent, "present_report")
        if parent:
            parent.set_text ("")

def close (widget, dummy, report):
    report.remove()
