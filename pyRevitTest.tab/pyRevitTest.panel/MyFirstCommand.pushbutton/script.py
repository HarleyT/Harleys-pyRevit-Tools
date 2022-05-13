# Select ACCDocs folder in AML Project
# Select .rfa file to edit
# Select .dwg to import into .rfa
# Reload selected Generic Models
from pyrevit import revit, forms

doc = revit.doc
user = doc.Username
filepath = "C:\Users" + user + "\ACCDocs\GHD Services Pty Ltd\12545014 - AML Detail Design 15MTPA\Project Files\02 - DELIVERY"

ACCDocs_dict = {}

for family in FilteredElementCollector(doc).OfClass(typeof(GenericModel)).ToElements():

    if family.FamilyCategory:

        ACCDocs_dict[

            "%s: %s" % (family.FamilyCategory.Name, family.Name)

        ] = family

if ACCDocs_dict:

    selected_families = forms.SelectFromList.show(

        sorted(ACCDocs_dict.keys()),

        title="Select Families",

        multiselect=True,

    )

    if selected_families:

        for idx, family in enumerate([ACCDocs_dict[x] for x in selected_families]):

            print (family.Name)
            
            print (family)