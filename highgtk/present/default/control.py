
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

def _add_group (view, group, path, merge_id):
    for i in group.members:
        action = i.front.make_action (i.name)
        if i.front.shortcut is None:
            view.present_action_group.add_action (action)
        else:
            view.present_action_group.add_action_with_accel (action, i.front.shortcut)
        if isinstance (i, highgtk.control.manager.Group):
            view.present_ui.add_ui (merge_id, path, i.name, i.name, gtk.UI_MANAGER_MENU,
                False)
            _add_group (view, i, path + "/" + i.name, merge_id)
        else:
            view.present_ui.add_ui (merge_id, path, i.name, i.name, gtk.UI_MANAGER_MENUITEM,
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
        _add_group (view, main, '/MenuBar', merge_id)
