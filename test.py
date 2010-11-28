#!/usr/bin/env python

import logging

import highgtk.app.staged
import highgtk.element.text
import highgtk.element.table
import highgtk.entity
import highgtk.data
import highgtk.constraint
import highgtk.control.manager
import highgtk.control.front
import highgtk.control.back

def test_execute():
    print "execute"

class TestStage (highgtk.app.staged.Stage):

    def __init__ (self, app):
        highgtk.app.staged.Stage.__init__ (self, app, "Stage 1")
        self.group = highgtk.entity.DocumentGroup (primary=True)

    def _quit_ok (self, inquiry, results):
        print results

    def _quit_cancel (self, inquiry):
        self.application.advance()

    def run (self):
        self.add (self.group)
        self._setup_text()
        self._setup_table()
        self._setup_inquiry()

    def _setup_inquiry (self):
        data = (
            ( highgtk.data.Text ("id1", "Some text"), [ highgtk.constraint.Min (3) ] ),
            ( highgtk.data.Text ("id2", "Some other text"), None ),
            ( highgtk.data.HiddenText ("id3", "hidden text"), [ highgtk.constraint.Equal ("id2") ] ),
            ( highgtk.data.Boolean ("id3", "an option"), None )
            )
        self.inquiry = highgtk.entity.Inquiry (data)
        self.inquiry.title = "Some Input, please!"
        self.inquiry.ok_method = "_quit_ok"
        self.inquiry.cancel_method = "_quit_cancel"
        self.add (self.inquiry)

    def _setup_text (self):
        self.document = highgtk.entity.Document()
        self.group.add (self.document)
        self.view = highgtk.entity.View()
        self.document.add (self.view)
        self.textdocument = highgtk.element.text.DocumentElement()
        self.document.add (self.textdocument)
        self.textview = highgtk.element.text.ViewElement (self.textdocument)
        self.view.add (self.textview)

    def _setup_table (self):
        self.document2 = highgtk.entity.Document()
        self.group.add (self.document2)
        self.view2 = highgtk.entity.View()
        self.view2.control = highgtk.control.manager.Root (self.view2)
        self.view2.control.create_group ("test", highgtk.control.front.Custom ("Test"))
        self.view2.control.create_interaction ("test2", highgtk.control.front.Custom ("Test2"),
            highgtk.control.back.Function (test_execute), parent="test")
        self.view2.control.create_group ("test3", highgtk.control.front.Custom ("Test3"),
            parent="test")
        self.view2.control.create_interaction ("test4", highgtk.control.front.Custom ("Test4"),
            highgtk.control.back.Function (test_execute), parent="test3")
        self.document2.add (self.view2)
        columns = ( highgtk.data.Text ("+ID", "text1"), highgtk.data.Boolean ("id2", "Option") )
        self.tabledocument = highgtk.element.table.OrderedDocumentElement (columns)
        self.tabledocument.reorder = 0
        content = (
            ('some text', True ), ('more text', False ), ('and then some more', True ) )
        content2 = (
            ('some text2', True ), ('more text', False ), ('and then some more', True ) )
        self.tabledocument.update (content)
        self.tabledocument.update (content2)
        self.document2.add (self.tabledocument)
        self.tableview = highgtk.element.table.ViewElement (self.tabledocument)
        self.tableview.search = "+ID"
        self.view2.add (self.tableview)


if __name__=="__main__":
    logging.basicConfig (level=logging.INFO)
    app = highgtk.app.staged.Application ("Test")
    app.stages.append (TestStage (app))
    app.run()
