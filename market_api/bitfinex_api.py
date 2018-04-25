import http.client
import json

http_timeout = 10


class Public:
    """
    https://docs.bitfinex.com/docs/public-endpoints
    """

    @staticmethod
    def api_call(market_url, method_name):
        conn = http.client.HTTPSConnection(f"api.{market_url}", timeout=http_timeout)
        conn.request('GET', '/v1/' + method_name)
        response = conn.getresponse().read().decode()
        data = json.loads(response)
        conn.close()
        return data

    @staticmethod
    def ticker(market_url, coin_from, coin_to):
        return Public.api_call(market_url, f'pubticker/{coin_from}{coin_to}')

    @staticmethod
    def trades(market_url, coin_from, coin_to, limit):
        return Public.api_call(market_url,
                               f'trades/{coin_from}{coin_to}?limit_trades={limit}')


class PublicV2:
    pass
