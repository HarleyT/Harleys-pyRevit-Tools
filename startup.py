# -*- coding: UTF-8 -*-
import System
import os.path as op
from pyrevit import HOST_APP, framework, coreutils, PyRevitException
from pyrevit import revit, DB, UI
from pyrevit import forms, script
from pyrevit.framework import wpf, ObservableCollection

sample_panel_id = "3110e336-f81c-4927-87da-4e0d30d4d64b"

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
    panel_source = op.join(op.dirname(__file__), "DockablePanel.xaml")
    panel_title = "Dockable Pane Sample"
    panel_id = sample_panel_id
    def __init__(self):
        wpf.LoadComponent(self, self.panel_source)
        self.thread_id = framework.get_current_thread_id()

        self.FilterName.ItemsSource = []
        self.FilterVisibility.ItemsSource = []
        self.FilterHalfTone.ItemsSource = []
        self.FilterTransparency.ItemsSource = []

    def get_active_filters_click(self, sender, args):
        try:
            doc = __revit__.ActiveUIDocument.Document
            current_view = doc.ActiveView
            current_filters = current_view.GetFilters()
            #uidoc.RefreshActiveView(current_view)
            #doc.Regenerate()
            FilterName,FilterVisibility,FilterHalfTone,FilterTransparency = [],[],[],[]
            elements = []

            for f in current_filters:
                FilterVisibility.append(current_view.GetFilterVisibility(f))
                element = doc.GetElement(f)
                elements.append(element)
                FilterName.append(element.Name)
                filterObject = current_view.GetFilterOverrides(f)
                FilterTransparency.append(filterObject.Transparency)
                FilterHalfTone.append(filterObject.Halftone)

            self.FilterName.ItemsSource = FilterName
            self.FilterVisibility.ItemsSource = FilterVisibility
            self.FilterHalfTone.ItemsSource = FilterHalfTone
            self.FilterTransparency.ItemsSource = FilterTransparency

        except Exception as e:
            print e.message

    def apply_filters_click(self, sender, args):
        try:
            self.get_active_filters_click().current_view.SetFilterVisibility = self.get_active_filters_click().FilterVisibility.ItemsSource
        except Exception as e:
            print e.message


registered_panel = register_dockable_panel(DockableExample)

def idling_eventhandler(sender, args):
    try: dockable_pane = UI.DockablePane(UI.DockablePaneId(System.Guid(sample_panel_id)))
    except: return

    global selected

    if HOST_APP.uidoc and dockable_pane.IsShown():
        try:
            doc = __revit__.ActiveUIDocument.Document
            current_view = doc.ActiveView
            if current_view:
                if current_view != selected:
                    selected = current_view
                    registered_panel.get_active_filters_click()
            else:
                if selected:
                    selected = []
                    registered_panel.get_active_filters_click()
        except Exception as e:
            print e.message

HOST_APP.uiapp.Idling += \
    framework.EventHandler[UI.Events.IdlingEventArgs](idling_eventhandler)