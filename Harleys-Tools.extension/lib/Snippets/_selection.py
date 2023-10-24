# -*- coding: utf-8 -*-
"""Get Selected Elements

Returns:
    Element ID of items in selection.
"""

# Imports
from Autodesk.Revit.DB import *

# Variables
uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document

selection = uidoc.Selection

# Functions
def get_selected_elements(uidoc):
    """Function to get selected elements in Revit UI."""
    doc = uidoc.Document
    return [doc.GetElement(e_id) for e_id in selection.GetElementIds()]
