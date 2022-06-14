# -*- coding: utf-8 -*-
__title__ = "Active View Filters"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 08.06.2022
_____________________________________________________________________
Description:
Dockable Panel showing all filters for the Active View.
_____________________________________________________________________
Last update:
- [08.06.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- Show all filters in active view
- make it a dockable panel
- add functionality of original filters (visibility on/off, projection/cut overrides etc.)
_____________________________________________________________________
Author: Harley Trappitt"""                          # Button Description shown in Revit UI

# EXTRA: You can remove them.
__author__ = "Harley Trappitt"                      # Script's Author
__helpurl__ = ""                                    # Link that can be opened with F1 when hovered over the tool in Revit UI.
#__highlight__ = "new"                                  # Button will have an orange dot + Description in Revit UI
__min_revit_ver__ = 2021                            # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
__max_revit_ver = 2023                              # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
# __context__     = ['Walls', 'Floors', 'Roofs']    # Make your button available only when certain categories are selected. Or Revit/View Types.


#   You need to use 'os' package to get all files in the given folder with 'os.listdir'.
#   Then you can filter family files and iterate through them to open each and make a change.
#ModelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(path_to_rfa)
#options = OpenOptions()
#rvt_doc = app.OpenDocumentFile(ModelPath, options)
#   Then make your changes to rvt_doc and close it.

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
import os, sys, math, datetime, time                                    # Regular Imports
from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import Transaction, FilteredElementCollector     # or Import only classes that are used.

# pyRevit
from pyrevit import revit, forms                                        # import pyRevit modules. (Lots of useful features)
from pyrevit import DB, UI
from pyrevit.framework import Input
from pyrevit import script
from pyrevit import HOST_APP, framework, coreutils, PyRevitException
from pyrevit import revit, DB, UI
from pyrevit import forms, script
from pyrevit.framework import wpf, ObservableCollection

# Custom Imports
# from Snippets._selection import get_selected_elements                   # lib import
# from Snippets._convert import convert_internal_to_m                     # lib import

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference("System")                  # Refference System.dll for import.
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentesis.

clr.AddReference("RevitServices")
import RevitServices
#from RevitServices.Persistence import DocumentManager
#doc = DocumentManager.Instance.CurrentDBDocument
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# WPF Dependencies
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

# find the path of ui.xaml
from pyrevit import UI
from pyrevit import script
xamlfile = script.get_bundle_file('ui.xaml')

# import WPF creator and base Window
import wpf
from System import Windows

from System.Collections.ObjectModel import ObservableCollection
from System.ComponentModel import INotifyPropertyChanged, PropertyChangedEventArgs
from System.Windows.Input import ICommand
from System.Windows import Controls
from System import ComponentModel
import pyevent


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)     # Absolute path to the folder where script is placed.



# GLOBAL VARIABLES

# - Place global variables here.

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ FUNCTIONS
# ==================================================

# - Place local functions here. If you might use any functions in other scripts, consider placing it in the lib folder.

# ╔═╗╦  ╔═╗╔═╗╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗║╣ ╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝╚═╝╚═╝ CLASSES
# ==================================================

# - Place local classes here. If you might use any classes in other scripts, consider placing it in the lib folder.

class _WPFPanelProvider(UI.IDockablePaneProvider):
    def __init__(self, panel_type, default_visible=True):
        self._panel_type = panel_type
        self._default_visible = default_visible
        self.panel = self._panel_type()

    def update_list(self):
        try:
            template_list = [forms.TemplateListItem(s.IntegerValue) for s in selected]
            self.selected_lb.ItemsSource = ObservableCollection[forms.TemplateListItem](template_list)
        except Exception as e:
            print e.message


class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

    def say_hello(self, sender, args):
        name = self.textbox.Text
        UI.TaskDialog.Show(
            "Hello World",
            "Hello {}".format(name or "World!")
            )

    def get_view_filters(self, sender, args):
        pass


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
#if __name__ == '__main__':
    # START CODE HERE
projRGBList, cutRGBList, surForPatList, surBacPatList, cutForPatList, cutBacPatList, transList, halfList, prweList = [],[],[],[],[],[],[],[],[]
prPatList, cutweList, cutPatList, surForList, surBacList, cutForList, cutBacList, elementList, nameList = [],[],[],[],[],[],[],[],[]
visibilitiesList, categories = [],[]

current_view = doc.ActiveView
view_filters = {}

filters = current_view.GetFilters()

elements, elementName, visibilities, listprojRGB, listcutRGB, listtrans, listhalf, listprwe, listprPat, listcutwe = [],[],[],[],[],[],[],[],[],[]
listcutPat, rgbsurForList, rgbsurBacList, rgbCutForList, rgbCutBacList, listSurForPat,listSurBacPat,listCutForPat = [],[],[],[],[],[],[],[],[],[]
listCutBacPat,cats = [],[]

for f in filters:
    visibilities.append(current_view.GetFilterVisibility(f))
    element=doc.GetElement(f)
    elements.append(element)
    elementName.append(element.Name)

    if element:
        view_filters[
            "%s: %s" % (element.Name, visibilities)
        ] = elements

    visibilities.append(v.GetFilterVisibility(f))
    element=doc.GetElement(f)
    elements.append(element)
    elementName.append(element.Name)
    catid=[Revit.Elements.Category.ById(c.IntegerValue).Name for c in element.GetCategories()]
    cate = catid if len(catid)>1 else catid[0]
    cats.append(cate)
    filterObject = v.GetFilterOverrides(f)
    projCol = filterObject.ProjectionLineColor
    if projCol.IsValid:
        projrgb = DSCore.Color.ByARGB(255, projCol.Red, projCol.Green, projCol.Blue)
    else:
        projrgb = None
    listprojRGB.Add(projrgb)

    cutCol= filterObject.CutLineColor
    if cutCol.IsValid:
        cutrgb = DSCore.Color.ByARGB(255, cutCol.Red, cutCol.Green, cutCol.Blue)
    else:
        cutrgb = None
    listcutRGB.Add(cutrgb)
    listtrans.append(filterObject.Transparency)
    listhalf.append(filterObject.Halftone)
    listprwe.append(filterObject.ProjectionLineWeight)
    listprPat.append(doc.GetElement(filterObject.ProjectionLinePatternId))
    listcutwe.append(filterObject.CutLineWeight)
    listcutPat.append(doc.GetElement(filterObject.CutLinePatternId))
    if version < 2019 :
        col = filterObject.ProjectionFillColor
        if col.IsValid:
            rgbSurFor = DSCore.Color.ByARGB(255, col.Red, col.Green, col.Blue)
        else:
            rgbSurFor = None
        rgbsurForList.Add(rgbSurFor)
        rgbsurBacList.Add(rgbSurFor)

        cut = filterObject.CutFillColor
        if cut.IsValid:
            rgbcut = DSCore.Color.ByARGB(255, cut.Red, cut.Green, cut.Blue)
        else:
            rgbcut = None
        rgbCutForList.Add(rgbcut)
        rgbCutBacList.Add(rgbcut)
        listSurForPat.append(doc.GetElement(filterObject.ProjectionFillPatternId))
        listSurBacPat.append(doc.GetElement(filterObject.ProjectionFillPatternId))
        listCutForPat.append(doc.GetElement(filterObject.CutFillPatternId))
        listCutBacPat.append(doc.GetElement(filterObject.CutFillPatternId))
    else:
        col = filterObject.SurfaceForegroundPatternColor
        if col.IsValid:
            rgbSurFor = DSCore.Color.ByARGB(255, col.Red, col.Green, col.Blue)
        else:
            rgbSurFor = None
        rgbsurForList.Add(rgbSurFor)

        surBacCol = filterObject.SurfaceBackgroundPatternColor
        if surBacCol.IsValid:
            rgbSurBac = DSCore.Color.ByARGB(255, surBacCol.Red, surBacCol.Green, surBacCol.Blue)
        else:
            rgbSurBac = None
        rgbsurBacList.Add(rgbSurBac)

        cut = filterObject.CutForegroundPatternColor
        if cut.IsValid:
            rgbcut = DSCore.Color.ByARGB(255, cut.Red, cut.Green, cut.Blue)
        else:
            rgbcut = None
        rgbCutForList.Add(rgbcut)

        cutBac = filterObject.CutBackgroundPatternColor
        if cutBac.IsValid:
            rgbCutBac = DSCore.Color.ByARGB(255, cutBac.Red, cutBac.Green, cutBac.Blue)
        else:
            rgbCutBac = None
        rgbCutBacList.Add(rgbCutBac)
        listSurForPat.append(doc.GetElement(filterObject.SurfaceForegroundPatternId))
        listSurBacPat.append(doc.GetElement(filterObject.SurfaceBackgroundPatternId))
        listCutForPat.append(doc.GetElement(filterObject.CutForegroundPatternId))
        listCutBacPat.append(doc.GetElement(filterObject.CutBackgroundPatternId))
		
prPatList.append(listprPat)
projRGBList.Add(listprojRGB)
prweList.append(listprwe)
surForPatList.append(listSurForPat)
surForList.Add(rgbsurForList)
surBacPatList.append(listSurBacPat)
surBacList.Add(rgbsurBacList)

cutPatList.append(listcutPat)
cutweList.append(listcutwe)
cutRGBList.Add(listcutRGB)
cutForPatList.append(listCutForPat)
cutForList.Add(rgbCutForList)
cutBacPatList.append(listCutBacPat)
cutBacList.Add(rgbCutBacList)

transList.Add(listtrans)
halfList.Add(listhalf)
visibilitiesList.append(visibilities)
elementList.append(elements)
nameList.append(elementName)
categories.append(cats)

# Let's show the window (modal)
MyWindow().ShowDialog()


################################################################################################
#family_dict = {}
#for e in revit.query.get_all_elements_in_view(active_view):
#    try:
#        e_type = revit.query.get_type(e)
#        family = e_type.Family
#        if family.FamilyCategory:
#            family_dict[
#                "%s: %s" % (family.FamilyCategory.Name, family.Name)
#            ] = family
#    except:
#        pass
#if family_dict:
#    selected_families = forms.SelectFromList.show(
#        sorted(family_dict.keys()),
#        title="Select Families",
#        multiselect=True,
#    )
################################################################################################

HOST_APP.uiapp.Idling += \
    framework.EventHandler[UI.Events.IdlingEventArgs](idling_eventhandler)

# AVOID  placing Transaction inside of your loops! It will drastically reduce perfomance of your script.
t = Transaction(doc,__title__)  # Transactions are context-like objects that guard any changes made to a Revit model.

# You need to use t.Start() and t.Commit() to make changes to a Project.
t.Start()  # <- Transaction Start

#- CHANGES TO REVIT PROJECT HERE

t.Commit()  # <- Transaction End

# Notify user that script is complete.
print('Script is finished.')