# https://github.com/devyueightfive
# utf-8
"""
Adapter classes for 'bitfinex_api'
"""
from pprint import pprint

import market_api.bitfinex_api as bitfinex


class Public:
    @staticmethod
    def getTicker(marketUrl: str, coinFrom: str, coinTo: str):

        def response_adapter(data):
            coin_pair = f"{coinFrom}_{coinTo}"
            adapted_data = {coin_pair: data}
            adapter = {
                'avg': 'mid',
                'last': 'last_price',
                'sell': 'ask',
                'buy': 'bid',
                'vol': 'volume',
                'updated': 'timestamp'
            }
            for k, v in adapter.items():
                adapted_data[coin_pair][k] = data.get(v, 0)
                adapted_data[coin_pair].pop(v)
            return adapted_data

        response = bitfinex.Public.ticker(marketUrl, coinFrom, coinTo)
        return response_adapter(response)

    @staticmethod
    def getTrades(marketUrl: str, coinFrom: str, coinTo: str, limit=999):

        def response_adapter(data):
            for e in data:
                e['type'] = 'bid' if e.get('type') == 'buy' else 'ask'
            coin_pair = f"{coinFrom}_{coinTo}"
            adapted_data = {coin_pair: data}
            return adapted_data

        response = bitfinex.Public.trades(marketUrl, coinFrom, coinTo, limit=limit)
        return response_adapter(response)


class TradeApi:
    pass


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
    url = 'bitfinex.com'
    cfrom = 'eth'
    cto = 'usd'
    # info = Public.getTicker(url, cfrom, cto)
    # pprint(info)
    trades = Public.getTrades(url, cfrom, cto)
    pprint(trades)

    # name = '#1 wex'
    # w = Wallets.get_wallet_by_name(name).Value
    # b = TradeApi.getBalanceInfo(w)
    # pprint(b)
