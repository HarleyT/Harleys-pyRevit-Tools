#vbCr = "\r"
#vbLf = "\n"
#vbCrLf = "\r\n"

import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

clr.AddReference('System')
from System.Collections.Generic import List

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
uiapp = DocumentManager.Instance.CurrentUIApplication

viewSetName = IN[0]

mySheets = UnwrapElement(IN[1])

mySheetNumbers = [m.SheetNumber for m in mySheets]



#mySheetNumbers.extend(["S-11-110","S-11-111","S-70-141"])



myViewSet = ViewSet()

sheetItr = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()

selectedSheets = list()

for sheet in sheetItr:
	if sheet.SheetNumber in mySheetNumbers:
		#selectedSheets.append(sheet.SheetNumber)
		myViewSet.Insert(sheet)
elemItr = FilteredElementCollector(doc).OfClass(ViewSheetSet).GetElementIterator()

elemItr.Reset()

existingViewSet = None

while (elemItr.MoveNext()):
	if (elemItr.Current.Name == viewSetName):
		existingViewSet = elemItr.Current


hasBeenDeleted = "No"

TransactionManager.Instance.EnsureInTransaction(doc)

if existingViewSet != None:
	doc.Delete(existingViewSet.Id);
	hasBeenDeleted = "Yes"

printMan = doc.PrintManager;
printMan.PrintRange = PrintRange.Select;
viewSetting = printMan.ViewSheetSetting;
viewSetting.CurrentViewSheetSet.Views = myViewSet;
viewSetting.SaveAs(viewSetName);

TransactionManager.Instance.TransactionTaskDone()

TaskDialog.Show("Result", "ViewSet: %s  \nExisting: %s \nThe view set contains %s sheets." % (viewSetName,hasBeenDeleted, myViewSet.Size))

# From the Journal File: Jrn.RibbonEvent "Execute external command:CustomCtrl_%CustomCtrl_%CADtools%Publish%Batch" & vbCr & 
#"Publish:Arup.CADtools.Revit.Commands.RevitPublishCmd"
name = "CustomCtrl_%CustomCtrl_%CADtools%Publish%Batch\rPublish"

id = RevitCommandId.LookupCommandId(name)

uiapp.PostCommand( id )


OUT = "Success"