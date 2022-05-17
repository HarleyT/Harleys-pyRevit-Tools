# Select ACCDocs folder in AML Project
# Select .rfa file to edit
# Select .dwg to import into .rfa
# Reload selected Generic Models
from pyrevit import revit, forms
import clr

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
app = DocumentManager.Instance.CurrentUIApplication.Application

doc = revit.doc
user = app.Username
filepath = "C:\Users" + user + "\ACCDocs\GHD Services Pty Ltd\12545014 - AML Detail Design 15MTPA\Project Files\02 - DELIVERY"

family_dict = {}

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