import data_updater
from QtObjects import ValueWithSignal
from market_api import cryptoMarketApi
from wallet.wallets import Wallets

# Thread updates global data by requests to markets
dataUpdater = data_updater.MarketDataUpdater()

# List of supported markets, pairs
_, supported_markets = cryptoMarketApi.getApi(None)
supported_pairs = Wallets.value_range_of_parameter('pairs').Value

# User selections in GUI
selected_public_market = ''  # connect to public_market.combo.currentText
selected_public_pair = ''  # connect to public_pair.combo.currentText
selected_wallet_name = ''  # connect to wallet_bar.combo.currentText

# Values for storing responses from requests to markets.
# Requests: Tickers, Trades, Balance, ActiveOrders
symbol_ticker = ValueWithSignal(value={})
trades = ValueWithSignal(value=[])
balance = ValueWithSignal(value={})
active_orders = ValueWithSignal(value={})

# Values stores last time updates for responses
public_data_last_time_update = 0  # last time when data was updated (in seconds)
wallet_authorize_update_time = 0  # last time when data was updated (in seconds)

# Wallet  = {'name':str, 'market':str, 'sign':str, 'key':str, 'robots':dict}
selected_wallet = {}

#
names_of_wallets = Wallets.get_list_of_wallets().Value  # name list of created wallets

robot_names = list()
