import clr

clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference("RevitAPI")
clr.AddReference('RevitAPIUI')
clr.AddReference("System.Collections")
clr.AddReference('IronPython.Wpf')
clr.AddReference('System.Printing')
import System
from System.Printing import *
import Autodesk
import wpf
from System import Windows
from System.Drawing import *
from System.Windows.Forms import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit import forms, revit, DB, script, UI, framework

from System.Collections.ObjectModel import ObservableCollection
from System.ComponentModel import INotifyPropertyChanged, PropertyChangedEventArgs
from System.Windows.Input import ICommand
from System.Windows import Controls
from System import ComponentModel
import pyevent


app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

xamlfile2 = script.get_bundle_file('ui2.xaml')


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

class SheetView(Reactive):
    def __int__(self, title, checks):
        NotifyPropertyChangedBase.__init__(self)
        self.Title = title
        self.Checked = checks

class viewsetInfo(Reactive):
    def __init__(self):
        self.viewSetsa = FilteredElementCollector(doc).OfClass(ViewSheetSet).WhereElementIsNotElementType().ToElements()
        self.viewSheets = FilteredElementCollector(doc).OfClass(ViewSheet)
        viewSetnames = []

        listlength = []
        for i in self.viewSetsa:
            listlength.append(i)
        self.selInd = len(listlength) - 1

        for i in self.viewSetsa:
            viewSetnames.append(i.Name)
        viewSheetsNames = []
        for i in self.viewSheets:
            if i.CanBePrinted:
                viewSheetsNames.append(i.Title)
        self.vsnames = viewSetnames
        self.fIndex = self.selInd
        self.viewSheetN = viewSheetsNames
        self.RviewSet = self.viewSetsa
        self.CBInfo = None
        self.CBInfoChange = None

        cbs = []
        for c, s in zip(self.SheetsList1(), self.SheetCheckList1()[self.selInd]):
            cb = Controls.CheckBox()
            cb.Content = c.Title
            cb.IsChecked = s
            # cb.IsChecked = d
            cbs.append(cb)
        self.CBInfo = cbs

    def CBInfoChange1(self, index):
        cbinfo =[]
        for c, s in zip(self.SheetsList1(), self.SheetCheckList2()[index]):
            cb = Controls.CheckBox()
            cb.Content = c.Title
            cb.IsChecked = s
            # cb.IsChecked = d
            cbinfo.append(cb)
        self.CBInfoChange = cbinfo

    def SheetsList1(self):
        viewsheetR = []
        viewSheetsNames = []
        for i in self.viewSheets:
            if i.CanBePrinted:
                viewSheetsNames.append(i.Title)
                viewsheetR.append(i)
        sheetlists = map(lambda c: c, viewsheetR)
        return sheetlists


    def SheetCheckList1(self):
        #viewSetsw = FilteredElementCollector(doc).OfClass(ViewSheetSet).WhereElementIsNotElementType().ToElements()
        viewsheetR = []
        viewSheetsNames = []
        for i in self.viewSheets:
            if i.CanBePrinted:
                viewSheetsNames.append(i.Title)
                viewsheetR.append(i)
        viewSetViews = []
        viewchecksets = []
        viewSetnames = []
        for i in self.viewSetsa:
            viewSetnames.append(i.Name)
            viewsn = []
            viewinset = []
            for e in i.Views:
                viewsn.append(e.Title)
            for s in viewSheetsNames:
                if s in viewsn:
                    viewinset.append(True)
                else:
                    viewinset.append(False)
            viewSetViews.append(viewsn)
            viewchecksets.append(viewinset)
        ischeckedlist = []
        for w in viewchecksets:
            icl = map(lambda c: c, w)
            ischeckedlist.append(icl)
        return ischeckedlist

    def SheetCheckList2(self):
        viewSetsx = FilteredElementCollector(doc).OfClass(ViewSheetSet).WhereElementIsNotElementType().ToElements()
        viewSheetx = FilteredElementCollector(doc).OfClass(ViewSheet)
        #viewSetsw = FilteredElementCollector(doc).OfClass(ViewSheetSet).WhereElementIsNotElementType().ToElements()
        viewsheetR = []
        viewSheetsNames = []
        for i in viewSheetx:
            if i.CanBePrinted:
                viewSheetsNames.append(i.Title)
                viewsheetR.append(i)
        viewSetViews = []
        viewchecksets = []
        viewSetnames = []
        for i in viewSetsx:
            viewSetnames.append(i.Name)
            viewsn = []
            viewinset = []
            for e in i.Views:
                viewsn.append(e.Title)
            for s in viewSheetsNames:
                if s in viewsn:
                    viewinset.append(True)
                else:
                    viewinset.append(False)
            viewSetViews.append(viewsn)
            viewchecksets.append(viewinset)
        ischeckedlist = []
        for w in viewchecksets:
            icl = map(lambda c: c, w)
            ischeckedlist.append(icl)
        return ischeckedlist


