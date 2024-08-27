# -*- coding: utf-8 -*-
__title__   = "EF-WPF Select Paths"


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#====================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms   # By importing forms you also get references to WPF package! Very IMPORTANT
import wpf, os, clr         # wpf can be imported only after pyrevit.forms!

# .NET Imports
clr.AddReference("System")
from System.Collections.Generic import List
from System.Windows import Window
from System.Windows.Forms import FolderBrowserDialog
import System

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#====================================================================================================
PATH_SCRIPT = os.path.dirname(__file__)
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application
doc     = __revit__.ActiveUIDocument.Document #type: Document


# ╔╦╗╔═╗╦╔╗╔  ╔═╗╔═╗╦═╗╔╦╗
# ║║║╠═╣║║║║  ╠╣ ║ ║╠╦╝║║║
# ╩ ╩╩ ╩╩╝╚╝  ╚  ╚═╝╩╚═╩ ╩ MAIN FORM
#====================================================================================================
class SimpleForm(Window):

    def __init__(self):
        # Connect to .xaml File (in same folder)
        path_xaml_file = os.path.join(PATH_SCRIPT, 'FilePathsUI.xaml')
        wpf.LoadComponent(self, path_xaml_file)

        # Show Form
        self.ShowDialog()


    # ╔╦╗╔═╗╔╦╗╦ ╦╔═╗╔╦╗╔═╗
    # ║║║║╣  ║ ╠═╣║ ║ ║║╚═╗
    # ╩ ╩╚═╝ ╩ ╩ ╩╚═╝═╩╝╚═╝
    def browse_for_folder(self):
        dialog = FolderBrowserDialog()
        if dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK:
            return dialog.SelectedPath
        return None


    # ╔═╗╦  ╦╔═╗╔╗╔╔╦╗╔═╗
    # ║╣ ╚╗╔╝║╣ ║║║ ║ ╚═╗
    # ╚═╝ ╚╝ ╚═╝╝╚╝ ╩ ╚═╝
    #====================================================================================================
    def BrowseFolder1_Click(self, sender, e):
        folder_path = self.browse_for_folder()
        if folder_path:
            self.FolderPath1.Text = folder_path

    def BrowseFolder2_Click(self, sender, e):
        folder_path = self.browse_for_folder()
        if folder_path:
            self.FolderPath2.Text = folder_path

    def BrowseFolder3_Click(self, sender, e):
        folder_path = self.browse_for_folder()
        if folder_path:
            self.FolderPath3.Text = folder_path

    # ╔╗ ╦ ╦╔╦╗╔╦╗╔═╗╔╗╔╔═╗
    # ╠╩╗║ ║ ║  ║ ║ ║║║║╚═╗
    # ╚═╝╚═╝ ╩  ╩ ╚═╝╝╚╝╚═╝ BUTTONS
    #==================================================
    def UIe_button_run(self, sender, e):
        """Button action: Rename view with given """
        self.Close()
        # You can do something here when button is clicked too.



# ╦ ╦╔═╗╔═╗  ╔═╗╔═╗╦═╗╔╦╗
# ║ ║╚═╗║╣   ╠╣ ║ ║╠╦╝║║║
# ╚═╝╚═╝╚═╝  ╚  ╚═╝╩╚═╩ ╩
# Show form to the user
UI = SimpleForm()

# Get User Input
print('Path 1: {}'.format(UI.FolderPath1.Text))
print('Path 2: {}'.format(UI.FolderPath2.Text))
print('Path 3: {}'.format(UI.FolderPath3.Text))