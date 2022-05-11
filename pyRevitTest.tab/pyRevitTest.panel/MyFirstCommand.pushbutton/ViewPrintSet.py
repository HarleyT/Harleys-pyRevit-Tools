import clr

from pyrevit import framework
from pyrevit import revit, DB, UI
from pyrevit import forms

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

from Autodesk.Revit.UI import *

from System.Collections.Generic import List

from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                          Separator, Button, CheckBox)

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

sheetsetname = 'ViewPrintSet'

# Get printmanager / viewsheetsetting
printmanager = revit.doc.PrintManager
printmanager.PrintRange = DB.PrintRange.Select
viewsheetsetting = printmanager.ViewSheetSetting

# Collect selected views
selected_views = forms.select_views(use_selection=True)
if selected_views:
    myviewset = DB.ViewSet()
    for el in selected_views:
        myviewset.Insert(el)

    if myviewset.IsEmpty:
        forms.alert('At least one view must be selected.')
    else:
        # Collect existing sheet sets
        viewsheetsets = DB.FilteredElementCollector(revit.doc)\
                          .OfClass(framework.get_type(DB.ViewSheetSet))\
                          .WhereElementIsNotElementType()\
                          .ToElements()

        allviewsheetsets = {vss.Name: vss for vss in viewsheetsets}

        with revit.Transaction('Created Print Set'):
            # Delete existing matching sheet set
            if sheetsetname in allviewsheetsets.keys():
                viewsheetsetting.CurrentViewSheetSet = \
                    allviewsheetsets[sheetsetname]
                viewsheetsetting.Delete()

            # Create new sheet set
            viewsheetsetting.CurrentViewSheetSet.Views = myviewset
            viewsheetsetting.SaveAs(sheetsetname)