from TraderClasses import ValueWithSignal
from marketAPI import cryptoMarketApi
from wallet.wallets import Wallets

# List of supported markets, pairs
supportedMarkets = cryptoMarketApi.getApi(None)[1]
supportedTradePairs = Wallets.getValueRange('pairs').Value

# User selections in GUI
marketURLSelectedByUser = ''  # connect to public_market.combo.currentText
tradePairSelectedByUser = ''  # connect to public_pair.combo.currentText
walletNameSelectedByUser = ''  # connect to wallet_bar.combo.currentText

# Values for storing responses from user requests to marketAPI.
# Requests: Tickers, Trades, Balance, ActiveOrders
tradePairTicker = ValueWithSignal(value={})
tradePairTrades = ValueWithSignal(value=[])  # list
walletBalance = ValueWithSignal(value={})
walletActiveOrders = ValueWithSignal(value={})

# Values stores last time updates for responses
lastRequestTimeForPublicAPI = 0  # last time when data was updated (in seconds)
lastRequestTimeForTradeAPI = 0  # last time when data was updated (in seconds)

# Wallet  = {'name':str, 'market':str, 'sign':str, 'key':str, 'robots':dict}
walletSelectedByUser = {}

#
names_of_wallets = Wallets.getListOfWallets().Value  # name list of created wallets

# last tweets
tweets = ValueWithSignal(value=[])  # list

robot_names = list()
