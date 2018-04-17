from PyQt5 import QtWidgets

from wallet.wallet_model import OrderModel


class OrdersTable(QtWidgets.QTableWidget):
    ROWS = 0
    COLUMNS = 8

    def __init__(self, *args):
        super().__init__(*args)
        self.setColumnCount(self.COLUMNS)
        self.setRowCount(self.ROWS)
        self.setHorizontalHeaderLabels(OrderModel.attributes)

    def __fillRow(self, order: dict, row: int):
        for index in range(len(OrderModel.attributes)):
            self.setItem(row, index,
                         QtWidgets.QTableWidgetItem(
                             str(order.get(OrderModel.attributes[index], ''))))

    def updateView(self, orders: dict):
        self.clear()
        self.ROWS = len(orders)
        self.setRowCount(self.ROWS)
        row = 0
        for k, v in orders.items():
            self.setItem(row, 0, k)
            self.__fillRow(v, row)
            row += 1
