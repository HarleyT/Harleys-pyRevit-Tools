# -*- coding: utf-8 -*-
__title__   = "EF-WPF: SelectFromList"
__doc__ = """Version = 1.0
Date    = 15.07.2024
_____________________________________________________________________
Description:
Example of EF-WPF SelectFromList Form with multi-select option.
This will show you how to populate list of items in the ListBox, 
How to create events on buttons and how to get your selection.

Happy Coding!
Erik Frits            
_____________________________________________________________________
How-To:
- Click the Button
_____________________________________________________________________
Last update:
- [15.07.2024] - V1.0 RELEASE
_____________________________________________________________________
Author: Erik Frits from LearnRevitAPI.com"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#====================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms   # By importing forms you also get references to WPF package! IT'S Very IMPORTANT !!!
import wpf, os, clr         # wpf can be imported only after pyrevit.forms!

# .NET Imports
clr.AddReference("System")
from System.Collections.Generic import List
from System.Windows import Application, Window, ResourceDictionary
from System.Windows.Controls import CheckBox, Button, TextBox, ListBoxItem
from System.Diagnostics.Process import Start
from System.Windows.Window import DragMove
from System.Windows.Input import MouseButtonState
from System import Uri

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#====================================================================================================
PATH_SCRIPT = os.path.dirname(__file__)
doc     = __revit__.ActiveUIDocument.Document #type: Document
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application


# ╔╦╗╔═╗╦╔╗╔  ╔═╗╔═╗╦═╗╔╦╗
# ║║║╠═╣║║║║  ╠╣ ║ ║╠╦╝║║║
# ╩ ╩╩ ╩╩╝╚╝  ╚  ╚═╝╩╚═╩ ╩ MAIN FORM
#====================================================================================================
# Inherit .NET Window for your UI Form Class
class EF_SelectFromList(Window):

    def __init__(self):
        # Connect to .xaml File (in the same folder!)
        path_xaml_file = os.path.join(PATH_SCRIPT, 'SelectFromList_UI.xaml')
        wpf.LoadComponent(self, path_xaml_file)

        # Populate ListBox with Views
        self.populate_views_list()

        # Show Form
        self.ShowDialog()

    # ╔╦╗╔═╗╔╦╗╦ ╦╔═╗╔╦╗╔═╗
    # ║║║║╣  ║ ╠═╣║ ║ ║║╚═╗
    # ╩ ╩╚═╝ ╩ ╩ ╩╚═╝═╩╝╚═╝
    #==================================================
    def populate_views_list(self):
        """Populate the list box with views"""
        views = FilteredElementCollector(doc).OfClass(View).ToElements()
        for view in views:
            if not view.IsTemplate:  # Skip view templates
                list_item = ListBoxItem()
                view_name = '[{}] {}'.format(view.ViewType, view.Name)
                check_box = CheckBox(Content=view_name, Tag=view)
                list_item.Content = check_box
                self.listBoxViews.Items.Add(list_item)

    def get_selected_views(self):
        selected_views = []
        for item in self.listBoxViews.Items:
            check_box = item.Content
            if check_box.IsChecked:
                selected_views.append(check_box.Tag)
        return selected_views

    # ╔╗ ╦ ╦╔╦╗╔╦╗╔═╗╔╗╔╔═╗
    # ╠╩╗║ ║ ║  ║ ║ ║║║║╚═╗
    # ╚═╝╚═╝ ╩  ╩ ╚═╝╝╚╝╚═╝ BUTTONS
    #==================================================
    def UIe_button_select_all(self, sender, e):
        """Button action: Select all checkboxes"""
        for item in self.listBoxViews.Items:
            check_box = item.Content
            check_box.IsChecked = True

    def UIe_button_select_none(self, sender, e):
        """Button action: Deselect all checkboxes"""
        for item in self.listBoxViews.Items:
            check_box = item.Content
            check_box.IsChecked = False

    def UIe_button_run(self, sender, e):
        """Button action: Handle selected views"""
        self.Close()


# ╦ ╦╔═╗╔═╗  ╔═╗╔═╗╦═╗╔╦╗
# ║ ║╚═╗║╣   ╠╣ ║ ║╠╦╝║║║
# ╚═╝╚═╝╚═╝  ╚  ╚═╝╩╚═╩ ╩
#====================================================================================================

# Show form to the user
UI = EF_SelectFromList()

# Get User Input
selected_views = UI.get_selected_views()

# Display Selected items
print('Selected Views:')
for view in selected_views:
    print(view.Name)





