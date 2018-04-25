from pprint import pprint

from market_api import binance_api as native_api


class Public:
    @staticmethod
    def pair(coin_from: str, coin_to: str) -> str:
        return f"{coin_from}_{coin_to}".lower()

    @staticmethod
    def getTicker(marketUrl: str, coinFrom: str, coinTo: str):
        response = native_api.Public.ticker(marketUrl, coinFrom, coinTo)
        pair = Public.pair(coinFrom, coinTo)
        return {pair: {'avg': (float(response['highPrice']) + float(response['lowPrice'])) / 2,
                       'buy': float(response['bidPrice']),
                       'high': float(response['highPrice']),
                       'last': float(response['lastPrice']),
                       'low': float(response['lowPrice']),
                       'sell': float(response['askPrice']),
                       'updated': float(response['closeTime']) / 1000,
                       'vol': float(response['volume']),
                       'vol_cur': float(response['quoteVolume'])
                       }
                }

    @staticmethod
    def getTrades(marketUrl: str, coinFrom: str, coinTo: str, limit=500):

        def response_adapter(data):
            pair = Public.pair(coinFrom, coinTo)
            adapted_data = {pair: data}
            adapter = {
                'amount': 'qty',
                # 'price': 'price',
                'tid': 'id',
                'timestamp': 'time',
                'type': 'isBuyerMaker',
            }
            for element in adapted_data.get(pair):
                for k, v in adapter.items():
                    element[k] = element.get(v, 0)
                    element.pop(v)
                element['type'] = 'bid' if element.get('type') == 'True' else 'ask'
                element['timestamp'] = float(element['timestamp']) / 1000
            return adapted_data

        response = native_api.Public.trades(marketUrl, coinFrom, coinTo, limit)
        return response_adapter(response)


class PublicV2:
    pass


if __name__ == "__main__":
    url = 'binance.com'
    cfrom = 'eth'
    cto = 'usd'
    # info = Public.getTicker(url, cfrom, cto)
    # pprint(info)
    trades = Public.getTrades(url, cfrom, cto)
    pprint(trades)
