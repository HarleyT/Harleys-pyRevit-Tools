from example import test_print
from Snippets._selection import get_selected_elements
from Snippets._selection import pick_elements_by_rect
from Snippets._selection import picked_object_single
from Snippets._selection import picked_object_multi
from Snippets._selection import picked_point
from Snippets._selection import picked_box
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter, PickBoxStyle
from Snippets._convert import convert_internal_units

# Variables
uidoc = __revit__.ActiveUIDocument              #type: UIDocument
# doc   = __revit__.ActiveUIDocument.Document     #type: Document


def GetManyRefByRectangle(doc):
    # ra = ReferenceArray()
    # selFilter = MassSelectionFilter()
    # eList = doc.Selection.PickElementsByRectangle(selFilter, "Select multiple faces")
    # return eList
    custom_filter = CustomFilter()
    selected_elements = selection.PickElementsByRectangle(custom_filter, "Select rooms ")
    print(selected_elements)

class MassSelectionFilter(ISelectionFilter):
    def AllowElement(self, element):
        if element.Category.Name == "Mass":
            return True
        return False

    def AllowReference(self, refer, point):
        return False

class CustomFilter(ISelectionFilter):

    def AllowElement(self, element):
        if element.Category.BuiltInCategory == BuiltInCategory.OST_Walls:
            return True

