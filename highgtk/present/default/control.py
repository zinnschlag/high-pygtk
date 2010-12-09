
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

def _add_action (view, instance):
    action = instance.front.make_action (instance.name)
    instance.present_action_group = gtk.ActionGroup (instance.name)
    view.present_ui.insert_action_group (instance.present_action_group)
    if instance.front.shortcut is None:
        instance.present_action_group.add_action (action)
    else:
        instance.present_action_group.add_action_with_accel (action, instance.front.shortcut)
    return action

def _add_group (view, group, path):
    for i in group.members:
        action = _add_action (view, i)
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
        view.present_ui.add_ui (merge_id, '/', 'main', '', gtk.UI_MANAGER_MENUBAR, False)
        view.present_layout.pack_start (view.present_ui.get_widget ("/main"), False, False)
        main = manager.get ("main")[0]
        _add_group (view, main, '/main')

def remove_interaction (view, interaction):
    view.present_ui.remove_ui (interaction.present_merge_id)
    view.present_ui.remove_action_group (interaction.present_action_group)
    del interaction.present_action_group

def add_interaction (view, path, interaction):
    action = _add_action (view, interaction)
    interaction.present_merge_id = view.present_ui.new_merge_id()
    path = '/' + '/'.join ([e for e in path[1:]])
    view.present_ui.add_ui (interaction.present_merge_id, path, interaction.name,
        interaction.name, gtk.UI_MANAGER_MENUITEM, False)
    back = getattr (interaction, "back", None)
    if back is not None:
        action.connect ("activate", execute, back, view)
    else:
        log.error ("no back-end for action %s in %s" % (interaction.name, path))
