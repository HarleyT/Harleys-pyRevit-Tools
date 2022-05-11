import clr

from pyrevit import framework
from pyrevit import revit, DB, UI
from pyrevit import forms

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

from Autodesk.Revit.UI import *

from System.Collections.Generic import List

from rpw.ui.forms import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

cl = FilteredElementCollector(doc).OfClass(ViewSheetSet).ToElements()

print(len(cl))

print("stuff")

for el in cl:
    print(el)
