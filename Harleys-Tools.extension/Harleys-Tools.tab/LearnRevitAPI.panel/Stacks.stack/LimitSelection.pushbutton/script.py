from Autodesk.Revit.DB                  import *
from Autodesk.Revit.UI.Selection        import ObjectType, ISelectionFilter, Selection
from Snippets._selection                import ISelectionFilter_Classes, ISelectionFilter_Categories
from Snippets._convert                  import convert_internal_units

import clr
clr.AddReference("System")

# Variables
uidoc = __revit__.ActiveUIDocument              #type: UIDocument
doc = uidoc.Document
selection = uidoc.Selection                     #type: Selection



# filter_classes = ISelectionFilter_Classes([Wall, Floor])
# selected_elements = selection.PickObjects(ObjectType.Element, filter_classes)
# for ref in selected_elements:
#     el = doc.GetElement(ref)
#     print(el)


filter_cat = ISelectionFilter_Categories([BuiltInCategory.OST_StructuralColumns,
                                          BuiltInCategory.OST_StructuralFraming])
selected_elements = selection.PickObjects(ObjectType.Element, filter_cat)
for ref in selected_elements:
    el = doc.GetElement(ref)
    print("Element Type: {}".format(el) + "\n"
          "Element Name: {}".format(el.Name))