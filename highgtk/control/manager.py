"""This module defines interactions and a tree-structure to manage them """

import logging

import highgtk.present.current

log = logging.getLogger ("highgtk.control")

class Interaction:
    """The interaction brings together the front-end and the back-end of a control."""

    def __init__ (self, name, front, back, position = None):
        """Newly created interactions are enabled by default.

        front: an instance of a class defined in control.front
        back: any instance, that provides an execute method, or a callable object with
        either zero or one (entity) arguments

        """

        self.name = name
        self.front = front
        if hasattr (back, "__call__"):
            self.back = highgtk.control.back.Function (back)
        else:
            self.back = back
        self.position = position
        self.enabled = True

    def enable (self):
        """Enable interaction.

        This is a no-op, if the interaction is already enabled.
        """

        if not self.enabled:
            self.endabled = True

    def disable (self):
        """Disable interaction.

        This is a no-op, if the interaction is already disabled.
        """

        if self.enabled:
            self.endabled = False


class Group:
    """A collection of interactions and sub-groups."""

    def __init__ (self, name, front = None, position = None):
        self.name = name
        self.front = front
        self.position = position
        self.members = []

    def _remove (self, name, entity):
        """Remove group or interaction from this group or a subgroup.

        Returns True if an instance has been found and removed, False otherwise."""
        for i in self.members:
            if i.name==name:
                if hasattr (entity, "control") and entity.is_linked():
                    if isinstance (i, Interaction):
                        entity.presentation.remove_control_interaction (entity, i)
                    else:
                        entity.presentation.remove_control_group (entity, i)
                self.members.remove (i)
                return True
            elif isinstance (i, Group):
                if i._remove (name, entity):
                    return True

        return False

    def _search (self, name):

        for i in self.members:
            if i.name==name:
                return (i, [self.name, i.name])
            elif isinstance (i, Group):
                sub, path = i._search (name)
                if sub is not None:
                    path.insert (0, self.name)
                    return (sub, path)

        return (None, None)

    def _is_yours (self, group):

        if group==self:
            return True
        for i in self.members:
            if i._is_yours (group):
                return True
        return False


class ParentError (Exception):

    def __init__ (self, name, parent_name):
        self.name = name
        self.parent_name = parent_name

    def __str__ (self):
        return "Can't create %s with parent %s, because the parent is not a group" % (
            self.name, self.parent_name)


class NotFoundError (Exception):

    def __init__ (self, name):
        self.name = name

    def __str__ (self):
        return "Group or interaction %s not found" % self.name


class Root:
    """The root of the control-tree for a single entity.

    To add a control manager to an entity, add a Root to it with the name control. The
    control manager will only be recognised, if it is added, before the entity is added to
    a parent entity.
    Note: Not all types of entities do support control managers."""

    def __init__ (self, entity):
        self.top = Group ("")
        self.entity = entity
        self.create_group ("main", None, parent=self.top)
        self.presentation = highgtk.present.current.get()

    def create_group (self, name, front, parent = None, position = None):
        """Create a new group and return it.

        Name must be unique within the root.
        Parent can either be a Group instance that belongs to this root or a name.
        If no parent is given, the parent group "main" is assumed.
        If no position is given, the group is appended at the end. Else position must be
        an integer (larger positions are inserted after smaller positions)

        """

        group = Group (name, front, position=position)
        if not parent:
            parent = "main"
        self._add_to_parent (parent, group)
        return group

    def create_interaction (self, name, front, back, parent, position = None):
        """Create an interaction and return it.

        Name of the interaction must be unique within the root.
        Parent can either be a Group instance that belongs to this root or a name.
        If no position is given, the interaction is appended at the end. Else position must be
        an integer (larger positions are inserted after smaller positions).

        """

        interaction = Interaction (name, front, back, position=position)
        self._add_to_parent (parent, interaction)
        return interaction

    def remove (self, name):
        """Remove an interaction or group with the given name.

        If a group is removed, all sub-groups and interactions of this group are removed
        too."""

        if not self.top._remove (name, self.entity):
            raise NotFoundError (name)

    def get (self, name):
        """Return an interaction or group with the given name.

        Returns a pair:
        - the interaction or group
        - a list containing the ancestor groups of the interaction or group
        (starting with the root-most group)
        """

        instance, path = self._search (name)

        if not instance:
            raise NotFoundError (name)

        return (instance, path)

    def _search (self, name):

        return self.top._search (name)

    def _add_to_parent (self, parent, instance):
        if isinstance (parent, Group):
            path = None
            if not self.top._is_yours (parent):
                raise NotFoundError (parent.name)
        else:
            parent, path = self.get (parent)
        parent.members.append (instance)
        if hasattr (self.entity, "control") and self.entity.is_linked():
            path = self.get (parent.name)[1]
            if isinstance (instance, Interaction):
                self.entity.presentation.add_control_interaction (self.entity, path, instance)
            else:
                self.entity.presentation.add_control_group (self.entity, path, instance)
