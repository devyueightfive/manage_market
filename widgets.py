from PyQt5 import QtWidgets, QtGui, QtChart

import settings
from wallets2 import Wallets


class PublicChart(QtChart.QChart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init()

    def init(self):
        settings.public_pair_trades.changed.connect(self.update_series)

    def update_series(self):
        # print("chart ", settings.public_pair_trades.value)
        self.removeAllSeries()
        trade_series = QtChart.QLineSeries()
        trade_series.setColor(QtGui.QColor().fromRgb(0, 255, 0))
        if len(settings.public_pair_trades.value) > 0:
            series = []
            for v in settings.public_pair_trades.value:
                date = int(v['timestamp']) * 1000
                value = float(v['price'])
                trade_series.append(date, value)
                series.append((date, value))
            # print(series)
            self.addSeries(trade_series)
            self.setTitle(f"Data from {settings.selected_public_market}")
            trade_series.setName(settings.selected_public_pair)
        else:
            self.setTitle("<market name>")
            trade_series.setName("<coin_pair>")
        self.createDefaultAxes()
        axis_x = QtChart.QDateTimeAxis()
        axis_x.setFormat("dd-MMM hh:mm")
        self.setAxisX(axis_x, trade_series)


class SComboBox(QtWidgets.QComboBox):
    def __init__(self, data_source, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_source = data_source
        self.update_items(data_source)
        self.setCurrentIndex(-1)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        print(f"source = {self.data_source}")
        self.update_items(self.data_source)
        super().mousePressEvent(e)
        self.setCurrentIndex(-1)

    def update_items(self, data_source):
        self.clear()
        for text in data_source:
            self.addItem(text)


# Class Bar represent bind of QLabel and QComboBox
class Bar:
    def __init__(self, label_text, combo_list, label_x, label_y, combo_x, combo_y, enabled, parent):
        self.label = QtWidgets.QLabel(parent=parent)
        self.label.setText(label_text)
        self.label.move(label_x, label_y)
        self.combo = SComboBox(data_source=combo_list, parent=parent)
        self.combo.setGeometry(combo_x, combo_y, 80, 20)
        self.set_enabled(enabled)

    def set_enabled(self, enabled):
        self.combo.setEnabled(enabled)
        self.label.setEnabled(enabled)


# Class Bar represent bind of QLabel and QComboBox
class TextLine:
    def __init__(self, label_text, text, label_x, label_y, text_x, text_y, text_w, enabled, parent):
        self.label = QtWidgets.QLabel(parent=parent)
        self.label.setText(label_text)
        self.label.move(label_x, label_y)
        self.text_edit = QtWidgets.QLineEdit(parent=parent)
        self.text_edit.setText(text)
        self.text_edit.move(text_x, text_y)
        self.text_edit.resize(text_w, 20)
        self.set_enabled(enabled)

    def set_enabled(self, enabled):
        self.label.setEnabled(enabled)
        self.text_edit.setEnabled(enabled)


class AddWalletWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.set_general_options()
        self.set_widgets()

    def set_general_options(self):  # general options for the window
        def center(w=self):
            cp = QtWidgets.QDesktopWidget().availableGeometry().center()
            qr = w.frameGeometry()
            qr.moveCenter(cp)
            w.move(qr.topLeft())

        self.resize(530, 200)
        self.setWindowTitle('Add Wallet ...')
        center()

    def set_widgets(self):
        wallet_text_bar = TextLine('Wallet name :', '', 20, 30, 120, 30, 130, True, self)
        market_text_bar = TextLine('Market address :', '', 280, 30, 380, 30, 130, True, self)
        key_text_bar = TextLine('Key :', '', 20, 70, 120, 70, 390, True, self)
        sign_text_bar = TextLine('Sign :', '', 20, 110, 120, 110, 390, True, self)
        save_button = QtWidgets.QPushButton('Save', self)
        save_button_width = save_button.width()
        save_button.move(int((self.width() - save_button_width) / 2), 150)

        # actions
        def on_push_save():
            wallet_to_save = {'name': wallet_text_bar.text_edit.text(),
                              'market': market_text_bar.text_edit.text(),
                              'key': key_text_bar.text_edit.text(),
                              'sign': sign_text_bar.text_edit.text(),
                              'robots': {}}
            Wallets.add_wallet(wallet_to_save)
            # global wallet_names
            settings.names_of_wallets.clear()
            settings.names_of_wallets.extend(Wallets.get_list_of_wallets().value)
            self.close()

        # bind actions with button
        save_button.clicked.connect(on_push_save)


class DeleteWalletWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.set_general_options()
        self.set_widgets()

    def set_general_options(self):  # general options for the window
        def center(w=self):
            cp = QtWidgets.QDesktopWidget().availableGeometry().center()
            qr = w.frameGeometry()
            qr.moveCenter(cp)
            w.move(qr.topLeft())

        self.resize(250, 120)
        self.setWindowTitle('Delete Wallet ...')
        center()

    def set_widgets(self):
        # global wallet_names
        wallet_bar = Bar('Wallet name :', settings.names_of_wallets, 20, 30, 120, 30, True, self)
        save_button = QtWidgets.QPushButton('Delete', self)
        save_button_width = save_button.width()
        save_button.move(int((self.width() - save_button_width) / 2), 70)

        # actions
        def on_push_delete():
            Wallets.delete_wallet_by_name(wallet_bar.combo.currentText())
            # global wallet_names
            settings.names_of_wallets.clear()
            settings.names_of_wallets.extend(Wallets.get_list_of_wallets().value)
            self.close()

        # bind actions with button
        save_button.clicked.connect(on_push_delete)
