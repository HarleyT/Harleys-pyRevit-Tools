"""Sets the Schedule Sheet Number to all of the Elements that appear on the Schedule"""
__title__ = 'Set Sched No\nTo Items On\nSchedule'

#import libraries and reference the RevitAPI and RevitAPIUI

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.UI import *

import clr
# clr.AddReferenceByName("PresentationFramework, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
# clr.AddReferenceByName("PresentationCore, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System.Windows.Forms')

import System.Windows

#set the active Revit application and document
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
activeView = doc.ActiveView

# define function pickobject()
def pickobject():
from Autodesk.Revit.UI.Selection import ObjectType
__window__.Hide()
picked = uidoc.Selection.PickObject(ObjectType.Element, \
'Pick the Titleblock on the required sheet')
__window__.Show()
__window__.Topmost = True
return picked

# Instructs User to select the TitleBlock on
# the required Shedule Sheet with a Dialog Box
TaskDialog.Show('Selection','Please select the Titleblock on the required Schedule Sheet')
# Gets the Selected TitleBlock to Extract Sheet Number
sheets = doc.GetElement(pickobject()) 
# Stores Sheet Number as string under variable h
h = sheets.LookupParameter('Sheet Number').AsString() 
# Confirms the Selected Sheet Number with a Dialog Box
TaskDialog.Show('Result', 'The Sheet Number of the selected sheet is \n'+h)

# Collect All Sheets in project to find Sheet Element 
# matching selected Sheet Number

Shtlist = []
ShtNums = [] 
ShtElems = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
# Check for matches between sheet 'Sheet Number' \
# and selected titleblock 'Sheet Number'
# Where it matches add sheet element to elementlist

for e in ShtElems:
num = e.LookupParameter('Sheet Number').AsString()
if num == h:
ShtNums.append(num)
Shtlist.append(e)
# SelSheet is the Sheet host of the selected titleblock.

# Get ScheduleViews on the sheet.
SelSht = Shtlist[0]
SelShtNo = SelSht.LookupParameter('Sheet Number').AsString()
print (str(SelShtNo))
elementlist = []

for sheet in Shtlist:
try:
viewlist = list()
collector = FilteredElementCollector(sheet.Document, sheet.Id) \
.OfClass(ScheduleSheetInstance)
for item in collector:
viewlist.append(sheet.Document.GetElement(item.ScheduleId))
elementlist.append(viewlist)
except:
elementlist.append()
schtables = elementlist[0]
NoSch = len(schtables)
print(NoSch)
# Gets Elements in each Schedule Table and puts them into lists = listElemOnSch
listElemOnSch = []
for sch in schtables:
collector = FilteredElementCollector(doc, sch.Id)
listElemOnSch.append(collector.ToElements())
# Transaction to write the schedule number to all the elements in 
# schedule tables on the selected sheet
t = Transaction(doc, 'Write Schedule No. to items on schedule')
t.Start(); 
for listElems in listElemOnSch:
print(str(len(listElems)))
for elems in listElems:
param = elems.LookupParameter('SCHEDULE_No.')
param.Set(SelShtNo)
t.Commit();