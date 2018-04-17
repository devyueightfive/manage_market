from PyQt5 import QtCore, QtGui


class ModelForTree(QtGui.QStandardItemModel):
    def __init__(self, *args):
        super().__init__(*args)
        self.inintData()

    def inintData(self):
        rootNode = self.invisibleRootItem()
        americaItem = QtGui.QStandardItem("America")
        europeItem = QtGui.QStandardItem("Europe")
        rootNode.appendRow(americaItem)
        rootNode.appendRow(europeItem)
        mexicoItem = QtGui.QStandardItem("Mexico")
        usaItem = QtGui.QStandardItem("USA")
        americaItem.appendRow(mexicoItem)
        americaItem.appendRow(usaItem)
        bostonItem = QtGui.QStandardItem("Boston")
        usaItem.appendRow(bostonItem)
        italyItem = QtGui.QStandardItem("Italy")
        europeItem.appendRow(italyItem)
        romeItem = QtGui.QStandardItem("Rome")
        venusItem = QtGui.QStandardItem("Venus")
        italyItem.appendRow(venusItem)
        italyItem.appendRow(romeItem)


class Model(QtCore.QAbstractTableModel):
    ROWS = 2
    COLUMNS = 3
    editCompleted = QtCore.pyqtSignal([str], name="EditCompleted")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timerHit)
        self.timer.start()
        self.__data = (['', '', ''], ['', '', ''])

    def timerHit(self):
        index = self.createIndex(1, 1)
        self.dataChanged.emit(index, index, [QtCore.Qt.DisplayRole])

    def rowCount(self, parent=None, *args, **kwargs):
        return self.ROWS

    def columnCount(self, parent=None, *args, **kwargs):
        return self.COLUMNS

    def data(self, QModelIndex, role=None):
        row = QModelIndex.row()
        column = QModelIndex.column()
        if role == QtCore.Qt.DisplayRole:
            return self.__data[QModelIndex.row()][QModelIndex.column()]
        elif role == QtCore.Qt.FontRole:
            if row == 0 and column == 0:
                boldFont = QtGui.QFont()
                boldFont.setBold(True)
                return boldFont
        elif role == QtCore.Qt.BackgroundRole:
            if row == 1 and column == 2:
                redBackground = QtGui.QBrush(QtCore.Qt.red)
                return redBackground
        elif role == QtCore.Qt.TextAlignmentRole:
            if row == 1 and column == 1:
                return QtCore.Qt.AlignRight + QtCore.Qt.AlignCenter
        elif role == QtCore.Qt.CheckStateRole:
            if row == 1 and column == 0:
                return QtCore.Qt.Checked
        else:
            return QtCore.QVariant()

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if Qt_Orientation == QtCore.Qt.Horizontal:
                return {'0': 'first',
                        '1': 'second',
                        '2': 'third'
                        }.get(str(p_int), "unnamed")
            else:
                return p_int
        return QtCore.QVariant()

    def setWindowTriger(self, window):
        self.editCompleted.connect(window.showWindowTitle)

    def setData(self, QModelIndex, Any, role=None):
        if role == QtCore.Qt.EditRole:
            self.__data[QModelIndex.row()][QModelIndex.column()] = str(Any)
            result = ''
            for i in range(self.ROWS):
                for j in range(self.COLUMNS):
                    result = f"{result}#{self.__data[i][j]}"
            self.editCompleted.emit(result)
        return True

    def flags(self, QModelIndex):
        return QtCore.Qt.ItemIsEditable | QtCore.QAbstractTableModel.flags(self, QModelIndex)
