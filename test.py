#!/usr/bin/env python

import highgtk.app.staged
import highgtk.entity
import highgtk.data
import highgtk.constraint

class TestStage (highgtk.app.staged.Stage):

    def __init__ (self, app):
        highgtk.app.staged.Stage.__init__ (self, app, "Stage 1")
        data = (
            ( highgtk.data.Text ("id1", "Some text"), [ highgtk.constraint.Min (3) ] ),
            ( highgtk.data.Text ("id2", "Some other text"), None ),
            ( highgtk.data.HiddenText ("id3", "hidden text"), [ highgtk.constraint.Equal ("id2") ] )
            )
        self.inquiry = highgtk.entity.Inquiry (data)
        self.inquiry.title = "Some Input, please!"
        self.inquiry.ok_method = "_quit_ok"
        self.inquiry.cancel_method = "_quit_cancel"

    def _quit_ok (self, inquiry, results):
        print results
        self.application.advance()

    def _quit_cancel (self, inquiry):
        self.application.advance()

    def run (self):
        self.add (self.inquiry)

if __name__=="__main__":
    app = highgtk.app.staged.Application ("Test")
    app.stages.append (TestStage (app))
    app.run()
