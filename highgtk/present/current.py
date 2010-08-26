"""
"""

import highgtk.present.default.main

presentation = None

def get():
    global presentation
    if presentation is None:
        presentation = highgtk.present.default.main.Presentation()
    return presentation
