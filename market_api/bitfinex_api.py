import http.client
import json

http_timeout = 10


class Public:
    @staticmethod
    def api_call(market_url, method_name):
        print(method_name)
        conn = http.client.HTTPSConnection(f"api.{market_url}", timeout=http_timeout)
        conn.request('GET', '/v1/' + method_name)
        response = conn.getresponse().read().decode()
        data = json.loads(response)
        conn.close()
        return data

    @staticmethod
    def ticker(market_url, coin_from, coin_to):
        def response_adapter(data):
            coin_pair = f"{coin_from}_{coin_to}"
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
            return adapted_data

        # Ratelimit: 30 req / min
        response = Public.api_call(market_url, f'pubticker/{coin_from}{coin_to}')
        return response_adapter(response)

        # response example
        # {
        #     "mid": "244.755",
        #     "bid": "244.75",
        #     "ask": "244.76",
        #     "last_price": "244.82",
        #     "low": "244.2",
        #     "high": "248.19",
        #     "volume": "7842.11542563",
        #     "timestamp": "1444253422.348340958"
        # }

    @staticmethod
    def trades(market_url, coin_from, coin_to, limit=None):
        def response_adapter(data):
            print(len(data))
            for e in data:
                e['type'] = 'bid' if e.get('type') == 'buy' else 'ask'
            coin_pair = f"{coin_from}_{coin_to}"
            adapted_data = {coin_pair: data}
            return adapted_data

        # Ratelimit: 45 req/min
        response = Public.api_call(market_url, f'trades/{coin_from}{coin_to}?limit_trades=999')
        return response_adapter(response)

        # example
        # [{
        #     "timestamp": 1444266681,
        #     "tid": 11988919,
        #     "price": "244.8",
        #     "amount": "0.03297384",
        #     "exchange": "bitfinex",
        #     "type": "sell"
        # }]


class PublicV2:
    pass


# test
if __name__ == "__main__":
    import pprint

    url = 'bitfinex.com'
    f = 'eth'
    t = 'usd'
    # pprint.pprint(PublicApi.ticker(url, f, t))
    pprint.pprint(Public.trades(url, f, t))
