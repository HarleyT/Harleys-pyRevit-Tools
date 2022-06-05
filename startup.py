# -*- coding: UTF-8 -*-
import System
import os.path as op
from pyrevit import HOST_APP, framework, coreutils, PyRevitException
from pyrevit import revit, DB, UI
from pyrevit import forms, script
from pyrevit.framework import wpf, ObservableCollection

sample_panel_id = "1458b7cb-4dbe-4a8e-bad3-837e14b0a1cb"

selected = []



class _WPFPanelProvider(UI.IDockablePaneProvider):
    def __init__(self, panel_type, default_visible=True):
        self._panel_type = panel_type
        self._default_visible = default_visible
        self.panel = self._panel_type()

    def SetupDockablePane(self, data):
        data.FrameworkElement = self.panel
        data.VisibleByDefault = self._default_visible

def register_dockable_panel(panel_type, default_visible=True):
    if not issubclass(panel_type, forms.WPFPanel):
        raise PyRevitException(
            "Dockable pane must be a subclass of forms.WPFPanel"
            )

    panel_uuid = coreutils.Guid.Parse(panel_type.panel_id)
    dockable_panel_id = UI.DockablePaneId(panel_uuid)
    panel_provider = _WPFPanelProvider(panel_type, default_visible)
    HOST_APP.uiapp.RegisterDockablePane(
        dockable_panel_id,
        panel_type.panel_title,
        panel_provider
        ) 
    return panel_provider.panel

class DockableExample(forms.WPFPanel):
    panel_source = op.join(op.dirname(__file__), "DockablePaneSample.xaml")
    panel_title = "Dockable Pane Sample"
    panel_id = sample_panel_id
    def __init__(self):
        wpf.LoadComponent(self, self.panel_source)
        self.thread_id = framework.get_current_thread_id()
        self.selected_lb.ItemsSource = []

    
    def update_list(self):
        try:
            template_list = [forms.TemplateListItem(s.IntegerValue) for s in selected]
            self.selected_lb.ItemsSource = ObservableCollection[forms.TemplateListItem](template_list)
        except Exception as e:
            print e.message


registered_panel = register_dockable_panel(DockableExample)

def idling_eventhandler(sender, args):
    try: dockable_pane = UI.DockablePane(UI.DockablePaneId(System.Guid(sample_panel_id)))
    except: return

    global selected

    if HOST_APP.uidoc and dockable_pane.IsShown():
        try:
            ids = sorted(HOST_APP.uidoc.Selection.GetElementIds())
            if ids:
                if ids != selected:
                    selected = ids
                    registered_panel.update_list()
            else:
                if selected:
                    selected = []
                    registered_panel.update_list()
        except Exception as e:
            print e.message

HOST_APP.uiapp.Idling += \
    framework.EventHandler[UI.Events.IdlingEventArgs](idling_eventhandler)