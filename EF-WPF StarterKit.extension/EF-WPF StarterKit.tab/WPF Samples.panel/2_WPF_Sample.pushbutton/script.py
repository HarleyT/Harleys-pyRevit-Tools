# -*- coding: utf-8 -*-
__title__   = "Code Samples: WPF Form Sample"
__doc__ = """Version = 1.0
Date    = 15.07.2024
_____________________________________________________________________
Description:
Example of using WPF Form.
Keep in mind that WPF forms need a .xaml file that has the form design.
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
from pyrevit import forms   # By importing forms you also get references to WPF package! Very IMPORTANT
import wpf, os, clr         # wpf can be imported only after pyrevit.forms!

# .NET Imports
clr.AddReference("System")
from System.Collections.Generic import List
from System.Windows import Application, Window, ResourceDictionary
from System.Windows.Controls import CheckBox, Button, TextBox, ListBoxItem



# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#====================================================================================================
PATH_SCRIPT = os.path.dirname(__file__)
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application
doc     = __revit__.ActiveUIDocument.Document #type: Document




# ╔═╗╦  ╔═╗╔═╗╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗║╣ ╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝╚═╝╚═╝
#====================================================================================================
class ListItem:
    """Helper Class for defining items in the ListBox."""
    def __init__(self,  Name='Unnamed', element = None, checked = False):
        self.Name       = Name
        self.IsChecked  = checked
        self.element    = element

    def __str__(self):
        return self.Name

# ╔╦╗╔═╗╦╔╗╔  ╔═╗╔═╗╦═╗╔╦╗
# ║║║╠═╣║║║║  ╠╣ ║ ║╠╦╝║║║
# ╩ ╩╩ ╩╩╝╚╝  ╚  ╚═╝╩╚═╩ ╩ MAIN FORM
#====================================================================================================
class SimpleForm(Window):

    def __init__(self):
        # Connect to .xaml File (in same folder)
        path_xaml_file = os.path.join(PATH_SCRIPT, 'FormUI.xaml')
        wpf.LoadComponent(self, path_xaml_file)

        # Define items for ListBox
        self.items = self.generate_listbox_items()
        self.UI_listbox.ItemsSource = self.items

        # Show Form
        self.ShowDialog()


    # ╔╦╗╔═╗╔╦╗╦ ╦╔═╗╔╦╗╔═╗
    # ║║║║╣  ║ ╠═╣║ ║ ║║╚═╗
    # ╩ ╩╚═╝ ╩ ╩ ╩╚═╝═╩╝╚═╝
    def generate_listbox_items(self):
        """Function to create a ICollection to pass to ListBox in GUI"""
        # Define Elements for ListBox (WallTypes)
        wall_types      = FilteredElementCollector(doc).OfClass(WallType).ToElements()
        dict_wall_types = {Element.Name.GetValue(wt): wt for wt in wall_types}

        # check_box = False
        # for item_name, item in sorted(dict_wall_types.items()):
        #     check_box = CheckBox(Content=item_name)
        #     list_box_item = ListBoxItem(Content=check_box)
        #     self.UI_listbox.Items.Add(list_box_item)


        # # Prepare List of Items
        # list_of_items = List[type(ListBoxItem())]()
        # for item_name, item in sorted(dict_wall_types.items()):
        #
        #
        #     list_of_items.Add(ListBoxItem(Content=item_name, ))

        # Prepare List of Items
        list_of_items = List[type(ListItem())]()
        for item_name, item in sorted(dict_wall_types.items()):
            list_of_items.Add(ListItem(item_name, item, False))

        return list_of_items



    # ╔═╗╦═╗╔═╗╔═╗╔═╗╦═╗╔╦╗╦╔═╗╔═╗
    # ╠═╝╠╦╝║ ║╠═╝║╣ ╠╦╝ ║ ║║╣ ╚═╗
    # ╩  ╩╚═╚═╝╩  ╚═╝╩╚═ ╩ ╩╚═╝╚═╝
    #====================================================================================================
    ef_comment = """You can access all the components in your .xaml form by their x:Name property"""

    # Read Textboxes and Checkboxes values from Form

    @property
    def textbox_1(self):
        return self.UI_textbox_1.Text

    @property
    def textbox_2(self):
        return self.UI_textbox_2.Text

    @property
    def checkbox_1(self):
        return self.UI_checkbox_1.IsChecked

    @property
    def checkbox_2(self):
        return self.UI_checkbox_2.IsChecked

    @property
    def checkbox_3(self):
        return self.UI_checkbox_3.IsChecked


    @property
    def search(self):
        return self.UI_search.IsChecked


    # ╔═╗╦  ╦╔═╗╔╗╔╔╦╗╔═╗
    # ║╣ ╚╗╔╝║╣ ║║║ ║ ╚═╗
    # ╚═╝ ╚╝ ╚═╝╝╚╝ ╩ ╚═╝
    #====================================================================================================
    def UIe_search_changed(self, sender, e):
        """Function to filter items in the main_ListBox."""
        filtered_list_of_items = List[type(ListItem())]()
        filter_keyword = self.UI_search.Text

        #RESTORE ORIGINAL LIST
        if not filter_keyword:
            self.UI_listbox.ItemsSource = self.items
            return

        # FILTER ITEMS
        for item in self.items:
            if filter_keyword.lower() in item.Name.lower():
                filtered_list_of_items.Add(item)

        # UPDATE LIST OF ITEMS
        self.UI_listbox.ItemsSource = filtered_list_of_items


    # ╔╗ ╦ ╦╔╦╗╔╦╗╔═╗╔╗╔╔═╗
    # ╠╩╗║ ║ ║  ║ ║ ║║║║╚═╗
    # ╚═╝╚═╝ ╩  ╩ ╚═╝╝╚╝╚═╝ BUTTONS
    #==================================================
    def UIe_button_run(self, sender, e):
        """Button action: Rename view with given """
        self.Close()
        # You can do something here when button is clicked



# ╦ ╦╔═╗╔═╗  ╔═╗╔═╗╦═╗╔╦╗
# ║ ║╚═╗║╣   ╠╣ ║ ║╠╦╝║║║
# ╚═╝╚═╝╚═╝  ╚  ╚═╝╩╚═╩ ╩


# Show form to the user
UI = SimpleForm()

# Read Form Values


text_1 = UI.textbox_1
text_2 = UI.textbox_2

check_1 = UI.checkbox_1
check_2 = UI.checkbox_2
check_3 = UI.checkbox_3

sel_combo_item   = UI.UI_combobox.SelectedItem

text_search      = UI.UI_search.Text
sel_listbox_item = UI.UI_listbox.SelectedItem

# Print Results

from pyrevit import script
output = script.get_output()

output.print_md('## Selected Values in EF-WPF Form:')
output.print_md('**TextBox 1:** {}'.format(text_1))
output.print_md('**TextBox 2:** {}'.format(text_2))

output.print_md('**CheckBox 1:** {}'.format(check_1))
output.print_md('**CheckBox 2:** {}'.format(check_2))
output.print_md('**CheckBox 3:** {}'.format(check_3))

output.print_md('**ComboBox Selected Item:** {}'.format(sel_combo_item))

output.print_md('**Search TextBox:** {}'.format(text_search))
output.print_md('**ListBox Selected Item:** {}'.format(sel_listbox_item))






