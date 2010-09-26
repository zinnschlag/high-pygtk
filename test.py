#!/usr/bin/env python

import logging

import highgtk.app.staged
import highgtk.element.text
import highgtk.element.table
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
        self.group = highgtk.entity.DocumentGroup (primary=True)
        self.document = highgtk.entity.Document()
        self.document2 = highgtk.entity.Document()

    def _quit_ok (self, inquiry, results):
        print results

    def _quit_cancel (self, inquiry):
        self.application.advance()

    def run (self):
        self.add (self.inquiry)
        self.add (self.group)
        self.group.add (self.document)
        self.group.add (self.document2)
        self.view = highgtk.entity.View()
        self.document.add (self.view)
        self.textdocument = highgtk.element.text.DocumentElement()
        self.document.add (self.textdocument)
        self.textview = highgtk.element.text.ViewElement (self.textdocument)
        self.view.add (self.textview)
        self.view2 = highgtk.entity.View()
        self.document2.add (self.view2)
        columns = ( highgtk.data.Text ("id1", "text1"), )
        self.tabledocument = highgtk.element.table.OrderedDocumentElement (columns)
        self.tabledocument.data.append (None, ('some text',) )
        self.document2.add (self.tabledocument)
        self.tableview = highgtk.element.table.ViewElement (self.tabledocument)
        self.view2.add (self.tableview)

if __name__=="__main__":
    logging.basicConfig (level=logging.INFO)
    app = highgtk.app.staged.Application ("Test")
    app.stages.append (TestStage (app))
    app.run()
