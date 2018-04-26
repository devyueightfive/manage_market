import time
from threading import Thread

import shared_data
from ReturnObjects import Return
from market_api import cryptoMarketApi

delay_update_for_public_requests = 13  # in seconds
delay_update_for_authorize_requests = 300  # in seconds


class MarketDataUpdater(Thread):
    last_pair = None
    last_market = None

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        try:
            while True:
                MarketDataUpdater.update()
        except Exception as e:
            return Return(-1, 'Error', e.__str__())

    @staticmethod
    def update():
        MarketDataUpdater.update_public_data()
        # print('public data updated.')
        MarketDataUpdater.update_authorize_data()
        # print('authorize data updated.')
        time.sleep(0.5)

    @staticmethod
    def update_public_data():
        # update ticker, trades data for coin/market selected by user
        if shared_data.selected_public_pair not in ['', None] and \
                shared_data.selected_public_market not in ['', None]:
            # print(
            #     f"{time.asctime()} Updater: \n"
            #     f"\tsymbol:\t{shared_data.selected_public_pair}\n"
            #     f"\tmarket:\t{shared_data.selected_public_market}")
            if (time.time() - shared_data.public_data_last_time_update) > delay_update_for_public_requests:
                shared_data.public_data_last_time_update = time.time()
                coin_from, coin_to = shared_data.selected_public_pair.split(sep='_')
                market_api, _ = cryptoMarketApi.getApi(shared_data.selected_public_market)
                # update data
                if market_api:
                    MarketDataUpdater.update_ticker_info(market_api, coin_from, coin_to)
                    MarketDataUpdater.update_trade_info(market_api, coin_from, coin_to)
            # markers for last selected user values
            MarketDataUpdater.last_pair = shared_data.selected_public_pair
            MarketDataUpdater.last_market = shared_data.selected_public_market
        else:
            if shared_data.selected_public_pair == '' and shared_data.selected_public_pair != \
                    MarketDataUpdater.last_pair:
                shared_data.symbol_ticker.value.clear()
                shared_data.symbol_ticker.changed.emit()
                MarketDataUpdater.last_pair = ''
            if shared_data.selected_public_market == '' and shared_data.selected_public_market != \
                    MarketDataUpdater.last_market:
                shared_data.trades.value.clear()
                shared_data.trades.changed.emit()
                MarketDataUpdater.last_market = ''

    @staticmethod
    def update_ticker_info(market_api, coin_from, coin_to):
        response = market_api.requestTickerInfo(coin_from, coin_to)
        # print(f'Ticker response : {response}')
        if response:
            shared_data.symbol_ticker.value.clear()
            shared_data.symbol_ticker.value.update(response.get(shared_data.selected_public_pair, {}))
            shared_data.symbol_ticker.changed.emit()

    @staticmethod
    def update_trade_info(market_api, coin_from, coin_to):
        response = market_api.requestTradesInfo(coin_from, coin_to)
        # print(f'Trade response : {response}')
        if response:
            shared_data.trades.value.clear()
            shared_data.trades.value.extend(response.get(shared_data.selected_public_pair, {}))
            shared_data.trades.changed.emit()

    @staticmethod
    def update_authorize_data():
        if shared_data.selected_wallet_name not in ['', None]:
            # print(shared_data.selected_wallet_name)
            if (time.time() - shared_data.wallet_authorize_update_time) > delay_update_for_authorize_requests:
                shared_data.wallet_authorize_update_time = time.time()
                # from wallet select 'market' url and define api
                market_api = cryptoMarketApi.getApi(shared_data.selected_wallet.get('market', ''))[0]
                # update data
                if market_api:
                    MarketDataUpdater.update_balance(market_api)
        else:
            shared_data.balance.value.clear()
            shared_data.balance.changed.emit()

    @staticmethod
    def update_balance(market_api: cryptoMarketApi.AbstractMarketAPI):
        response = market_api.requestBalance(shared_data.selected_wallet)
        print(f'Balance response : {response}')
        if response:
            shared_data.balance.value.clear()
            shared_data.balance.value.update(response)
            shared_data.balance.changed.emit()
