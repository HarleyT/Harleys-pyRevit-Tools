# -*- coding: utf-8 -*-
__title__ = "Active View Filters"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 08.06.2022
_____________________________________________________________________
Description:
Panel showing all filters for the Active View.
_____________________________________________________________________
Last update:
- [08.06.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- Show all filters in active view
- Make it a dockable panel
- Add functionality of original filters (visibility on/off, projection/cut overrides etc.)
_____________________________________________________________________
Author: Harley Trappitt"""                                  # Button Description shown in Revit UI


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
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent      # noinspection PyUnresolvedReferences
from Autodesk.Revit.Exceptions import InvalidOperationException         # noinspection PyUnresolvedReferences

# pyRevit
from pyrevit import revit, forms, DB, UI, script                        # import pyRevit modules. (Lots of useful features)
from pyrevit import HOST_APP, framework, coreutils, PyRevitException
from pyrevit.framework import Input, wpf, ObservableCollection
from pyrevit.forms import WPFWindow

# Custom Imports
# from Snippets._selection import get_selected_elements                 # lib import
# from Snippets._convert import convert_internal_to_m                   # lib import

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference("System")                  # Refference System.dll for import.
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentesis.

clr.AddReference("RevitServices")
import RevitServices
#from RevitServices.Persistence import DocumentManager
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# WPF Dependencies
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

# find the path of ui.xaml
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
#uidoc = HOST_APP.uidoc

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

class Reactive(ComponentModel.INotifyPropertyChanged):
    """WPF property updator base mixin"""
    PropertyChanged, _propertyChangedCaller = pyevent.make_event()

    def add_PropertyChanged(self, value):
        self.PropertyChanged += value

    def remove_PropertyChanged(self, value):
        self.PropertyChanged -= value

    def OnPropertyChanged(self, prop_name):
        if self._propertyChangedCaller:
            args = ComponentModel.PropertyChangedEventArgs(prop_name)
            self._propertyChangedCaller(self, args)

class Command(ICommand):
    def __init__(self, execute):
        self.execute = execute

    def Execute(self, parameter):
        self.execute()

    def add_CanExecuteChanged(self, handler):
        pass

    def remove_CanExecuteChanged(self, handler):
        pass

    def CanExecute(self, parameter):
        return True

class ActiveFilters(Windows.Window, Reactive):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

        self.FilterName.ItemsSource = []
        self.FilterVisibility.ItemsSource = []
        self.FilterHalfTone.ItemsSource = []
        self.FilterTransparency.ItemsSource = []

    def get_active_filters_click(self, sender, args):
        try:
            current_view = doc.ActiveView
            current_filters = current_view.GetFilters()
            #uidoc.RefreshActiveView(current_view)
            #doc.Regenerate()
            FilterName,FilterVisibility,FilterHalfTone,FilterTransparency = [],[],[],[]
            elements = []

            for f in current_filters:
                FilterVisibility.append(current_view.GetFilterVisibility(f))
                element = doc.GetElement(f)
                elements.append(element)
                FilterName.append(element.Name)
                filterObject = current_view.GetFilterOverrides(f)
                FilterTransparency.append(filterObject.Transparency)
                FilterHalfTone.append(filterObject.Halftone)

            self.FilterName.ItemsSource = FilterName
            self.FilterVisibility.ItemsSource = FilterVisibility
            self.FilterHalfTone.ItemsSource = FilterHalfTone
            self.FilterTransparency.ItemsSource = FilterTransparency

        except Exception as e:
            print e.message

    def add_filters():
        pass

    def remove_filters():
        pass

    def edit_filters():
        pass

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
#if __name__ == '__main__':
    # START CODE HERE

print(ActiveFilters.FilterName)

#                <ListView.View>
#                    <GridView AllowsColumnReorder="True">
#                        <GridViewColumn x:Name="FilterName" Header="Name" Width="Auto"/>
#                        <GridViewColumn x:Name="FilterVisibility" Header="Visibility" Width="Auto"/>
#                        <GridViewColumn x:Name="FilterHalfTone" Header="Halftone" Width="Auto"/>
#                        <GridViewColumn x:Name="FilterTransparency" Header="Transparency" Width="Auto"/>
#                    </GridView>
#                </ListView.View>

# Let's show the window (modal)
ActiveFilters().ShowDialog()

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


# AVOID  placing Transaction inside of your loops! It will drastically reduce perfomance of your script.
#t = Transaction(doc,__title__)  # Transactions are context-like objects that guard any changes made to a Revit model.

# You need to use t.Start() and t.Commit() to make changes to a Project.
#t.Start()  # <- Transaction Start

#- CHANGES TO REVIT PROJECT HERE

#t.Commit()  # <- Transaction End

# Notify user that script is complete.
#print('Script is finished.')