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

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
#if __name__ == '__main__':
    # START CODE HERE

current_view = doc.ActiveView.ToDSType(True)

for v in current_view:
    filters = v.GetFilters()
    elements, elementName, visibilities = [],[],[]
    for f in filters:
        visibilities.append(v.GetFilterVisibility(f))
        element=doc.GetElement(f)
        elements.append(element)
        elementName.append(element.Name)

        view_filters = forms.SelectFromList.show(

            sorted(view_filters.keys()),

            title="Select Filters",

            multiselect=True,

        )


# AVOID  placing Transaction inside of your loops! It will drastically reduce perfomance of your script.
t = Transaction(doc,__title__)  # Transactions are context-like objects that guard any changes made to a Revit model.

# You need to use t.Start() and t.Commit() to make changes to a Project.
t.Start()  # <- Transaction Start

#- CHANGES TO REVIT PROJECT HERE

t.Commit()  # <- Transaction End

# Notify user that script is complete.
print('Script is finished.')