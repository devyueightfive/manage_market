# https://github.com/devyueightfive
# utf-8
"""
Adapter classes for 'wex_api'
"""

import market_api.wex_api as wex
from wallet.wallets import Wallets

http_timeout = 10


class Public:
    @staticmethod
    def getTicker(marketUrl: str, coinFrom: str, coinTo: str):
        response = wex.Public.ticker(marketUrl, coinFrom, coinTo)
        for symbol, element in response.items():
            element['vol'], element['vol_cur'] = element['vol_cur'], element['vol']
        return response

    @staticmethod
    def getTrades(marketUrl: str, coinFrom: str, coinTo: str, limit=5000):
        if limit:
            return wex.Public.trades(marketUrl, coinFrom, coinTo, limit=limit)
        else:
            return wex.Public.trades(marketUrl, coinFrom, coinTo)


class TradeApi:
    @staticmethod
    def getBalanceInfo(wallet: dict):
        balance = {'funds': {}, 'orders': {}}
        # request for Info
        response = wex.TradeApi.getinfo(wallet)
        if response['success'] == 1:
            funds = response.get('return', {}).get('funds', {})
            for k, v in funds.items():
                if v != 0:
                    balance['funds'][k] = v
            response = wex.TradeApi.active_orders(wallet)
            if response['success'] == 1 and 'return' in response.keys():
                balance['orders'].update(response['return'])
        return balance

    @staticmethod
    def createOrder(wallet: dict, pair: str, type: str, rate: float, amount: float):
        return wex.TradeApi.trade(wallet, pair, type, rate, amount)

    @staticmethod
    def cancelOrder(wallet: dict, order_id: str):
        return wex.TradeApi.cancel_order(wallet, order_id)


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
    url = 'wex.nz'
    cfrom = 'eth'
    cto = 'usd'
    # info = Public.getTicker(url, cfrom, cto)
    # pprint(info)
    # trades = Public.getTrades(url, cfrom, cto)
    # pprint(trades)

    name = '#1 wex'
    w = Wallets.get_wallet_by_name(name).Value
    # b = TradeApi.getBalanceInfo(w)
    # pprint(b)
    order = TradeApi.createOrder(w, "btc_usd")
