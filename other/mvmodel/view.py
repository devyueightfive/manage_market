import sys

from PyQt5 import QtCore, QtWidgets

from other.mvmodel.model import ModelForTree


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.initUI()
        self.resize(600, 800)

    def initUI(self):
        self.treeView = QtWidgets.QTreeView(parent=self)
        self.treeView.setModel(self.model)
        self.treeView.expandAll()
        self.treeView.setGeometry(QtCore.QRect(10, 10, 430, 200))
        selectionModel = self.treeView.selectionModel()
        selectionModel.selectionChanged.connect(self.selectionChangedSlot)

    def selectionChangedSlot(self, newSelection, oldSelection):
        index = self.treeView.selectionModel().currentIndex()
        selectedText = str(index.data(QtCore.Qt.DisplayRole))
        level = 1
        seekRoot = index
        while seekRoot.parent() != QtCore.QModelIndex():
            level += 1
            seekRoot = seekRoot.parent()
            print(f"{level}:{seekRoot}")
        print(seekRoot.parent())
        title = f"{selectedText}:{level}"
        self.setWindowTitle(title)

    def connectTriger(self):
        self.model.setWindowTriger(self)

    def showWindowTitle(self, text):
        self.setWindowTitle(text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    model = ModelForTree()
    w = MainWindow(model)
    w.show()
    sys.exit(app.exec_())
