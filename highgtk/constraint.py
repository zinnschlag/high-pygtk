"""Constraints for data entries."""

import highgtk.data

class Constraint:
    """Constraints base class."""

    def get_error (self, data, result, entry):
        """Return error string or None.

        data: list of entry/constraints-list pairs
        result: dictionary of result values indexed by ID.

        enty_: entry to be bound by constraint
        """
        return None

    def configure (self, data, widget, entry):
        """Configure widget according to constraint.

        data: list of entry/constraints-list pairs
        entry: entry to be bound by constraint
        """
        pass

class Min (Constraint):
    """Minimum constraint.

    Text: length of string

    """

    def __init__ (self, limit, message = None):
        self.limit = limit
        self.message = message

    def get_error (self, data, result, entry):
        """Return error string or None.

        data: list of entry/constraints-list pairs
        result: dictionary of result values indexed by ID.
        entry: ID of data entry to be bound by constraint

        """
        if isinstance (entry, highgtk.data.Text):
            if len (result[entry.id_])<self.limit:
                if self.message is None:
                    return "%s must be at least %s characters long" % (entry.label, self.limit)
                else:
                    return self.message
        return None
