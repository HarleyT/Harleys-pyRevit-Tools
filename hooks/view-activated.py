from pyrevit import forms
from pyrevit import EXEC_PARAMS

forms.alert(EXEC_PARAMS.event_args.CurrentActiveView.Name)