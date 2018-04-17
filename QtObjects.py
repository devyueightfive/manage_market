from PyQt5.QtCore import QObject, pyqtSignal


class ValueWithSignal(QObject):
    """Object with attributes (value, changed)\n
    value: for storing data\n
    changed: Qt Signal, for informing of 'value' change
    """
    changed = pyqtSignal()

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value

    def __str__(self):
        return f"{self.value}"
