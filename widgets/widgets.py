import re

from PyQt5 import QtWidgets, QtGui, QtCore
from bs4 import BeautifulSoup

import shared_data
from market_api.cryptoMarketApi import getApi
from wallet.wallets import Wallets
from widgets.CoinInfo import CoinInfoWidget
from widgets.LiveChart import LiveChart
from widgets.Tables import OrdersTable, BalanceTable


class InfoWidget:

    def __init__(self, parent):
        self.public_info_box = QtWidgets.QGroupBox('Info', parent)
        self.coin_info_widget = CoinInfoWidget(parent=self.public_info_box)
        self.live_chart_widget = LiveChart(parent=self.public_info_box)
        self.public_pair = Bar('Pair', shared_data.supported_pairs, 20, 50, 70, 50, self.public_info_box)
        self.public_market = Bar('Market', shared_data.supported_markets, 20, 20, 70, 20, self.public_info_box)
        self.init_widget()
        self.set_slots()

    def init_widget(self):
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
        self.wallet_bar = Bar('Wallet', shared_data.names_of_wallets, 20, 30, 70, 30, self.wallet_box)
        self.balance_table = BalanceTable(self.wallet_box)
        self.order_table = OrdersTable(self.wallet_box)
        self.init_widget()
        self.set_slots()

    def init_widget(self):
        self.wallet_box.setGeometry(QtCore.QRect(10, 440, 1090, 450))
        self.balance_table.setGeometry(QtCore.QRect(10, 100, 160, 340))
        self.order_table.setGeometry(QtCore.QRect(180, 20, 540, 420))

    def set_slots(self):
        self.wallet_bar.combo.currentTextChanged.connect(self.select_wallet)
        shared_data.balance.changed.connect(self.balance_table.updateBalance)
        shared_data.balance.changed.connect(self.order_table.updateOrders)

    def select_wallet(self):
        shared_data.selected_wallet_name = self.wallet_bar.combo.currentText()
        if shared_data.selected_wallet_name != '':
            shared_data.wallet_authorize_update_time = 0
            shared_data.selected_wallet.clear()
            shared_data.selected_wallet.update(
                Wallets.get_wallet_by_name(shared_data.selected_wallet_name).Value)


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
        wallet_text_bar = TextLine('Wallet name :', '', 20, 30, 120, 30, self, text_width=130)
        market_text_bar = TextLine('Market address :', '', 280, 30, 380, 30, self, text_width=130)
        key_text_bar = TextLine('Key :', '', 20, 70, 120, 70, self, text_width=390)
        sign_text_bar = TextLine('Sign :', '', 20, 110, 120, 110, self, text_width=390)
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
            shared_data.names_of_wallets.extend(Wallets.get_list_of_wallets().Value)
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
        wallet_bar = Bar('Wallet name :', shared_data.names_of_wallets, 20, 30, 120, 30, self)
        save_button = QtWidgets.QPushButton('Delete', self)
        save_button_width = save_button.width()
        save_button.move(int((self.width() - save_button_width) / 2), 70)

        # actions
        def on_push_delete():
            Wallets.delete_wallet_by_name(wallet_bar.combo.currentText())
            shared_data.names_of_wallets.clear()
            shared_data.names_of_wallets.extend(Wallets.get_list_of_wallets().Value)
            self.close()

        # bind actions with button
        save_button.clicked.connect(on_push_delete)


