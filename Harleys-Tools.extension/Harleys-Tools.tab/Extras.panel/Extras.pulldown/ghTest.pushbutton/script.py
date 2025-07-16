# -*- coding: utf-8 -*-
__title__   = "HTML Testing"
__doc__     = """Version = 1.0"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr
clr.AddReference('System')
clr.AddReferemce('System.Windows.Forms')
clr.AddReferemce('System.Diagnostics')
from System.Collections.Generic import List

from System.Diagnostics import Process
from System.Windows.Forms import OpenFileDialog, DialogResult

import os
from pyrevit import script
from pyrevit.forms import WPFWindow



# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

def open_grasshopper_script(gh_file_path):
    try:
        Process.Start(gh_file_path)
        print(f"Attempting to open Grasshopper Script: {gh_file_path}")
        except Exception as e:
            print(f"Error opening Grasshopper script: {e}")
            print("Ensure Grasshopper (and Rhino) is installed and the .gh/.ghx file association is correct.")

def select_and_open_gh_script():
    openFileDialog = OpenFileDialog()
    openFileDialog.Filter = "Grasshopper Script Files {*.gh;.ghx}|*.gh;*.ghx|All files(*.*)|*.*"
    openFileDialog.Title = "Select a Grasshopper Script File"

    if openFileDialog.ShowDialog() == DialogResult.OK:
        selected_file_path = openFileDialog.FileName
        if os.path.exists(selected_file_path):
            open_grasshopper_script(selected_file_path)
            else:
                print("Grasshopper script selection cancelled.")

if __name__ == '__main__':
    # Option 1: Hardcode the path (for developemnt/testing)
    # Be sure to change this to an actual path on your system.
    # example_gh_path = r="UI SCRIPT.gh"
    # open_grasshopper_script(example_gh_path)

    # Option 2: Allow the user to select the file (recommended for general use)
    select_and_open_gh_script()



#==================================================
