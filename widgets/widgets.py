from PyQt5 import QtWidgets, QtGui, QtCore

import shared_data
from wallet.wallets import Wallets
from widgets.CoinInfo import CoinInfoWidget
from widgets.LiveChart import LiveChart
from widgets.OrderView import OrdersTable


class InfoWidget:
    def __init__(self, parent):
        self.public_info_box = QtWidgets.QGroupBox('Info', parent)
        self.coin_info_widget = CoinInfoWidget(parent=self.public_info_box)
        self.live_chart_widget = LiveChart(parent=self.public_info_box)
        self.public_pair = Bar('Pair', shared_data.supported_pairs, 20, 50, 70, 50, True, self.public_info_box)
        self.public_market = Bar('Market', shared_data.supported_markets, 20, 20, 70, 20, True, self.public_info_box)
        self.init_widget()
        self.set_slots()

    def init_widget(self):
        # public_box
        self.public_info_box.setGeometry(QtCore.QRect(10, 30, 780, 390))

    def set_slots(self):
        self.public_market.combo.currentTextChanged.connect(self.select_public_market)
        self.public_pair.combo.currentTextChanged.connect(self.select_public_symbol)
        shared_data.symbol_ticker.changed.connect(self.coin_info_widget.update_info)

    def select_public_market(self):
        shared_data.selected_public_market = self.public_market.combo.currentText()
        shared_data.public_data_last_time_update = 0

    def select_public_symbol(self):
        shared_data.selected_public_pair = self.public_pair.combo.currentText()
        shared_data.public_data_last_time_update = 0


class WalletWidget:
    def __init__(self, parent):
        self.wallet_box = QtWidgets.QGroupBox('Wallet', parent)
        self.wallet_bar = Bar('Wallet', shared_data.names_of_wallets, 20, 30, 70, 30, True, self.wallet_box)
        self.order_table = OrdersTable(self.wallet_box)
        self.init_widget()
        self.set_slots()

    def init_widget(self):
        self.wallet_box.setGeometry(QtCore.QRect(10, 440, 780, 250))
        self.order_table.setGeometry(QtCore.QRect(10, 70, 760, 170))

    def set_slots(self):
        self.wallet_bar.combo.currentTextChanged.connect(self.select_wallet)
        shared_data.balance.changed.connect(self.on_wallet_balance_change)
        shared_data.active_orders.changed.connect(self.on_active_orders_change)

    def select_wallet(self):
        shared_data.selected_wallet_name = self.wallet_bar.combo.currentText()
        if shared_data.selected_wallet_name != '':
            shared_data.wallet_authorize_update_time = 0
            shared_data.selected_wallet.clear()
            shared_data.selected_wallet.update(
                Wallets.get_wallet_by_name(shared_data.selected_wallet_name).Value)

    def on_wallet_balance_change(self):
        pass

    def on_active_orders_change(self):
        pass


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
        self.label = QtWidgets.QLabel(parent)
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
        self.label = QtWidgets.QLabel(parent)
        self.label.setText(label_text)
        self.label.move(label_x, label_y)
        self.text_edit = QtWidgets.QLineEdit(parent)
        self.text_edit.setText(text)
        self.text_edit.move(text_x, text_y)
        self.text_edit.resize(text_w, 20)
        self.set_enabled(enabled)

    def set_enabled(self, enabled):
        self.label.setEnabled(enabled)
        self.text_edit.setEnabled(enabled)


class AddWalletWidget(QtWidgets.QWidget):
    def __init__(self, *args):
        super().__init__(*args)
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
            shared_data.names_of_wallets.clear()
            shared_data.names_of_wallets.extend(Wallets.get_list_of_wallets().value)
            self.close()

        # bind actions with button
        save_button.clicked.connect(on_push_save)


class DeleteWalletWidget(QtWidgets.QWidget):
    def __init__(self, *args):
        super().__init__(*args)
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
        wallet_bar = Bar('Wallet name :', shared_data.names_of_wallets, 20, 30, 120, 30, True, self)
        save_button = QtWidgets.QPushButton('Delete', self)
        save_button_width = save_button.width()
        save_button.move(int((self.width() - save_button_width) / 2), 70)

        # actions
        def on_push_delete():
            Wallets.delete_wallet_by_name(wallet_bar.combo.currentText())
            # global wallet_names
            shared_data.names_of_wallets.clear()
            shared_data.names_of_wallets.extend(Wallets.get_list_of_wallets().value)
            self.close()

        # bind actions with button
        save_button.clicked.connect(on_push_delete)
