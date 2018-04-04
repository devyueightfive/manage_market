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
        except Exception:
            return None

    def get_trades(self, coin_from, coin_to, **params):
        try:
            return self.public_strategy.trades(self.market_url, coin_from, coin_to, **params)
        except Exception:
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


def get_api(api_name, version=1):
    switcher = {
        'bitfinex.com': BitfinexApi(version),
        'wex.nz': WexApi(version),
        'yobit.io': YobitApi(version)
    }
    return switcher.get(api_name, None), list(switcher.keys())
