
import logging
import inspect

import gtk

import highgtk.control

log = logging.getLogger ("highgtk.present")

def execute (widget, back, entity):
    if len (inspect.getargspec (back.execute)[0])==1:
        back.execute()
    else:
        back.execute (entity)

def _add_group (view, group, path):
    for i in group.members:
        action = i.front.make_action (i.name)
        i.present_action_group = gtk.ActionGroup (i.name)
        view.present_ui.insert_action_group (i.present_action_group)
        if i.front.shortcut is None:
            i.present_action_group.add_action (action)
        else:
            i.present_action_group.add_action_with_accel (action, i.front.shortcut)
        i.present_merge_id = view.present_ui.new_merge_id()
        if isinstance (i, highgtk.control.manager.Group):
            view.present_ui.add_ui (i.present_merge_id, path, i.name, i.name, gtk.UI_MANAGER_MENU,
                False)
            _add_group (view, i, path + "/" + i.name)
        else:
            view.present_ui.add_ui (i.present_merge_id, path, i.name, i.name, gtk.UI_MANAGER_MENUITEM,
                False)
            back = getattr (i, "back", None)
            if back is not None:
                action.connect ("activate", execute, back, view)
            else:
                log.error ("no back-end for action %s in %s" % (i.name, path))

def add_control (view):
    manager = getattr (view, "control", None)
    if manager is not None:
        view.present_ui = gtk.UIManager()
        view.present_action_group = gtk.ActionGroup ("main")
        view.present_ui.insert_action_group (view.present_action_group)
        merge_id = view.present_ui.new_merge_id()
        view.present_ui.add_ui (merge_id, '/', 'MenuBar', '', gtk.UI_MANAGER_MENUBAR, False)
        view.present_layout.pack_start (view.present_ui.get_widget ("/MenuBar"), False, False)
        main = manager.get ("main")
        _add_group (view, main, '/MenuBar')

def remove_interaction (view, interaction):
    view.present_ui.remove_ui (interaction.present_merge_id)
    view.present_ui.remove_action_group (interaction.present_action_group)
    del interaction.present_action_group
