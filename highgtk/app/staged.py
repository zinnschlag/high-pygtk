"""Application with stage structure.

This module implements an application entity for application, that consist of several
distinct stages. This can be used thoughout the lifetime of the application, but is
primarily meant to handle a staged initialisation, i.e. an application, that requires a login
before the primary stage becomes accessable.


"""

import glib
import gtk

import highgtk.entity

class Stage:
    """A stage within a stages application."""

    def __init__ (self, name):
        self.name = name

    def run (self):
        """Start stage (making it the current stage)."""
        pass

    def stop (self):
        """Notify stage, that it is no longer the current stage."""
        pass

class Application (highgtk.entity.Application):
    """Stages application.

    Stages can be added by inserting them into self.stages. self.stages must not be
    changed anymore after run is called.
    After the last stage has been completed the applications shuts down.

    """

    def __init__ (self, name):
        highgtk.entity.Application.__init__ (self, name)
        self.stages = []
        self.stage = -1

    def advance (self, steps = 1):
        """Enter next stage.

        Enter the next stage, option skipping one or more stages. If there is no more stage,
        the application shuts down.
        It is possible to go one or more stages back instead by giving steps a negative value. Moving
        beyond the first stage will make the application shut down.
        Calling this function with steps==0 resets the current stage by calling stop and run.

        """
        self._exit_current()
        self.stage = self.stage + steps
        if self.stage<0 or self.stage>=len (self.stages):
            gtk.main_quit()
        else:
            self.stages[self.stage].run()

    def enter_stage (self, stage_name):
        """Enter a specific stage."""
        stage = get_stage (stage_name)
        self._exit_current()
        self.stage = self.stages (stage)
        self.stages[self.stage].run()

    def get_stage (self, stage_name):
        """Get stage by name."""
        for s in self.stages:
            if s.name==stage_name:
                return s
        raise Exception ("Unknown stage: " + stage_name)

    def _exit_current (self):
        if self.stage>=0 and self.stage < len (self.stages):
            self.stages[self.stage].stop()

    def _start (self):
        """Start the first stage."""
        self.advance()
        return False

    def run (self):
        """Run main loop and start first stage (blocks until application is qutting)."""
        glib.idle_add (self._start)
        highgtk.entity.Application.run (self)
