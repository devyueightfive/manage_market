import time
from threading import Thread

import settings
from market_api import api

delay_update = 5  # in seconds


class MarketDataUpdater(Thread):
    last_pair = None
    last_market = None

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        try:
            while True:
                # print("ticker round start")
                MarketDataUpdater.update()
                # print("ticker round end")
        except Exception as e:
            return settings.Return(-1, 'Error', e.__str__())

    @staticmethod
    def update():
        MarketDataUpdater.update_public_data()
        # print("Update public data finished.")
        MarketDataUpdater.update_balance()
        # print("balance finished")
        MarketDataUpdater.update_active_orders()
        time.sleep(0.5)
        print(f"{time.asctime()}: Updated.")

    @staticmethod
    def update_public_data():
        # update ticker, trades data for coin/market selected by user
        if settings.selected_public_pair != '' and \
                settings.selected_public_market != '':
            if (time.time() - settings.public_data_last_time_update) > delay_update:
                settings.public_data_last_time_update = time.time()
                coin_from, coin_to = settings.selected_public_pair.split(sep='_')
                market_api, _ = api.get_api(settings.selected_public_market)
                # update data
                if market_api:
                    MarketDataUpdater.update_ticker_info(market_api, coin_from, coin_to)
                    MarketDataUpdater.update_trade_info(market_api, coin_from, coin_to)
            # markers for last selected user values
            MarketDataUpdater.last_pair = settings.selected_public_pair
            MarketDataUpdater.last_market = settings.selected_public_market
        else:
            if settings.selected_public_pair == '' and settings.selected_public_pair != \
                    MarketDataUpdater.last_pair:
                settings.public_pair_value.value.clear()
                settings.public_pair_value.changed.emit()
                MarketDataUpdater.last_pair = ''
            if settings.selected_public_market == '' and settings.selected_public_market != \
                    MarketDataUpdater.last_market:
                settings.public_pair_trades.value.clear()
                settings.public_pair_trades.changed.emit()
                MarketDataUpdater.last_market = ''

    @staticmethod
    def update_ticker_info(market_api, coin_from, coin_to):
        response = market_api.get_ticker(coin_from, coin_to)
        if response:
            settings.public_pair_value.value.clear()
            settings.public_pair_value.value.update(response.get(settings.selected_public_pair, {}))
            settings.public_pair_value.changed.emit()

    @staticmethod
    def update_trade_info(market_api, coin_from, coin_to):
        response = market_api.get_trades(coin_from, coin_to, limit=1500)
        if response:
            print(response)
            settings.public_pair_trades.value.clear()
            settings.public_pair_trades.value.extend(response.get(settings.selected_public_pair, {}))
            settings.public_pair_trades.changed.emit()

    @staticmethod
    def update_balance():
        pass
        # if settings.selected_wallet_name != '':
        #     if (time.time() - settings.wallet_balance_update_time) > delay_update:
        #         response = TradeApi.getinfo(settings.selected_wallet)
        #         # print(f"Balance {response}")
        #         if response['success']:
        #             settings.selected_wallet_balance.value.clear()
        #             settings.selected_wallet_balance.value.update(response['return']['funds'])
        #             settings.selected_wallet_balance.changed.emit()
        #             if 'funds_incl_orders' in response['return'].keys():
        #                 pass
        #             settings.wallet_balance_update_time = time.time()
        #         else:
        #             settings.selected_wallet_balance.value.clear()
        #             settings.selected_wallet_balance.changed.emit()
        # else:
        #     settings.selected_wallet_balance.value.clear()
        #     settings.selected_wallet_balance.changed.emit()

    @staticmethod
    def update_active_orders():
        pass
        # if settings.selected_wallet_name != '':
        #     if (time.time() - settings.wallet_active_update_time) > delay_update:
        #         response = TradeApi.active_orders(settings.selected_wallet)
        #         # print(f"Active Orders {response}")
        #         if response['success']:
        #             settings.selected_wallet_active_orders.value.clear()
        #             settings.selected_wallet_active_orders.value.update(response['return'])
        #             settings.selected_wallet_active_orders.changed.emit()
        #             settings.wallet_active_update_time = time.time()
        #         else:
        #             settings.selected_wallet_active_orders.value.clear()
        #             settings.selected_wallet_active_orders.changed.emit()
        # else:
        #     settings.selected_wallet_active_orders.value.clear()
        #     settings.selected_wallet_active_orders.changed.emit()
