# -*- coding: utf-8 -*-
__title__ = "xaml Test"
__author__ = "Harley Trappitt"
__doc__ = """Version = 1.0
Date    = 14.12.2023
_____________________________________________________________________
Description:

Testing setups to find a workable template for my wpf forms.
_____________________________________________________________________
Last update:
-

_____________________________________________________________________
"""






#______________________________ IMPORTS
import sys
from Autodesk.Revit.DB import (FilteredElementCollector,
                               BuiltInParameter,
                               BuiltInCategory,
                               ViewSheet,
                               Transaction)
from pyrevit.forms import SelectFromList
from pyrevit import forms

# .NET IMPORTS
import clr
from clr import AddReference
AddReference("System")
from System.Diagnostics.Process import Start
from System.Windows.Window import DragMove
from System.Windows.Input import MouseButtonState

# VARIABLES
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application



# FUNCTIONS
# from Snippets._selection import get_selected_sheets


def say_hello(name):
    """Function to do something"""
    forms.ask_for_string(
        default='pyRevit',
        prompt='Enter Name:',
        title=__title__
    )
    # UI.TaskDialog.Show(
    #     "Hello World",
    #     "Hello {}".format(name or "World!"),
    #     )

class MyWindow(forms.WPFWindow):
    """GUI"""
    def __init__(self, xaml_file_name):
        self.form = forms.WPFWindow.__init__(self, xaml_file_name)
        self.main_title.Text = __title__

    @property
    def name(self):
        return self.input_name.Text




    # GUI EVENT HANDLERS:
    def button_close(self,sender,e):
        """Stop application by clicking on a <Close> button in the top right corner."""
        self.Close()

    def Hyperlink_RequestNavigate(self, sender, e):
        """Forwarding for a Hyperlink"""
        Start(e.Uri.AbsoluteUri)

    def header_drag(self,sender,e):
        """Drag window by holding LeftButton on the header."""
        if e.LeftButton == MouseButtonState.Pressed:
            DragMove(self)
    def button_run(self, sender, e):
        """Button action: Do a thing """
        say_hello(self.name)
        self.Close()


if __name__ == '__main__':
    do_a_thing = True
    t = Transaction(doc, __title__)
    t.Start()
    if do_a_thing:
        MyWindow("ui.xaml").ShowDialog()
    t.Commit()