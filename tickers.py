from threading import Thread
from market_api import PublicApi, TradeApi
import time
import settings

delay_update = 5  # in seconds


class MarketTicker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        try:
            while True:
                # print("ticker round start")
                MarketTicker.update()
                time.sleep(5)
                # print("ticker round end")
        except Exception as e:
            return settings.Return(-1, 'Error', e.__str__())

    @staticmethod
    def update():
        MarketTicker.update_public_pair()
        # print("public pair finished")
        time.sleep(1)
        MarketTicker.update_balance()
        # print("balance finished")
        time.sleep(1)
        MarketTicker.update_active_orders()
        # print("active orders finished")

    @staticmethod
    def update_public_pair():
        if settings.selected_public_pair != '' and \
                settings.selected_public_market != '':
            if (time.time() - settings.public_pair_update_time) > delay_update:
                pair = settings.selected_public_pair.split(sep='_')
                t_from = pair[0]
                t_to = pair[1]
                response = PublicApi.ticker(settings.selected_public_market, t_from, t_to)
                settings.public_pair_value.value.clear()
                settings.public_pair_value.value.update(response[settings.selected_public_pair])
                settings.public_pair_value.changed.emit()
                settings.public_pair_update_time = time.time()
        else:
            settings.public_pair_value.value.clear()
            settings.public_pair_value.changed.emit()

    @staticmethod
    def update_balance():
        if settings.selected_wallet_name != '':
            if (time.time() - settings.wallet_balance_update_time) > delay_update:
                response = TradeApi.getinfo(settings.selected_wallet)
                print(f"Balance {response}")
                if response['success']:
                    settings.selected_wallet_balance.value.clear()
                    settings.selected_wallet_balance.value.update(response['return']['funds'])
                    settings.selected_wallet_balance.changed.emit()
                    if 'funds_incl_orders' in response['return'].keys():
                        pass
                    settings.wallet_balance_update_time = time.time()
                else:
                    settings.selected_wallet_balance.value.clear()
                    settings.selected_wallet_balance.changed.emit()
        else:
            settings.selected_wallet_balance.value.clear()
            settings.selected_wallet_balance.changed.emit()

    @staticmethod
    def update_active_orders():
        if settings.selected_wallet_name != '':
            if (time.time() - settings.wallet_active_update_time) > delay_update:
                response = TradeApi.active_orders(settings.selected_wallet)
                print(f"Active Orders {response}")
                if response['success']:
                    settings.selected_wallet_active_orders.value.clear()
                    settings.selected_wallet_active_orders.value.update(response['return'])
                    settings.selected_wallet_active_orders.changed.emit()
                    settings.wallet_active_update_time = time.time()
                else:
                    settings.selected_wallet_active_orders.value.clear()
                    settings.selected_wallet_active_orders.changed.emit()
        else:
            settings.selected_wallet_active_orders.value.clear()
            settings.selected_wallet_active_orders.changed.emit()
