# -*- coding: utf-8 -*-
__title__   = "9.02 - Create Sheets and Viewports"
__doc__ = """Date    = 08.05.2024
_____________________________________________________________________
Description:
Learn how to create ViewSheet and Viewports with Revit API:
_____________________________________________________________________
Author: Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
from Autodesk.Revit.DB import *

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document


# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝

# 👇 FUNCTION
def get_titleblocks_from_sheet(doc, sheet):
    # type:(Document, ViewSheet) -> list
    """Function to get TitleBlocks from the given ViewSheet.
    :return:      Return TitleBlock from provided Sheet"""

    # RULE ARGUMENTS
    rule_value         = sheet.SheetNumber
    param_sheet_number = ElementId(BuiltInParameter.SHEET_NUMBER)
    f_pvp              = ParameterValueProvider(param_sheet_number)
    evaluator          = FilterStringEquals()

    # CREATE A RULE (Method has changed in Revit API in 2022)
    f_rule = FilterStringRule(f_pvp, evaluator, rule_value)        # RVT 2022+
    tb_filter = ElementParameterFilter(f_rule)

    # GET TITLEBLOCKS
    tb = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks) \
        .WhereElementIsNotElementType().WherePasses(tb_filter).FirstElement()

    return tb


def get_view_paper_size(view):
    """Get View's CropBox size in Paperscale
    :return tuple (W,H)"""
    if view.CropBoxActive:
        # CropBox Size
        BB = view.CropBox

        # Get Model H/W Size
        W = BB.Max.X - BB.Min.X #feet
        H = BB.Max.Y - BB.Min.Y #feet

        # Convert To Paper Size (divide by View Scale)
        W = W / view.Scale
        H = H / view.Scale

        return (W,H)



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================



#📰 Get TitleBlocks
all_titleblocks = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks)\
    .WhereElementIsElementType().ToElements()
default_title_block_id = doc.GetDefaultFamilyTypeId(ElementId(BuiltInCategory.OST_TitleBlocks))

#🔓 Start Transaction
t= Transaction(doc, 'Create New Sheet')
t.Start() #🔓

#📰 Create Sheet
new_sheet = ViewSheet.Create(doc, default_title_block_id)
print('Created New Sheet: {} - {}'.format(new_sheet.SheetNumber, new_sheet.Name))

#👉 Get Views
elev = doc.GetElement(ElementId(395398))
cros = doc.GetElement(ElementId(395407))
plan = doc.GetElement(ElementId(395416))


#📏 Get TitleBlock Size
titleblock = get_titleblocks_from_sheet(doc, new_sheet)
# titleblock_typ = doc.GetElement(titleblock.GetTypeId())
tb_W = titleblock.get_Parameter(BuiltInParameter.SHEET_WIDTH).AsDouble()  # In Feet
tb_H = titleblock.get_Parameter(BuiltInParameter.SHEET_HEIGHT).AsDouble() # In Feet

#📏 Get View Sizes
elev_WH = get_view_paper_size(elev)
cros_WH = get_view_paper_size(cros)
plan_WH = get_view_paper_size(plan)


# ⏺️ Define Viewport positions
# pt_elev = XYZ(-1.00, 0.65, 0)
# pt_cros = XYZ(-0.75, 0.65, 0)
# pt_plan = XYZ(-1.00, 0.25, 0)

seg = -tb_W/4
pt_elev = XYZ(seg  , tb_H/2, 0 )
pt_cros = XYZ(seg*2, tb_H/2, 0)
pt_plan = XYZ(seg*3, tb_H/2, 0)


# 🖼️ Place Views on Sheets (Viewport.Create)
if Viewport.CanAddViewToSheet(doc, new_sheet.Id, elev.Id):
    viewport_elev = Viewport.Create(doc, new_sheet.Id, elev.Id, pt_elev)
    viewport_cros = Viewport.Create(doc, new_sheet.Id, cros.Id, pt_cros)
    viewport_plan = Viewport.Create(doc, new_sheet.Id, plan.Id, pt_plan)


t.Commit() #🔒







# ╦═╗╔═╗╦  ╦╦╔╦╗  ╔═╗╦ ╦╔╦╗╦ ╦╔═╗╔╗╔  ╔═╗╦ ╦╔═╗╦  ╦
# ╠╦╝║╣ ╚╗╔╝║ ║   ╠═╝╚╦╝ ║ ╠═╣║ ║║║║  ╚═╗╠═╣║╣ ║  ║
# ╩╚═╚═╝ ╚╝ ╩ ╩   ╩   ╩  ╩ ╩ ╩╚═╝╝╚╝  ╚═╝╩ ╩╚═╝╩═╝╩═╝
# elev = doc.GetElement(ElementId(395398))
#
# # Calculate Outline Size
# outline = elev.Outline
#
# v_min = outline.Min
# v_max = outline.Max
#
# W = v_max.U - v_min.U #feet
# H = v_max.V - v_min.V #feet
#
# w_cm = UnitUtils.ConvertFromInternalUnits(W, UnitTypeId.Centimeters)
# h_cm = UnitUtils.ConvertFromInternalUnits(H, UnitTypeId.Centimeters)
#
# print('Outline: {}, {}'.format(w_cm, h_cm))
#
#
#
#
# # CropBox Size
# BB = elev.CropBox
#
# # Get Model H/W Size
# W = BB.Max.X - BB.Min.X #feet
# H = BB.Max.Y - BB.Min.Y #feet
#
# # Convert To Paper Size (divide by View Scale)
# W = W / elev.Scale
# H = H / elev.Scale
#
# # Convert to CM
# w_cm = UnitUtils.ConvertFromInternalUnits(W, UnitTypeId.Centimeters)
# h_cm = UnitUtils.ConvertFromInternalUnits(H, UnitTypeId.Centimeters)
#
# print('CropBox cm: {}, {}'.format(w_cm, h_cm))








