"""https://api.hitbtc.com"""

from marketAPI.HttpRequests import RestRequests

timeLimitForRequest = 10  # seconds


class PublicRequests(RestRequests):

    @staticmethod
    def requestTicker(forCryptoCoin, forCurrencyCoin, fromURL):
        """24 hour price change statistics."""
        return PublicRequests.__publicRequest(fromURL, f'ticker/{forCryptoCoin}{forCurrencyCoin}')

    @staticmethod
    def requestTrades(forCryptoCoin, forCurrencyCoin, fromURL, withRowLimit):
        """Get recent trades (up to last 500)."""
        return PublicRequests.__publicRequest(fromURL,
                                              f'trades/{forCryptoCoin}{forCurrencyCoin}?limit={withRowLimit}')

    @staticmethod
    def __publicRequest(toURL: str, withMethodName: str):
        URIEndpoint = f"api.{toURL}"
        apiPoint = 'api/2/public'
        return RestRequests.publicRequest(URIEndpoint, apiPoint, withMethodName, timeLimitForRequest)
