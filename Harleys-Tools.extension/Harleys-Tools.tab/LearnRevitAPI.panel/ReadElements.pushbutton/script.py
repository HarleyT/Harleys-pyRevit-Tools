
import sys
from Autodesk.Revit.UI.Selection    import ObjectType, Selection
from Autodesk.Revit.DB              import *

# Variables
uidoc = __revit__.ActiveUIDocument              #type: UIDocument
doc = uidoc.Document
selection = uidoc.Selection                     #type: Selection
fam_type = FamilyInstance                       #type: FamInstance

# Pick an Element
ref = selection.PickObject(ObjectType.Element)
elem = doc.GetElement(ref)
# print(elem.StructuralType)

# Check if that's a Column
if str(elem.StructuralType) != "Column":
    print("This is not a Column selected. Please Try Again.")
    sys.exit()

print(elem)