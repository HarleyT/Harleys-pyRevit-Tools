from example import test_print
from Snippets._selection import get_selected_elements
from Snippets._selection import pick_elements_by_rect
from Snippets._selection import picked_object_single
from Snippets._selection import picked_object_multi
from Snippets._selection import picked_point
from Snippets._selection import picked_box
from Autodesk.Revit.DB import *

# Variables
uidoc = __revit__.ActiveUIDocument              #type: UIDocument
# doc   = __revit__.ActiveUIDocument.Document     #type: Document


# Test Print
# test_print()

# Get Selected Elements in view
# selected_elements = get_selected_elements(uidoc)
# print(selected_elements)

# Get Selected Elements in view by Rectangle Selection
rect_selection = pick_elements_by_rect()
print(rect_selection)

# Get Picked Objects in view, Single
# pick_s = picked_object_single(uidoc)
# print(pick_s)

# Get Picked Objects in view, Multiple
# pick_m = picked_object_multi(uidoc)
# print(pick_m)

# Get Picked Point
# pick_p = picked_point(uidoc)
# print(pick_p)

# Get Pick Box
# pick_box = picked_box(uidoc)
# print(pick_box)