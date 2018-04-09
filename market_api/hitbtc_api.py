import http.client
import json

from dateutil import parser

http_timeout = 10


class Public:
    @staticmethod
    def api_call(market_url, method_name):
        print(method_name)
        conn = http.client.HTTPSConnection(f"api.{market_url}", timeout=http_timeout)
        conn.request('GET', '/api/2/public/' + method_name)
        response = conn.getresponse().read().decode()
        data = json.loads(response)
        conn.close()
        return data

    @staticmethod
    def ticker(market_url, coin_from, coin_to):
        def response_adapter(data):
            symbol = f"{coin_from}_{coin_to}"
            adapted_data = {symbol: data}
            adapter = {
                'sell': 'ask',
                'buy': 'bid',
                'vol': 'volume',
                'updated': 'timestamp',
                'vol_cur': 'volumeQuote'
            }
            for k, v in adapter.items():
                adapted_data[symbol][k] = data.get(v, 0)
            updated = adapted_data.get(symbol).get('updated')
            if updated:
                adapted_data[symbol]['updated'] = int(float(parser.parse(updated).timestamp()))
            return adapted_data

        # Ratelimit: 30 req / min
        response = Public.api_call(market_url, f'ticker/{coin_from}{coin_to}')
        return response_adapter(response)

        # response example
        # {
        #     "ask": "410.48", #sell
        #     "bid": "410.18", #buy
        #     "last": "410.35", #last
        #     "open": "411.11",
        #     "low": "407.14", #low
        #     "high": "442.96", #high
        #     "volume": "13152.156",
        #     "volumeQuote": "5504255.35493",
        #     "timestamp": "2018-04-09T13:28:29.150Z",
        #     "symbol": "ETHUSD"
        # }
        # [avg, buy, high, last, low, sell, updated, vol, vol_cur]

    @staticmethod
    def trades(market_url, coin_from, coin_to, limit=None):
        def response_adapter(data):
            print(len(data))
            # print(data)
            symbol = f"{coin_from}_{coin_to}"
            adapted_data = {symbol: data}
            adapter = {
                'type': 'side',
                'amount': 'quantity'
            }
            for element in adapted_data.get(symbol):
                for k, v in adapter.items():
                    element[k] = element.get(v, 0)
                # print(element)
                element['timestamp'] = int(float(parser.parse(element.get('timestamp', 0)).timestamp()))
            return adapted_data

        # Ratelimit: 45 req/min
        response = Public.api_call(market_url, f'trades/{coin_from}{coin_to}?limit=1000')
        return response_adapter(response)

        # example
        # [
        #   {
        #     "id": 76502536,
        #     "price": "0.012285",
        #     "quantity": "6.754",
        #     "side": "sell",
        #     "timestamp": "2017-01-10T12:00:00.672Z"
        #   }
        # ]
        #   [type,price,amount,tid,timestamp]


if __name__ == "__main__":
    cfrom = 'ETH'
    cto = 'USD'
    the_symbol = f'{cfrom}_{cto}'
    url = 'hitbtc.com'
    print(Public.trades(url, cfrom, cto))
