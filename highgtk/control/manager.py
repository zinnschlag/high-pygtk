"""This module defines interactions and a tree-structure to manage them """

import highgtk.present.current


class Interaction:
    """The interaction brings together the front-end and the back-end of a control."""

    def __init__ (self, name, front, back):
        """Newly created interactions are enabled by default.

        front: an instance of a class defined in control.front
        back: any instance, that provides a invoke method

        """

        self.name = name
        self.front = front
        self.back = back
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

    def __init__ (self, name, front = None, semantics = None):
        self.name = name
        self.front = front
        self.semantics = semantics
        self.members = []

    def _remove (self, name, entity):
        """Remove group or interaction from this group or a subgroup.

        Returns True if an instance has been found and removed, False otherwise."""
        for i in self.members:
            if i.name==name:
                if hasattr (entity, "control") and entity.is_linked():
                    if isinstance (i, Interaction):
                        entity.presentation.remove_control_interaction (i)
                    else:
                        entity.presentation.remove_control_group (i)
                self.members.remove (i)
                return True
            elif isinstance (i, Group):
                if i._remove (name, entity):
                    return True

        return False

    def _search (self, name):

        for i in self.members:
            if i.name==name:
                return i
            elif isinstance (i, Group):
                sub = i._search (name)
                if sub is not None:
                    return sub

        return None

    def _is_yours (self, group):

        if group==self:
            return True
        for i in self.members:
            if i._is_yours (group):
                return True
        return False


class CreationError (Exception):

    def __init__ (self, name):
        self.name = name

    def __str__ (self):
        return "Data insufficient to place %s into the control tree" % self.name


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
        self.create_group ("main", None, parent=self.top)
        self.entity = entity
        self.presentation = highgtk.present.current.get()

    def create_group (self, name, front, semantics = None, parent = None):
        """Create a new group and return it.

        Name must be unique within the root.
        Must have either semantics or parent or neither one, but not both.
        Parent can either be a Group instance that belongs to this root or a name.
        If semantics is given and there is already a group with similar semantics, the
        pre-existing group is returned. In this case the name of the group is not
        guaranteed to match the name argument.
        If neither semantics nor parent are given, the parent group "main" is assumed.

        """

        if semantics and not parent:
            pass #TODO
        elif not semantics and parent:
            self._add_to_parent (parent, Group (name, front))
        elif not semantics and not parent:
            self._add_to_parent (self.get ("main"), Group (name, front))
        else:
            raise CreationError (name)

    def create_interaction (self, name, front, back, semantics = None, parent = None):
        """Create an interaction and return it.

        Name of the interaction must be unique within the root.
        Must have either semantics or parent.
        Parent can either be a Group instance that belongs to this root or a name.

        """

        if semantics and not parent:
            pass #TODO
        elif not semantics and parent:
            self._add_to_parent (parent, Interaction (name, front, back))
        else:
            raise CreationError (name)

    def remove (self, name):
        """Remove an interaction or group with the given name.

        If a group is removed, all sub-groups and interactions of this group are removed
        too."""

        if not self.top._remove (name, self.entity):
            raise NotFoundError (name)

    def get (self, name):
        """Return an interaction or group with the given name."""

        instance = self._search (name)

        if not instance:
            raise NotFoundError (name)

        return instance

    def _search (self, name):

        return self.top._search (name)

    def _add_to_parent (self, parent, instance):
        if isinstance (parent, Group):
            if not self.top._is_yours (parent):
                raise NotFoundError (parent.name)
        else:
            parent = self.get (parent)
        parent.members.append (instance)
