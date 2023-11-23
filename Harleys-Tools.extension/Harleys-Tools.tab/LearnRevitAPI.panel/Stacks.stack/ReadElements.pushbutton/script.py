
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

# Column variables
level_id = elem.LevelId
level    = doc.GetElement(level_id)
group = "None" if elem.GroupId == ElementId(-1) else elem.GroupId
# room_name  = elem.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() # Option A (Just RoomName)
# room_name_ = Element.Name.GetValue(elem)

# Print statements
print("ElementId: {}        ".format(elem.Id))
print("GroupId: {}          ".format(group))
print("Category: {}         ".format(elem.Category.Name))
print("BuiltInCategory: {}  ".format(elem.Category.BuiltInCategory))
print("Level: {}            ".format(level.Name))
print("XYZ: {}              ".format(elem.Location.Point))
print("Element Name: {}     ".format(Element.Name.GetValue(elem)))

# OriginalGeometry
opts                = Options()
og_geom = elem.GetOriginalGeometry(opts)
print("Original Geometry: {}".format(og_geom))

# Boundary Segments
# opts              = GeometryElement()
# geometry_element = elem.get_Geometry(opts)
# print("Geometry Element: {}".format(geometry_element))