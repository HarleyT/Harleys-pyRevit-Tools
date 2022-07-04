# dependencies
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

# find the path of ui.xaml
from pyrevit import UI
from pyrevit import script
xamlfile = script.get_bundle_file('ui.xaml')

# import WPF creator and base Window
import wpf
from System import Windows

doc = __revit__.ActiveUIDocument.Document

class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

    def say_hello(self, sender, args):
        name = self.textbox.Text
        UI.TaskDialog.Show(
            "Hello World",
            "Hello {}".format(name or "World!"),
            nameList
            )

current_view = doc.ActiveView
view_filters = {}

filters = current_view.GetFilters()

elements, elementName, visibilities, listtrans, listhalf = [],[],[],[],[]
visibilitiesList, elementList, nameList, transList, halfList = [],[],[],[],[]

for f in filters:
    #if element:
    #    view_filters[
    #        "%s: %s" % (element.Name, visibilities)
    #    ] = elements

    visibilities.append(current_view.GetFilterVisibility(f))
    element=doc.GetElement(f)
    elements.append(element)
    elementName.append(element.Name)
    filterObject = current_view.GetFilterOverrides(f)
    listtrans.append(filterObject.Transparency)
    listhalf.append(filterObject.Halftone)

		
transList.Add(listtrans)
halfList.Add(listhalf)
visibilitiesList.append(visibilities)
elementList.append(elements)
nameList.append(elementName)

# Let's show the window (modal)
MyWindow().ShowDialog()