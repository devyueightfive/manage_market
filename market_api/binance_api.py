"""
https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
"""

import market_api.rest_api as rapi

http_timeout = 10


class Public:
    @staticmethod
    def api_call(market_url: str, method_name: str):
        base_endpoint = f"api.{market_url}"
        api_point = '/api/v1/'
        return rapi.RestApi.publicApiCall(base_endpoint, api_point, method_name, http_timeout)

    @staticmethod
    def symbol(coin_from: str, coin_to: str) -> str:
        s = [coin_from, coin_to]
        for index in range(len(s)):
            if s[index].upper() == 'USD':
                s[index] = 'USDT'
        return f'{s[0]}{s[1]}'.upper()

    @staticmethod
    def ticker(market_url: str, coin_from: str, coin_to: str):
        """24 hour price change statistics."""
        symbol = Public.symbol(coin_from, coin_to)
        return Public.api_call(market_url, f'ticker/24hr?symbol={symbol}')

    @staticmethod
    def trades(market_url: str, coin_from: str, coin_to: str, limit=None):
        """Get recent trades (up to last 500).
        """
        symbol = Public.symbol(coin_from, coin_to)
        if limit:
            return Public.api_call(market_url,
                                   f'trades?symbol={symbol}&limit={limit}')
        else:
            return Public.api_call(market_url, f'trades?symbol={symbol}')


class PublicV2:
    pass


if __name__ == "__main__":
    from pprint import pprint

    coin_from = 'eth'
    coin_to = 'usd'
    market_url = 'binance.com'

    ticker = Public.ticker(market_url, coin_from, coin_to)
    pprint(ticker)
    trades = Public.trades(market_url, coin_from, coin_to)
    pprint(trades)
