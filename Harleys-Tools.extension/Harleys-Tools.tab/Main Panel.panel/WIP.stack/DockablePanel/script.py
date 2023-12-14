# -*- coding: utf-8 -*-
__title__ = "Dockable\nPanel"                           # Name of the button displayed in Revit UI
"""
_____________________________________________________________________
Description:
Opens a dockable panel

_____________________________________________________________________
Author: Harley Trappitt"""                          # Button Description shown in Revit UI

__context__ = 'zero-doc'


from pyrevit import forms


test_panel_uuid = "3110e336-f81c-4927-87da-4e0d30d4d64b"

forms.open_dockable_panel(test_panel_uuid)
