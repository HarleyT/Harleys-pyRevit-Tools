#import clr
#clr.AddReference('RevitAPI')
#clr.AddReference('System.Windows.Forms')
#clr.AddReference('IronPython.Wpf')
#from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter
#from pyrevit import revit, script, UI
#import re
#import wpf
#xamlfile = script.get_bundle_file('ui.xaml')
#from System import Windows


# Import the XAML layout
#clr.AddReference('PresentationFramework')
#from System.Windows import Application, Window

# Define a regular expression pattern to match Unicode characters
#unicode_pattern = re.compile('[^\x00-\x7F]+')

# Function to check if a string contains Unicode characters
#def contains_unicode(text):
#    return bool(unicode_pattern.search(text))

# Function to search for Unicode characters in sheet numbers
#def search_sheets_for_unicode(sender, e):
#    # Get all sheets in the current Revit project
#    sheets_collector = FilteredElementCollector(revit.doc).OfCategory(BuiltInCategory.OST_Sheets)
#    sheets = list(sheets_collector)

    # Initialize a list to store sheets with Unicode characters
#    sheets_with_unicode = []

    # Iterate through each sheet and check its sheet number
#    for sheet in sheets:
#        sheet_number = sheet.get_Parameter(BuiltInParameter.SHEET_NUMBER).AsString()
#        if contains_unicode(sheet_number):
#            sheets_with_unicode.append(sheet_number)

    # Display the sheets with Unicode characters in the resultTextBox
#    if sheets_with_unicode:
#        resultTextBox.Text = "\n".join(sheets_with_unicode)
#    else:
#        resultTextBox.Text = "No sheets with Unicode characters found."

# Create the main window
#class MainWindow(Windows.Window):
#    def __init__(self):
#        wpf.LoadComponent(self, xamlfile)
#        self.SearchButton_Click += self.search_sheets_for_unicode

#if __name__ == '__main__':
#    #Application().Run(MainWindow())
#    MainWindow().ShowDialog()


import os, sys, math, datetime, time                                    # Regular Imports
from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import Transaction, FilteredElementCollector     # or Import only classes that are used.

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference("System")                  # Refference System.dll for import.
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentesis.


# dependencies
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
import re

# find the path of ui.xaml
from pyrevit import UI
from pyrevit import script
xamlfile = script.get_bundle_file('ui.xaml')

# import WPF creator and base Window
import wpf
from System import Windows

doc = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)     # Absolute path to the folder where script is placed.

class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

    # Function to search for Unicode characters in sheet numbers
    def SearchButton_Click(self, sender, args):
        # Get all sheets in the current Revit project
        sheets_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets)
        sheets = list(sheets_collector)

        # Initialize a list to store sheets with Unicode characters
        sheets_with_unicode = []
        unicode_pattern = re.compile('[^\x00-\x7F]+')

        # Iterate through each sheet and check its sheet number
        for sheet in sheets:
            sheet_number = sheet.get_Parameter(BuiltInParameter.SHEET_NUMBER).AsString()
            if bool(unicode_pattern.search(sheet_number)):
                sheets_with_unicode.append(sheet_number)

        # Display the sheets with Unicode characters in the resultTextBox
        if sheets_with_unicode:
            resultTextBox.Text = "\n".join(sheets_with_unicode)
        else:
            resultTextBox.Text = "No sheets with Unicode characters found."

# Let's show the window (modal)
MyWindow().ShowDialog()