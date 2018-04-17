class AbstractAPI:
    """ Base MarketApi class.
    """
    market_url = None
    public_strategy = None
    authorize_strategy = None

    def __init__(self, version=1):
        self._version = version

    def get_ticker(self, coin_from, coin_to):
        try:
            return self.public_strategy.getTicker(self.market_url, coin_from, coin_to)
        except Exception as e:
            print("Error ", e.__str__())
            return None

    def get_trades(self, coin_from, coin_to):
        try:
            return self.public_strategy.getTrades(self.market_url, coin_from, coin_to)
        except Exception as e:
            print("Error ", e.__str__())
            return None

    def get_balance(self, wallet: dict):
        """Response for the wallet Balance
        :param wallet: wallet.keys()->['name','market','sign','orders']
        :return: dictionary of Balance
        """
        try:
            return self.authorize_strategy.getBalanceInfo(wallet)
        except Exception as e:
            print("Error ", e.__str__())
            return None


class WexApi(AbstractAPI):
    def __init__(self, version=1):
        super().__init__(version)
        self.market_url = 'wex.nz'
        from .wex_api import Public, TradeApi
        self.public_strategy = {
            '1': Public(),
        }.get(str(version), Public())
        self.authorize_strategy = {
            '1': TradeApi(),
        }.get(str(version), TradeApi())


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
        from .adapter_yobit import Public, TradeApi
        self.public_strategy = {
            '1': Public(),
        }.get(str(version), Public())
        self.authorize_strategy = {
            '1': TradeApi(),
        }.get(str(version), TradeApi())


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
