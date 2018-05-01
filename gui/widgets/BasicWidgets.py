from PyQt5 import QtWidgets, QtGui


class SComboBox(QtWidgets.QComboBox):
    def __init__(self, data_source, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_source = data_source
        self.update_items(data_source)
        self.setCurrentIndex(-1)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self.update_items(self.data_source)
        super().mousePressEvent(e)
        self.setCurrentIndex(-1)

    def update_items(self, data_source):
        """Update data source"""
        self.clear()
        for text in sorted(data_source):
            self.addItem(text)


# Class Bar represent bind of QLabel and QComboBox
class Bar:

    def __init__(self, label_text, combo_list, label_x, label_y, combo_x, combo_y,
                 parent, enabled=True, combo_width=100, combo_height=22):
        self.label = QtWidgets.QLabel(parent)
        self.label.setText(label_text)
        self.label.move(label_x, label_y)
        self.combo = SComboBox(data_source=combo_list, parent=parent)
        self.combo.setGeometry(combo_x, combo_y, combo_width, combo_height)
        self.set_enabled(enabled)

    def set_enabled(self, enabled):
        self.combo.setEnabled(enabled)
        self.label.setEnabled(enabled)


# Class Bar represent bind of QLabel and QComboBox
class TextLine:

    def __init__(self, label_text, text, label_x, label_y, text_x, text_y,
                 parent, enabled=True, text_width=100, text_height=22):
        self.label = QtWidgets.QLabel(parent)
        self.label.setText(label_text)
        self.label.move(label_x, label_y)
        self.text_edit = QtWidgets.QLineEdit(parent)
        self.text_edit.setText(text)
        self.text_edit.move(text_x, text_y)
        self.text_edit.resize(text_width, text_height)
        self.set_enabled(enabled)

    def set_enabled(self, enabled):
        self.label.setEnabled(enabled)
        self.text_edit.setEnabled(enabled)


