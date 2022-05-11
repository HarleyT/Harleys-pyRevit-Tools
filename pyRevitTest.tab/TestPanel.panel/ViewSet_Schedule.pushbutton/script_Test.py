"""Creates print set from selected views."""

import clr
clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System')
clr.AddReferenceByPartialName('System.Windows.Forms')

from pyrevit import framework
from pyrevit import revit, DB, UI
from pyrevit import forms

from Autodesk.Revit import DB


sheetsetname = 'ViewPrintSet'

# Get printmanager / viewsheetsetting
printmanager = revit.doc.PrintManager
printmanager.PrintRange = DB.PrintRange.Select
viewsheetsetting = printmanager.ViewSheetSetting

viewsheets = []
viewsheetsets = DB.FilteredElementCollector(revit.doc)\
                    .OfClass(framework.get_type(DB.ViewSheetSet))\
                    .WhereElementIsNotElementType()\
                    .ToElements()

allviewsheetsets = {vss.Name: vss for vss in viewsheetsets}

print(allviewsheetsets)

for el in viewsheetsets:
    viewsheets.append(el)

#print(viewsheets)