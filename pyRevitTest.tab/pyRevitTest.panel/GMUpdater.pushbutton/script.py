# -*- coding: utf-8 -*-
__title__ = "Generic Model w/ DWG Import Updater"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 18.05.2022
_____________________________________________________________________
Description:
Update selected Generic Models with their selected .dwg imports.

_____________________________________________________________________
How-to:

-> Select ACCDocs folder in AML Project
-> Select .rfa file to edit
-> Select .dwg to import into .rfa
-> Reload selected Generic Models
_____________________________________________________________________
Last update:
- [18.05.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- Select ACCDocs folder in AML Project
- Select .rfa file to edit
- Select .dwg to import into .rfa
- Reload selected Generic Models
_____________________________________________________________________
Author: Harley Trappitt"""                          # Button Description shown in Revit UI

# EXTRA: You can remove them.
__author__ = "Harley Trappitt"                      # Script's Author
__helpurl__ = ""                                    # Link that can be opened with F1 when hovered over the tool in Revit UI.
__highlight__ = "new"                               # Button will have an orange dot + Description in Revit UI
__min_revit_ver__ = 2021                            # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
__max_revit_ver = 2023                              # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
# __context__     = ['Walls', 'Floors', 'Roofs']    # Make your button available only when certain categories are selected. Or Revit/View Types.

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
from Snippets._selection import get_selected_elements                   # lib import
from Snippets._convert import convert_internal_to_m                     # lib import

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference("System")                  # Refference System.dll for import.
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentesis.

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)     # Absolute path to the folder where script is placed.

user = app.Username
filepath = "C:\Users" + user + "\ACCDocs\GHD Services Pty Ltd\12545014 - AML Detail Design 15MTPA\Project Files\02 - DELIVERY"
family_dict = {}

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
if __name__ == '__main__':
    # START CODE HERE
    for family in revit.query.get_families(revit.doc, only_editable=True):

        if family.FamilyCategory.Name == "Generic Models":

            family_dict[

                "%s: %s" % (family.FamilyCategory.Name, family.Name)

            ] = family

        if family_dict:

            selected_families = forms.SelectFromList.show(

                sorted(family_dict.keys()),

                title="Select Families",

                multiselect=True,

            )

            if selected_families:

                for idx, family in enumerate([family_dict[x] for x in selected_families]):
                    
                    print (user)
                    print (filepath)
                    print (family.Name)            
                    print (family)
    
    # AVOID  placing Transaction inside of your loops! It will drastically reduce perfomance of your script.
    t = Transaction(doc,__title__)  # Transactions are context-like objects that guard any changes made to a Revit model.

    # You need to use t.Start() and t.Commit() to make changes to a Project.
    t.Start()  # <- Transaction Start

    #- CHANGES TO REVIT PROJECT HERE

    t.Commit()  # <- Transaction End

    # Notify user that script is complete.
    print('Script is finished.')