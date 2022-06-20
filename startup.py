# -*- coding: UTF-8 -*-
import System
import os.path as op
from pyrevit import HOST_APP, framework, coreutils, PyRevitException
from pyrevit import revit, DB, UI
from pyrevit import forms, script
from pyrevit.framework import wpf, ObservableCollection

import clr
clr.AddReference('DSCoreNodes')
import DSCore
from DSCore import Color

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitNodes')
import Revit

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
#doc = DocumentManager.Instance.CurrentDBDocument
#uiapp = DocumentManager.Instance.CurrentUIApplication
#app = uiapp.Application
#version=int(app.VersionNumber)

#current_view = Revit.Document.ActiveView(doc)

doc = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
#PATH_SCRIPT = os.path.dirname(__file__)     # Absolute path to the folder where script is placed.
current_view = doc.ActiveView
#uidoc = HOST_APP.uidoc

filters = current_view.GetFilters()
FilterVisibility, element, elements, FilterName = [],[],[],[]


print('Startup script execution test.')
print('\n'.join(sys.path))

# test code for creating event handlers =======================================
# define event handler
def docopen_eventhandler(sender, args):
    forms.alert('Document Opened: {}'.format(args.PathName))

# add to DocumentOpening
# type is EventHandler[DocumentOpeningEventArgs] so create that correctly
HOST_APP.app.DocumentOpening += \
    framework.EventHandler[DB.Events.DocumentOpeningEventArgs](
        docopen_eventhandler
        )


# test dockable panel =========================================================

class DockableExample(forms.WPFPanel):
    panel_title = "Active View - Filters"
    panel_id = "3110e336-f81c-4927-87da-4e0d30d4d64b"
    panel_source = op.join(op.dirname(__file__), "ui.xaml")

    def do_something(self, sender, args):
        forms.alert("Voila!!!")

    def refresh_active_view():
        uidoc.RequestViewChange(current_view)
        uidoc.RefreshActiveView()
        doc.Regenerate()

    def active_filters(self):
        try:
            #template_list = [forms.TemplateListItem(s.IntegerValue) for s in selected]
            #self.selected_lb.ItemsSource = ObservableCollection[forms.TemplateListItem](template_list)
            for f in filters:
                FilterVisibility.append(current_view.GetFilterVisibility(f))
                element=doc.GetElement(f)
                elements.append(element)
                FilterName.append(element.Name)
        except Exception as e:
            print e.message

if not forms.is_registered_dockable_panel(DockableExample):
    forms.register_dockable_panel(DockableExample)
else:
    print("Skipped registering dockable pane. Already exists.")