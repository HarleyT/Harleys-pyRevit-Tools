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

class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

    def say_hello(self, sender, args):
        name = self.textbox.Text
        UI.TaskDialog.Show(
            "Hello World",
            "Hello {}".format(name or "World!")
            )

# Let's show the window (modal)
MyWindow().ShowDialog()