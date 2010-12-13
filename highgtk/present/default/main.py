"""Default presentation."""

import gtk

import highgtk.entity
import highgtk.present.default.inquiry
import highgtk.present.default.report
import highgtk.present.default.view
import highgtk.present.default.element

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

    def add_view (self, view):
        """Add presentation to view."""
        highgtk.present.default.view.add (view)

    def show_view (self, view):
        """Present view to user"""
        highgtk.present.default.view.show (view)

    def remove_view (self, view):
        """Remove presentation from view."""
        highgtk.present.default.view.remove (view)

    def show_element (self, view_element):
        """Present element to user."""
        view_element.present_widget.show()

    def add_element_text (self, view_element):
        """Add presentation for text element to view_element."""
        highgtk.present.default.element.add_text (view_element)

    def remove_element_text (self, view_element):
        """Remove presentation from view_element."""
        highgtk.present.default.element.remove_text (view_element)

    def add_element_table (self, view_element):
        """Add presentation for table element to view element."""
        highgtk.present.default.element.add_table (view_element)

    def remove_element_table (self, view_element):
        """Remove presentation from view element."""
        highgtk.present.default.element.remove_table (view_element)

    def add_element_to_view (self, view, view_element):
        """Add view element to view.

        Adding an element that has already been added is a no-op.

        """
        child = view_element.present_widget
        children = view.present_window.get_children()
        if not children or children[0]!=child:
            view.present_layout.pack_start (child)

    def remove_element_from_view (self, view, view_element):
        """Remove view element from view.

        Removing an element that does not belong to view is a no-op.

        """
        child = view_element.present_widget
        children = view.present_window.get_children()
        if child in children:
            view.present_layout.remove (child)

    def remove_control_interaction (self, view, interaction):
        """Remove an interaction from a linked view."""

        highgtk.present.default.control.remove_interaction (view, interaction)

    def remove_control_group (self, view, group):
        """Remove a group from a linked view."""

        highgtk.present.default.control.remove_group (view, group)

    def add_control_interaction (self, view, path, interaction):
        "Adding an interaction to a linked view."

        highgtk.present.default.control.add_interaction (view, path, interaction)

    def add_control_group (self, view, path, group):
        "Adding a group to a linked view."

        highgtk.present.default.control.add_group (view, path, group)
