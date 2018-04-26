class AbstractMarketAPI:
    """ Base MarketApi class.
    """
    marketURL = None
    publicAPI = None
    tradeAPI = None

    marketFine = 0

    def requestTickerInfo(self, forCryptoCoin, forCurrencyCoin):
        try:
            return self.publicAPI.requestTicker(forCryptoCoin, forCurrencyCoin, self.marketURL)
        except Exception as e:
            print(f"{self.marketURL} Ticker error:", e.__str__())
            return None

    def requestTradesInfo(self, forCryptoCoin, forCurrencyCoin, withRowLimit=None):
        try:
            if withRowLimit:
                return self.publicAPI.requestTrades(forCryptoCoin, forCurrencyCoin, self.marketURL,
                                                    withRowLimit=withRowLimit)
            else:
                return self.publicAPI.requestTrades(forCryptoCoin, forCurrencyCoin, self.marketURL)
        except Exception as e:
            print(f"{self.marketURL} Trades error:", e.__str__())
            return None

    def requestBalance(self, forWallet: dict):
        """Request for Wallet Balance"""
        try:
            return self.tradeAPI.requestBalance(forWallet)
        except Exception as e:
            print(f"{self.marketURL} Balance error:", e.__str__())
            return None

    def requestOrderCreation(self, forTradePair: str, withOrderType: str, withRate: float, withAmount: float,
                             inWallet: dict):
        """Request for Order Creation"""
        try:
            return self.tradeAPI.requestOrderCreation(forTradePair, withOrderType, withRate, withAmount, inWallet)
        except Exception as e:
            print(f"{self.marketURL} Create Order error:", e.__str__())
            return None

    def requestOrderCancellation(self, forOrderID: str, inWallet: dict):
        """Request for Order Cancel"""
        try:
            return self.tradeAPI.requestOrderCancellation(forOrderID, inWallet)
        except Exception as e:
            print(f"{self.marketURL} Cancel Order error:", e.__str__())
            return None


class WexMarketApi(AbstractMarketAPI):
    def __init__(self, version=1):
        super().__init__()
        self.marketURL = 'wex.nz'
        self.marketFine = 0.002
        from .adaptedApiForWexMarket import Public, TradeApi
        self.publicAPI = {
            '1': Public(),
        }.get(str(version), Public())
        self.tradeAPI = {
            '1': TradeApi(),
        }.get(str(version), TradeApi())


class BitfinexMarketApi(AbstractMarketAPI):
    def __init__(self, version=1):
        super().__init__()
        self.marketURL = 'bitfinex.com'
        self.marketFine = 0.002
        from .adaptedApiForBitfinexMarket import Public
        self.publicAPI = {
            '1': Public(),
        }.get(str(version), Public())


class YobitMarketApi(AbstractMarketAPI):
    def __init__(self, version=1):
        super().__init__()
        self.marketURL = 'yobit.io'
        self.marketFine = 0.002
        from .adaptedApiForYobitMarket import Public, TradeApi
        self.publicAPI = {
            '1': Public(),
        }.get(str(version), Public())
        self.tradeAPI = {
            '1': TradeApi(),
        }.get(str(version), TradeApi())


class HitBTCMarketApi(AbstractMarketAPI):
    def __init__(self, version=1):
        super().__init__()
        self.marketURL = 'hitbtc.com'
        self.marketFine = 0.002
        from .adaptedApiForHitBTCMarket import Public
        self.publicAPI = {
            '1': Public(),
        }.get(str(version), Public())


class BinanceMarketApi(AbstractMarketAPI):
    def __init__(self, version=1):
        super().__init__()
        self.marketURL = 'binance.com'
        self.marketFine = 0.002
        from .adaptedApiForBinanceMarket import Public
        self.publicAPI = {
            '1': Public(),
        }.get(str(version), Public())


def getApi(byName, withVersion=1):
    switcher = {
        'binance.com': BinanceMarketApi(withVersion),
        'bitfinex.com': BitfinexMarketApi(withVersion),
        'wex.nz': WexMarketApi(withVersion),
        'yobit.io': YobitMarketApi(withVersion),
        'hitbtc.com': HitBTCMarketApi(withVersion),
    }
    return switcher.get(byName, None), list(switcher.keys())
