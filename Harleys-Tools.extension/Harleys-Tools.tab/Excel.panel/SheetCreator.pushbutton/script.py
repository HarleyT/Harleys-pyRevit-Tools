# -*- coding: utf-8 -*-
__title__ = "SheetCreator"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 11.03.2025
_____________________________________________________________________
Description:

_____________________________________________________________________
How-to:
-> Click on the button
_____________________________________________________________________
Last update:
- 
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Harley Trappitt"""                                           # Button Description shown in Revit UI

# EXTRA: You can remove them.
__author__ = "Harley Trappitt"                                       # Script's Author
#__helpurl__ = "https://www.youtube.com/watch?v=YhL_iOKH-1M"     # Link that can be opened with F1 when hovered over the tool in Revit UI.
# __highlight__ = "new"                                           # Button will have an orange dot + Description in Revit UI
__min_revit_ver__ = 2019                                        # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
__max_revit_ver = 2025                                          # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
# __context__     = ['Walls', 'Floors', 'Roofs']                # Make your button available only when certain categories are selected. Or Revit/View Types.

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================

# import os, sys, datetime
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.ApplicationServices import *
import xlrd

# .NET Imports
import os
import clr
clr.AddReference("System")                  # Reference System.dll for import.
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentesis.

# pyRevit
#from pyrevit import forms, revit, script


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc   = __revit__.ActiveUIDocument.Document     #type: Document     # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc = __revit__.ActiveUIDocument              #type: UIDocument   # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app   = __revit__.Application                   #type: Application  # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
rvt_year = int(app.VersionNumber)               # e.g. 2023

PATH_SCRIPT = os.path.dirname(__file__)         # Absolute path to the folder where script is placed.




# GLOBAL VARIABLES

# - Place global variables here.
filepath = "P:\2024 JOBS\24385 Global Switch Data Centre Upgrade Project - Ultimo\1_Project Management\BIM Execution Plan\ISO 19650-2 RBG Documentation\Task Information Delivery Plan"
workbook = xlrd.open_workbook(filepath)
worksheet = workbook.sheet_by_index(5)
parameter_names = worksheet.row_values(11)
data = []

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
    for row in range(1,worksheet.nrows):
        row_values = worksheet.row_values(row)
        row_data = {}

        for i, parameter_name in enumerate(parameter_names):
            row_data[parameter_name] = row_values[i]

        data.append(row_data)

    # AVOID  placing Transaction inside of your loops! It will drastically reduce perfomance of your script.
    t = Transaction(doc,__title__)  # Transactions are context-like objects that guard any changes made to a Revit model.

    # You need to use t.Start() and t.Commit() to make changes to a Project.
    t.Start()  # <- Transaction Start

    #- CHANGES TO REVIT PROJECT HERE

    t.Commit()  # <- Transaction End

    # Notify user that script is complete.
    print(data)
    print('Script is finished.')
    print('Template has been developed by Erik Frits.')