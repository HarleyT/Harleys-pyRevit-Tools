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

from Autodesk.Revit import DB

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

viewsheetsets = DB.FilteredElementCollector(revit.doc)\
                    .OfClass(framework.get_type(DB.ViewSheetSet))\
                    .WhereElementIsNotElementType()\
                    .ToElements()

viewsets = []

for el in viewsheetsets:
    viewsets.append(el)

sheetsetname = 'ViewPrintSet'

# Get printmanager / viewsheetsetting
printmanager = revit.doc.PrintManager
printmanager.PrintRange = DB.PrintRange.Select
viewsheetsetting = printmanager.ViewSheetSetting


class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

    def show_viewsets(self, sender, args):
        UI.TaskDialog.Show(
            "Hello World",
            "{}".format(viewsets)
            )
    # event handlers
    def sheetlist_changed(self, sender, args):
        print_settings = None
        tblocks = revit.query.get_elements_by_categories(
            [DB.BuiltInCategory.OST_TitleBlocks],
            doc=self.selected_doc
        )
        if self.selected_schedule and self.selected_print_setting:
            if self.selected_print_setting.allows_variable_paper:
                sheet_printsettings = self._get_sheet_printsettings(tblocks)
                self.show_element(self.sheetopts_wp)
                self.show_element(self.psettingcol)
                self._scheduled_sheets = [
                    ViewSheetListItem(
                        view_sheet=x,
                        view_tblock=self._find_sheet_tblock(x, tblocks),
                        print_settings=sheet_printsettings.get(
                            x.SheetNumber,
                            None))
                    for x in self._get_ordered_schedule_sheets()
                    ]
            else:
                print_settings = self.selected_print_setting.print_settings
                self.hide_element(self.sheetopts_wp)
                self.hide_element(self.psettingcol)
                self._scheduled_sheets = [
                    ViewSheetListItem(
                        view_sheet=x,
                        view_tblock=self._find_sheet_tblock(x, tblocks),
                        print_settings=[print_settings])
                    for x in self._get_ordered_schedule_sheets()
                    ]
        self._update_combine_option()
        # self._update_index_slider()
        self.options_changed(None, None)

# let's show the window (modal)
MyWindow().ShowDialog()