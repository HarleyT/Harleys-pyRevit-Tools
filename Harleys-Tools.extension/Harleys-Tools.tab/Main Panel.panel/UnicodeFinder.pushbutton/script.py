import clr
clr.AddReference('RevitAPI')
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter
from pyrevit import revit, script, UI
import re
import wpf
#xamlfile = script.get_bundle_file('ui.xaml')
from System import Windows


# Import the XAML layout
#clr.AddReference('PresentationFramework')
#from System.Windows import Application, Window

# Define a regular expression pattern to match Unicode characters
unicode_pattern = re.compile('[^\x00-\x7F]+')

# Function to check if a string contains Unicode characters
def contains_unicode(text):
    return bool(unicode_pattern.search(text))

# Function to search for Unicode characters in sheet numbers
def search_sheets_for_unicode(sender, e):
    # Get all sheets in the current Revit project
    sheets_collector = FilteredElementCollector(revit.doc).OfCategory(BuiltInCategory.OST_Sheets)
    sheets = list(sheets_collector)

    # Initialize a list to store sheets with Unicode characters
    sheets_with_unicode = []

    # Iterate through each sheet and check its sheet number
    for sheet in sheets:
        sheet_number = sheet.get_Parameter(BuiltInParameter.SHEET_NUMBER).AsString()
        if contains_unicode(sheet_number):
            sheets_with_unicode.append(sheet_number)

    # Display the sheets with Unicode characters in the resultTextBox
    if sheets_with_unicode:
        resultTextBox.Text = "\n".join(sheets_with_unicode)
    else:
        resultTextBox.Text = "No sheets with Unicode characters found."

# Create the main window
class MainWindow(Window.Window):
    def __init__(self):
        wpf.LoadComponent(self, 'ui.xaml')
        self.searchButton.Click += self.search_sheets_for_unicode

if __name__ == '__main__':
    Application().Run(MainWindow())
