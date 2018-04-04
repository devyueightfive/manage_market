import os

from PyQt5.QtCore import QObject, pyqtSignal

import data_updater
from market_api import api


class ValueWithSignal(QObject):
    changed = pyqtSignal()

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value


class Return:
    """
        v = (0,-1)
        t = ('OK', 'Warning', 'Error')
        text = any_text
    """

    def __init__(self, v, t='OK', text=''):
        self.value = v
        self.type = t
        self.text = text

    def __str__(self):
        return f"Value:\t{self.value}\nType:\t{self.type}\nText:\t{self.text}"


my_path = os.path.abspath(os.curdir)
wallets_file = "\\".join([my_path, "json\\wallets.json"])
balance_file = "\\".join([my_path, "json\\balance.json"])
active_orders_file = "\\".join([my_path, "\\json\\active_orders.json"])
bots_file = "\\".join([my_path, "json\\active_orders.json"])

# globals
#
refresh_data_thread = data_updater.MarketDataUpdater()
#
_, supported_markets = _, sup_markets = api.get_api(None)
supported_pairs = []
# data in public widget
selected_public_market = ''  # connect to public_market.combo.currentText
selected_public_pair = ''  # connect to public_pair.combo.currentText
public_pair_value = ValueWithSignal(value={})
public_pair_trades = ValueWithSignal(value=[])
public_data_last_time_update = 0  # last time when data was updated (in seconds)
# wallets
names_of_wallets = []  # name list of created wallets
selected_wallet_name = ''  # connect to wallet_bar.combo.currentText
selected_wallet = {}
selected_wallet_balance = ValueWithSignal(value={})
wallet_balance_update_time = 0  # last time when data was updated (in seconds)
# orders
selected_wallet_active_orders = ValueWithSignal(value={})
wallet_active_update_time = 0  # last time when data was updated (in seconds)
#
robot_names = list()
