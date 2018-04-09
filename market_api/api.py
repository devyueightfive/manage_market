class AbstractAPI:
    """ Base Api class.

    """
    market_url = None
    public_strategy = None
    authorize_strategy = None

    def __init__(self, version=1):
        self._version = version

    def get_ticker(self, coin_from, coin_to):
        try:
            return self.public_strategy.ticker(self.market_url, coin_from, coin_to)
        except Exception as e:
            print("Error ", e.__str__())
            return None

    # return template
    # {'eth_usd': {'avg': 405.804125,
    #              'buy': 393.275,
    #              'high': 425.48325,
    #              'last': 392.17251,
    #              'low': 386.125,
    #              'sell': 391.08001,
    #              'updated': 1522849214,
    #              'vol': 3237730.99523,
    #              'vol_cur': 7941.64073}}

    def get_trades(self, coin_from, coin_to, **params):
        try:
            return self.public_strategy.trades(self.market_url, coin_from, coin_to, **params)
        except Exception as e:
            print("Error ", e.__str__())
            return None


class WexApi(AbstractAPI):
    def __init__(self, version=1):
        super().__init__(version)
        self.market_url = 'wex.nz'
        from .wex_api import Public
        self.public_strategy = {
            '1': Public(),
        }.get(str(version), Public())


class BitfinexApi(AbstractAPI):
    def __init__(self, version=1):
        super().__init__(version)
        self.market_url = 'bitfinex.com'
        from .bitfinex_api import Public
        self.public_strategy = {
            '1': Public(),
        }.get(str(version), Public())


class YobitApi(AbstractAPI):
    def __init__(self, version=1):
        super().__init__(version)
        self.market_url = 'yobit.io'
        from .yobit_api import Public
        self.public_strategy = {
            '1': Public(),
        }.get(str(version), Public())


class HitBTCApi(AbstractAPI):
    def __init__(self, version=1):
        super().__init__(version)
        self.market_url = 'hitbtc.com'
        from .hitbtc_api import Public
        self.public_strategy = {
            '1': Public(),
        }.get(str(version), Public())


def get_api(api_name, version=1):
    switcher = {
        'bitfinex.com': BitfinexApi(version),
        'wex.nz': WexApi(version),
        'yobit.io': YobitApi(version),
        'hitbtc.com': HitBTCApi(version)
    }
    return switcher.get(api_name, None), list(switcher.keys())
