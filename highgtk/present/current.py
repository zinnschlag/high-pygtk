"""Presentation selection.
"""

import logging

import highgtk.present.default.main

presentation = None

def get():
    global presentation
    if presentation is None:
        log = logging.getLogger ("highgtk.presentation")
        log.info ("Automatically selecting default presentation")
        presentation = highgtk.present.default.main.Presentation()
    return presentation
