from example import test_print
from Snippets._selection import get_selected_elements

# Variables
uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document


# Test Print
test_print()

# Get Selected Elements
selected_elements = get_selected_elements(uidoc)
print(selected_elements)