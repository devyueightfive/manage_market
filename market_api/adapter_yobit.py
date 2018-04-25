# https://github.com/devyueightfive
# utf-8
"""
Adapter classes for 'yobit_api'
"""
from pprint import pprint

import market_api.yobit_api as native_api
from wallet.wallets import Wallets

http_timeout = 15

convertible_coins = ['btc', 'eth', 'doge', 'waves', 'usd', 'rur']
not_coins = ['usd', 'rur']


class Public:
    @staticmethod
    def getTicker(marketUrl: str, coinFrom: str, coinTo: str):
        response = native_api.Public.ticker(marketUrl, coinFrom, coinTo)
        for symbol, element in response.items():
            element['vol'], element['vol_cur'] = element['vol_cur'], element['vol']
        return response

    @staticmethod
    def getTrades(marketUrl: str, coinFrom: str, coinTo: str, limit=1999):
        if limit:
            return native_api.Public.trades(marketUrl, coinFrom, coinTo, limit=limit)
        else:
            return native_api.Public.trades(marketUrl, coinFrom, coinTo)


class TradeApi:
    @staticmethod
    def getBalanceInfo(wallet: dict):
        balance = {'funds': {}, 'orders': {}}
        # request for Info
        response = native_api.TradeApi.getinfo(wallet)
        # pprint(response)
        if response['success'] == 1:
            funds = response.get('return', {}).get('funds', {})
            for k, v in funds.items():
                if v != 0:
                    balance['funds'][k] = v
            funds_incl_orders = response.get('return', {}).get('funds_incl_orders', {})
            coins_in_orders = [k for k, v in funds_incl_orders.items() if v]
            # pprint(coins_in_orders)
            for coin in coins_in_orders:
                for con_coin in convertible_coins:
                    if coin != con_coin and coin not in not_coins:
                        symbol = f"{coin}_{con_coin}"
                        # request for Orders
                        response = native_api.TradeApi.active_orders(wallet, symbol)
                        # print(f"{symbol}:\n {response}")
                        if response['success'] == 1 and 'return' in response.keys():
                            balance['orders'].update(response['return'])
        return balance

    @staticmethod
    def createOrder(wallet: dict, pair: str, stype: str, rate: float, amount: float):
        return native_api.TradeApi.trade(wallet, pair, stype, rate, amount)

    @staticmethod
    def cancelOrder(wallet: dict, order_id: str):
        return native_api.TradeApi.cancel_order(wallet, order_id)


"""
Example of Ticker return:
{'eth_usd': {'avg': 521.99999995,
             'buy': 511.39871603,
             'high': 538,
             'last': 511.39871604,
             'low': 505.9999999,
             'sell': 511.39871604,
             'updated': 1523910555,
             'vol': 294513.04929871,
             'vol_cur': 567.68937382
             }
}
Example of Trades return:
{'eth_usd': [{'amount': 0.01992642,
              'price': 511.39871604,
              'tid': 200832192,
              'timestamp': 1523911039,
              'type': 'bid'},
             {'amount': 0.00157641,
              'price': 511.39871604,
              'tid': 200832191,
              'timestamp': 1523911015,
              'type': 'bid'}
              ...
              ]
}
Example of Balance return:
{'funds': {'eth': 0.00764265, 'usd': 8.57e-06, 'waves': 0.00272569},
 'orders': {'150010654918436': {'amount': 0.01061921,
                                'pair': 'eth_usd',
                                'rate': 408,
                                'status': 0,
                                'timestamp_created': '1523496095',
                                'type': 'buy'
                                }
                                ...
            }
}
"""

if __name__ == "__main__":
    name = 'yobit@yura'
    w = Wallets.get_wallet_by_name(name).Value
    b = TradeApi.getBalanceInfo(w)
    pprint(b)
    url = 'yobit.io'
    cfrom = 'eth'
    cto = 'usd'
    info = Public.getTicker(url, cfrom, cto)
    pprint(info)
    trades = Public.getTrades(url, cfrom, cto)
    pprint(trades)
