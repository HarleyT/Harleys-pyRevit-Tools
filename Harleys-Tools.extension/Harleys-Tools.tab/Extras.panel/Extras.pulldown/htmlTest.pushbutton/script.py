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
from System.Collections.Generic import List

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


class HtmlWindow(WPFWindow):
    def __init__(self, xaml_file_path):
        super(HtmlWindow, self).__init__(xaml_file_path)
        html_path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.webViewer.Navigate('file:///' + html_path.replace('\\', '/'))
        self.ShowDialog()

# Load and show the window
xaml_path = os.path.join(os.path.dirname(__file__), 'html_viewer.xaml')
HtmlWindow(xaml_path)



#==================================================
