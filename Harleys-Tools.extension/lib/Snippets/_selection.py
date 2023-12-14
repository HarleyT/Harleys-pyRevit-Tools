# -*- coding: utf-8 -*-
"""Get Selected Elements
"""

# Imports
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter, Selection

# Variables
uidoc = __revit__.ActiveUIDocument          #type: UIDocument
doc = __revit__.ActiveUIDocument.Document   #type: Document
selection = uidoc.Selection                 #type: Selection


# Functions
def get_selected_elements(uidoc):
    """Function to get selected elements in Revit UI."""
    doc = uidoc.Document
    return [doc.GetElement(e_id) for e_id in selection.GetElementIds()]



# ISelectionFilter
class ISelectionFilter_Classes(ISelectionFilter):
    def __init__(self, allowed_types):
        """ ISelectionFilter made to filter with types
        :param allowed_types: list of allowed types
        """
        self.allowed_types = allowed_types

    def AllowElement(self, element):
        if type(element) in self.allowed_types:
            return True

class ISelectionFilter_Categories(ISelectionFilter):
    def __init__(self, allowed_categories):
        """ ISelectionFilter made to filter with types
        :param allowed_categories: list of allowed types
        """
        self.allowed_categories = allowed_categories

    def AllowElement(self, element):
        if element.Category.BuiltInCategory in self.allowed_categories:
            return True