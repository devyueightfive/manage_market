"""https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md"""

from marketAPI.HttpRequests import RestRequests

timeLimitForRequest = 10  # seconds


class PublicRequests(RestRequests):
    @staticmethod
    def requestTicker(forCryptoCoin: str, forCurrencyCoin: str, fromURL: str):
        """24 hour price change statistics."""
        tradeSymbol = PublicRequests.getTradeSymbolFrom(forCryptoCoin, forCurrencyCoin)
        return PublicRequests.__publicRequest(fromURL, f'ticker/24hr?symbol={tradeSymbol}')

    @staticmethod
    def requestTrades(forCryptoCoin: str, forCurrencyCoin: str, fromURL: str, withRowLimit=None):
        """Get recent trades (up to last 500)."""
        tradeSymbol = PublicRequests.getTradeSymbolFrom(forCryptoCoin, forCurrencyCoin)
        if withRowLimit:
            return PublicRequests.__publicRequest(fromURL, f'trades?symbol={tradeSymbol}&limit={withRowLimit}')
        else:
            return PublicRequests.__publicRequest(fromURL, f'trades?symbol={tradeSymbol}')

    @staticmethod
    def getTradeSymbolFrom(cryptoCoin: str, currencyCoin: str) -> str:
        """Trade Symbol like 'BTCUSDT'. Binance.com api is case sensitive."""
        'Market restriction use for USD.'
        if currencyCoin.upper() == 'USD':
            currencyCoin = 'USDT'
        return f'{cryptoCoin}{currencyCoin}'.upper()

    @staticmethod
    def __publicRequest(toURL: str, withMethodName: str):
        URIEndpoint = f"api.{toURL}"
        apiPoint = 'api/v1'
        return RestRequests.publicRequest(URIEndpoint, apiPoint, withMethodName, timeLimitForRequest)