class AddOrder(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)
        self.init_ui()

    def init_ui(self):
        self.set_general_options()
        self.set_widgets()
        self.set_slots()

    def set_general_options(self):  # general options for the window
        self.resize(440, 190)
        self.setWindowTitle('Add Order ...')
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr = self.frameGeometry()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def getCurrencyBalance(self):
        # should be defined shared.balance
        if shared_data.selected_wallet_name not in ['', None]:
            pair = self.pairText.combo.currentText()
            actionType = self.typeBar.combo.currentText()
            print(f"Pair = {pair}")
            if pair not in ['', None] and actionType not in ['', None]:
                coin, currency = pair.split('_')
                if self.typeBar.combo.currentText() == 'buy':
                    remains = shared_data.balance.value.get('funds').get(currency, 0)
                else:
                    remains = shared_data.balance.value.get('funds').get(coin, 0)
                return self.currencyBalance.setText(
                    '<center><u style="color:#0000ff;">{:0,.8f}</u></center>'.format(
                        remains)
                )
            return self.currencyBalance.setText("")

    def set_widgets(self):
        self.typeBar = Bar("Type:", ['sell', 'buy'], 20, 20, 70, 20, self)
        self.pairText = Bar("Pair:", shared_data.supported_pairs, 220, 20, 270, 20, self)
        label = QtWidgets.QLabel(self)
        label.setText("On Balance:")
        label.move(200, 60)
        self.currencyBalance = QtWidgets.QLabel(self)
        self.currencyBalance.setTextFormat(QtCore.Qt.RichText)
        self.currencyBalance.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.currencyBalance.resize(100, 15)
        self.currencyBalance.move(270, 60)
        self.rateText = TextLine("Rate:", '', 20, 100, 70, 100, self)
        self.amountText = TextLine("Amount:", '', 220, 100, 270, 100, self)

        self.create_button = QtWidgets.QPushButton('Add Order', self)
        self.create_button_width = self.create_button.width()
        self.create_button.move(int((self.width() - self.create_button_width) / 2), 150)

    def set_slots(self):
        self.create_button.clicked.connect(self.__action_AddOrder)
        self.pairText.combo.currentTextChanged.connect(self.getCurrencyBalance)
        self.typeBar.combo.currentTextChanged.connect(self.getCurrencyBalance)

    def mousePressEvent(self, event):
        self.fillAmount()

    def fillAmount(self):
        typeAction = self.typeBar.combo.currentText()
        rate = self.rateText.text_edit.text()
        remains = self.currencyBalance.text()
        remains = BeautifulSoup(remains, "html.parser").text
        if re.match("^\d+?\.?\d+?$", rate) and re.match("^\d+?\.?\d+?$", remains):
            amount = 0
            if typeAction == 'buy':
                api = getApi(shared_data.selected_wallet.get('market'))[0]
                amount = float(remains) / float(rate) * (1 - api.market_fine)
            elif typeAction == 'sell':
                amount = float(remains)
            self.amountText.text_edit.setText(str(int(amount * 10 ** 8) / 10 ** 8))
        else:
            mb = QtWidgets.QMessageBox()
            mb.setText("Some error")
            mb.setWindowTitle("Error")
            mb.exec()

    def __action_AddOrder(self):
        actionType = self.typeBar.combo.currentText()
        pair = self.pairText.combo.currentText()
        rate = self.rateText.text_edit.text()
        amount = self.amountText.text_edit.text()
        if actionType not in ['', None] and pair not in ['', None]:
            if re.match("^\d+?\.?\d+?$", rate) and re.match("^\d+?\.?\d+?$", amount):
                wallet = shared_data.selected_wallet
                api = getApi(shared_data.selected_wallet.get('market'))[0]
                response = api.requestOrderCreation(pair, actionType, float(rate), float(amount), wallet)
                shared_data.wallet_authorize_update_time = 0
                self.close()
                if response['success'] == 0:
                    mb = QtWidgets.QMessageBox()
                    mb.setText(response.get('error', 'Error'))
                    mb.setWindowTitle("Error")
                    mb.exec()
            else:
                mb = QtWidgets.QMessageBox()
                mb.setText("Please select rate/amount.")
                mb.setWindowTitle("Warning")
                mb.exec()
        else:
            mb = QtWidgets.QMessageBox()
            mb.setText("Please select type/pair.")
            mb.setWindowTitle("Warning")
            mb.exec()

    def show(self):
        if shared_data.selected_wallet_name not in ['', None]:
            super().show()
        else:
            mb = QtWidgets.QMessageBox()
            mb.setText("Please select a wallet.")
            mb.setWindowTitle("Warning")
            mb.exec()


class DeleteOrder(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)
        self.orderNumbers = []
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

        self.resize(440, 120)
        self.setWindowTitle('Cancel Order ...')
        center()

    def set_widgets(self):
        print("Set Up")
        delete_button = QtWidgets.QPushButton('Cancel Order', self)
        delete_button_width = delete_button.width()
        delete_button.move(int((self.width() - delete_button_width) / 2), 60)
        self.orderID = Bar("Order id:", self.orderNumbers,
                           100, 20, 200, 20, self, combo_width=150)
        delete_button.clicked.connect(self.__action_DeleteOrder)

    def show(self):
        if shared_data.selected_wallet_name not in ['', None]:
            super().show()
            self.orderNumbers.clear()
            self.orderNumbers.extend(
                list(shared_data.balance.value.get('orders', {}).keys()))
        else:
            mb = QtWidgets.QMessageBox()
            mb.setText("Please select a wallet.")
            mb.setWindowTitle("Warning")
            mb.exec()

    def __action_DeleteOrder(self):
        order_id = self.orderID.combo.currentText()
        if order_id not in ['', None]:
            wallet = shared_data.selected_wallet
            api = getApi(shared_data.selected_wallet.get('market'))[0]
            response = api.requestOrderCancellation(self.orderID.combo.currentText(), wallet)
            shared_data.wallet_authorize_update_time = 0
            if response['success'] == 0:
                mb = QtWidgets.QMessageBox()
                mb.setText(response.get('error', 'Error'))
                mb.setWindowTitle("Error")
                mb.exec()
            self.close()
        else:
            mb = QtWidgets.QMessageBox()
            mb.setText("Please select Order ID")
            mb.setWindowTitle("Warning")
            mb.exec()
