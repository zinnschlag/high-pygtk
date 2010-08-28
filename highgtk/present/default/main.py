"""Default presentation."""

import gtk

import highgtk.entity
import highgtk.present.default.inquiry
import highgtk.present.default.report

class Presentation:

    def terminate (self, entity, error):
        """Terminate application with a fatal error."""
        entity = highgtk.entity.get_root (entity)
        message = gtk.MessageDialog (type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            message_format="Terminating application " + entity.name)
        message.format_secondary_text ("Reason: " + error)
        message.show()
        message.run()
        gtk.main_quit()

    def add_inquiry (self, inquiry):
        """Add presentation to inquiry."""
        highgtk.present.default.inquiry.add (inquiry)

    def remove_inquiry (self, inquiry):
        """Remove presentation from inquiry."""
        highgtk.present.default.inquiry.remove (inquiry)

    def add_report (self, report):
        """Add presentation to report."""
        highgtk.present.default.report.add (report)

    def remove_report (self, report):
        """Remove presentation from report."""
        highgtk.present.default.report.remove (report)
