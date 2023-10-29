# -*- coding: utf-8 -*-
"""Get Selected Elements
"""

# Imports
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import Selection, ObjectType, PickBoxStyle

# Variables
uidoc = __revit__.ActiveUIDocument          #type: UIDocument
doc = __revit__.ActiveUIDocument.Document   #type: Document

selection = uidoc.Selection                 #type: Selection


# Functions
def get_selected_elements(uidoc):
    """Function to get selected elements in Revit UI."""
    doc = uidoc.Document
    return [doc.GetElement(e_id) for e_id in selection.GetElementIds()]


def pick_elements_by_rect():
    """Function to get selected elements in Revit UI based on rectangle selection."""
    return [selection.PickElementsByRectangle('Rectangle Selection: Select some elements.')]

def picked_object_single(uidoc):
    """Function to get a picked object(singular)"""
    doc = uidoc.Document
    ref_picked_object = selection.PickObject(ObjectType.Element)
    return doc.GetElement(ref_picked_object)


def picked_object_multi(uidoc):
    """Function to get picked objects(multiple)"""
    doc = uidoc.Document
    ref_picked_objects = selection.PickObjects(ObjectType.Element)
    picked_objects = [doc.GetElement(ref) for ref in ref_picked_objects]
    for el in picked_objects:
        print(el)

def picked_point(uidoc):
    """Function to get picked point"""
    doc = uidoc.Document
    picked_pt = selection.PickPoint()
    print(picked_pt)
    print(type(picked_pt))  # XYZ type


def picked_box(uidoc):
    """Function to pick object via box selection"""
    doc = uidoc.Document
    pb_style = PickBoxStyle.Directional
    pick_box = selection.PickBox(pb_style, 'Select 2 points for pick box')
    print(pick_box.Min)
    print(pick_box.Max)