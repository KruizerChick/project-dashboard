from django.contrib.admin import widgets
from django.forms.widgets import Textarea


# Custom forms
class MiniTextarea(Textarea):
    """
    Vertically shorter version of the default Django textarea widget.
    """
    rows = 2

    def __init__(self, attrs=None):
        super(MiniTextarea, self).__init__(
            {'rows': self.rows})


class MiniAdminTextarea(widgets.AdminTextareaWidget):
    """
    Vertically shorter version of the admin textarea widget.
    """
    rows = 2

    def __init__(self, attrs=None):
        super(MiniAdminTextarea, self).__init__(
            {'rows': self.rows})