class ViewsetWindow(Windows.Window, Reactive):
    sheetsSet = None

    def __init__(self):
        wpf.LoadComponent(self, xamlfile2)
        self.printManager = doc.PrintManager
        self.printManager.PrintRange = PrintRange.Select
        self.printManager.Apply()
        self.ViewSS = self.printManager.ViewSheetSetting

        self.vs = viewsetInfo()
        #self.sv = ViewModel()
        #self.CB1.ItemsSource = ObservableCollection[Name]()
        self.CB2.ItemsSource = self.vs.vsnames
        self.CB2.SelectedIndex = self.vs.fIndex
        self.CB1.ItemsSource = self.vs.CBInfo
        self.CB2.DropDownClosed += self.CBchangeEvent


    @property
    def ComboChange2(self):
        return self.CB2.SelectedItem

    @property
    def value(self):
        return self.IsChecked

    def CBchangeEvent(self, sender, args):
        self.vs2 = viewsetInfo()
        self.vsSelectedx = self.CB2.SelectedIndex

        for item, chk in zip(self.CB1.Items, self.vs2.SheetCheckList1()[self.vsSelectedx]):
            item.IsChecked = chk



    def selectAll_Click(self, sender, args):

        for item in self.CB1.Items:
            item.IsChecked = True

    def selectNone_Click(self, sender, args):
        for item in self.CB1.Items:
            item.IsChecked = False

    def save_Click(self, sender, args):

        vsetsel = self.CB2.SelectedItem
        for e in viewsetInfo().RviewSet:
            if e.Name == vsetsel:
                setviewcurrent = e

        printManager = doc.PrintManager
        printManager.PrintRange = PrintRange.Select
        printManager.Apply()
        ViewSS = printManager.ViewSheetSetting
        txsa = Transaction(doc)
        txsa.Start('save')
        ViewSS.CurrentViewSheetSet = setviewcurrent
        txsa.Commit()
        #txsa = Transaction(doc)
        #txsa.Start('save')
        #ViewSS.Delete()
        #txsa.Commit()
        sheet_set = DB.ViewSet()
        for item in self.CB1.Items:
            if item.IsChecked:
                for i in viewsetInfo().viewSheets:
                    if i.Title == item.Content:
                        sheet_set.Insert(i)

        txsaa = Transaction(doc)
        txsaa.Start('save')
        ViewSS.CurrentViewSheetSet.Views = sheet_set
        #ViewSS.SaveAs(str(vsetsel))
        ViewSS.Save()
        txsaa.Commit()
        viewsetInfo()
        vsx = viewsetInfo()
        vsx.SheetCheckList1()
        self.CB2.ItemsSource = vsx.vsnames
        newindex = self.CB2.SelectedIndex
        vsx.CBInfoChange1(newindex)
        self.CB1.ItemsSource = vsx.CBInfoChange

    def saveAs_Click(self, sender, args):

        saveasname = forms.GetValueWindow.show('Name', title='Name:', width=500, height=600)
        sheet_set = DB.ViewSet()
        vsetsel = self.CB2.SelectedItem
        for item in self.CB1.Items:
            if item.IsChecked:
                for i in viewsetInfo().viewSheets:
                    if i.Title == item.Content:
                        sheet_set.Insert(i)
        for e in viewsetInfo().RviewSet:
            if e.Name == vsetsel:
                setviewcurrent = e
        printManager = doc.PrintManager
        printManager.PrintRange = PrintRange.Select
        printManager.Apply()
        ViewSS = printManager.ViewSheetSetting
        txsa = Transaction(doc)
        txsa.Start('save')
        ViewSS.CurrentViewSheetSet = setviewcurrent

        ViewSS.CurrentViewSheetSet.Views = sheet_set
        ViewSS.SaveAs(str(saveasname))
        txsa.Commit()
        viewsetInfo()
        vsx = viewsetInfo()
        vsx.SheetCheckList1()
        self.CB2.ItemsSource = vsx.vsnames
        newindex = self.CB2.SelectedIndex
        vsx.CBInfoChange1(newindex)
        self.CB1.ItemsSource = vsx.CBInfoChange


    def revert_Click(self, sender, args):
        vsetsel = self.CB2.SelectedItem
        for e in viewsetInfo().RviewSet:
            if e.Name == vsetsel:
                setviewcurrent = e
        txs = Transaction(doc)
        txs.Start('rename')
        self.ViewSS.CurrentViewSheetSet = setviewcurrent
        self.ViewSS.Revert()
        txs.Commit()
        newindex = self.CB2.SelectedIndex
        viewsetInfo()
        vsx = viewsetInfo()
        vsx.SheetCheckList1()
        self.CB2.ItemsSource = vsx.vsnames
        vsx.CBInfoChange1(newindex)
        self.CB1.ItemsSource = vsx.CBInfoChange
        self.CB2.SelectedIndex = newindex


    def rename_Click(self, sender, args):
        rename = forms.GetValueWindow.show('Name', title='Name:', width=500, height=600)
        vsetsel = self.CB2.SelectedItem
        for e in viewsetInfo().RviewSet:
            if e.Name == vsetsel:
                setviewcurrent = e
        txs = Transaction(doc)
        txs.Start('rename')
        self.ViewSS.CurrentViewSheetSet = setviewcurrent
        self.ViewSS.Rename(rename)
        txs.Commit()
        newindex = self.CB2.SelectedIndex
        viewsetInfo()
        vsx = viewsetInfo()
        vsx.SheetCheckList1()
        self.CB2.ItemsSource = vsx.vsnames
        vsx.CBInfoChange1(newindex)
        self.CB1.ItemsSource = vsx.CBInfoChange
        self.CB2.SelectedIndex = newindex
    def delete_Click(self, sender, args):
        vsetsel = self.CB2.SelectedItem
        for e in viewsetInfo().RviewSet:
            if e.Name == vsetsel:
                setviewcurrent = e
        txs = Transaction(doc)
        txs.Start('rename')
        self.ViewSS.CurrentViewSheetSet = setviewcurrent
        self.ViewSS.Delete()
        txs.Commit()
        newindex = self.CB2.SelectedIndex - 1
        viewsetInfo()
        vsx = viewsetInfo()
        vsx.SheetCheckList1()
        self.CB2.ItemsSource = vsx.vsnames

        vsx.CBInfoChange1(newindex)
        self.CB1.ItemsSource = vsx.CBInfoChange
        self.CB2.SelectedIndex = newindex


    def okay2(self, sender, args):
        sheet_set = DB.ViewSet()
        for item in self.CB1.Items:
            if item.IsChecked:
                for i in viewsetInfo().viewSheets:
                    if i.Title == item.Content:
                        sheet_set.Insert(i)

        self.returnvalue(sheet_set)

        self.Close()
        return ViewsetWindow.sheetsSet

    def cancel2(self, sender, args):
        self.Close()