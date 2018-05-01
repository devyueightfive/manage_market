import os
import time
from threading import Thread

import tables

import settings
import sharedData
from marketAPI import cryptoMarketApi
from marketAPI.HttpRequests import RestRequests


class MarketDataProvider(Thread):
    delayForPublicRequests = 13  # in seconds
    delayForTradeRequests = 90  # in seconds
    last_pair = None
    last_market = None

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        while True:
            MarketDataProvider.requestData()
            time.sleep(0.5)

    @staticmethod
    def requestData():
        try:
            MarketDataProvider.requestPublicData()
            MarketDataProvider.requestTradeData()
        except Exception as err:
            print(f"Privider Error:{err.__str__()}")

    @staticmethod
    def requestPublicData():
        # update ticker, trades data for coin/market selected by user
        if sharedData.tradePairSelectedByUser not in ['', None] and \
                sharedData.marketURLSelectedByUser not in ['', None]:
            if (time.time() - sharedData.lastRequestTimeForPublicAPI) > MarketDataProvider.delayForPublicRequests:
                sharedData.lastRequestTimeForPublicAPI = time.time()
                cryptoCoin, currencyCoin = sharedData.tradePairSelectedByUser.split(sep='_')
                marketAPI = cryptoMarketApi.getApi(sharedData.marketURLSelectedByUser)[0]
                'request public data (Ticker/Trades)'
                if marketAPI:
                    MarketDataProvider.requestTickerInfo(cryptoCoin, currencyCoin, marketAPI)
                MarketDataProvider.readTradesInfo(cryptoCoin, currencyCoin, sharedData.marketURLSelectedByUser)
            # markers for last selected user values
            MarketDataProvider.last_pair = sharedData.tradePairSelectedByUser
            MarketDataProvider.last_market = sharedData.marketURLSelectedByUser
        else:
            if sharedData.tradePairSelectedByUser == '' and sharedData.tradePairSelectedByUser != \
                    MarketDataProvider.last_pair:
                sharedData.tradePairTicker.value.clear()
                sharedData.tradePairTicker.changed.emit()
                MarketDataProvider.last_pair = ''
            if sharedData.marketURLSelectedByUser == '' and sharedData.marketURLSelectedByUser != \
                    MarketDataProvider.last_market:
                sharedData.tradePairTrades.value.clear()
                sharedData.tradePairTrades.changed.emit()
                MarketDataProvider.last_market = ''

    @staticmethod
    def requestTickerInfo(forCryptoCoin, forCurrencyCoin, fromMarketAPI):
        response = fromMarketAPI.requestTickerInfo(forCryptoCoin, forCurrencyCoin)
        # print(f'Ticker response : {response}')
        if response:
            sharedData.tradePairTicker.value.clear()
            sharedData.tradePairTicker.value.update(response.get(sharedData.tradePairSelectedByUser, {}))
            sharedData.tradePairTicker.changed.emit()

    @staticmethod
    def readTradesInfo(forCryptoCoin, forCurrencyCoin, forURL, fromTradesFile=settings.pathToTradesFile):
        tradePair = RestRequests.getTradePairSymbolFrom(forCryptoCoin, forCurrencyCoin)
        url = forURL.replace('.', '')
        dayInSeconds = 3 * 60 * 60 * 24  # 3 days
        trades24h = None
        if os.path.exists(fromTradesFile):
            with tables.open_file(fromTradesFile, 'r') as file:
                where = f'/{tradePair}/{url}'
                tableWithTrades = file.get_node(where, 'trades')
                lastDayInSeconds = time.time() - dayInSeconds
                trades24h = [dict(tid=row['tid'], type=row['type'], timestamp=row['timestamp'], price=row['price'],
                                  amount=row['amount']) for row in
                             tableWithTrades.where(f'timestamp >= {int(lastDayInSeconds)}')]
                tableWithTrades.close()
        if trades24h:
            sharedData.tradePairTrades.value.clear()
            sharedData.tradePairTrades.value.extend(trades24h)
            sharedData.tradePairTrades.changed.emit()

    @staticmethod
    def requestTradeData():
        if sharedData.walletNameSelectedByUser not in ['', None]:
            # print(shared_data.selected_wallet_name)
            if (time.time() - sharedData.lastRequestTimeForTradeAPI) > MarketDataProvider.delayForTradeRequests:
                sharedData.lastRequestTimeForTradeAPI = time.time()
                # from wallet select 'market' url and define api
                market_api = cryptoMarketApi.getApi(sharedData.walletSelectedByUser.get('market', ''))[0]
                # update data
                if market_api:
                    MarketDataProvider.update_balance(market_api)
        else:
            sharedData.walletBalance.value.clear()
            sharedData.walletBalance.changed.emit()

    @staticmethod
    def update_balance(market_api: cryptoMarketApi.AbstractMarketAPI):
        response = market_api.requestBalance(sharedData.walletSelectedByUser)
        print(f'Balance response : {response}')
        if response:
            sharedData.walletBalance.value.clear()
            sharedData.walletBalance.value.update(response)
            sharedData.walletBalance.changed.emit()
