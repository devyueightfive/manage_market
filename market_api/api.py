class AbstractAPI:
    """ Base MarketApi class.
    """
    market_url = None
    public_strategy = None
    authorize_strategy = None

    market_fine = 0

    def __init__(self, version=1):
        self._version = version

    def get_ticker(self, coin_from, coin_to):
        try:
            return self.public_strategy.getTicker(self.market_url, coin_from, coin_to)
        except Exception as e:
            print(f"{self.market_url} Ticker error:", e.__str__())
            return None

    def get_trades(self, coin_from, coin_to, limit=None):
        try:
            if limit:
                return self.public_strategy.getTrades(self.market_url, coin_from, coin_to, limit=limit)
            else:
                return self.public_strategy.getTrades(self.market_url, coin_from, coin_to)
        except Exception as e:
            print(f"{self.market_url} Trades error:", e.__str__())
            return None

    def get_balance(self, wallet: dict):
        """Request for Wallet Balance"""
        try:
            return self.authorize_strategy.getBalanceInfo(wallet)
        except Exception as e:
            print(f"{self.market_url} Balance error:", e.__str__())
            return None

    def create_order(self, wallet: dict, pair: str, stype: str, rate: float, amount: float):
        """Request for Order Creation"""
        try:
            return self.authorize_strategy.createOrder(wallet, pair, stype, rate, amount)
        except Exception as e:
            print(f"{self.market_url} Create Order error:", e.__str__())
            return None

    def cancel_order(self, wallet: dict, order_id: str):
        """Request for Order Cancel"""
        try:
            return self.authorize_strategy.cancelOrder(wallet, order_id)
        except Exception as e:
            print(f"{self.market_url} Cancel Order error:", e.__str__())
            return None


class WexApi(AbstractAPI):
    def __init__(self, version=1):
        super().__init__(version)
        self.market_url = 'wex.nz'
        self.market_fine = 0.002
        from .adapter_wex import Public, TradeApi
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
        self.market_fine = 0.002
        from .adapter_bitfinex import Public
        self.public_strategy = {
            '1': Public(),
        }.get(str(version), Public())


class YobitApi(AbstractAPI):
    def __init__(self, version=1):
        super().__init__(version)
        self.market_url = 'yobit.io'
        self.market_fine = 0.002
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
        self.market_fine = 0.002
        from .adapter_hitbtc import Public
        self.public_strategy = {
            '1': Public(),
        }.get(str(version), Public())


class BinanceApi(AbstractAPI):
    def __init__(self, version=1):
        super().__init__(version)
        self.market_url = 'binance.com'
        self.market_fine = 0.002
        from .adapter_binance import Public
        self.public_strategy = {
            '1': Public(),
        }.get(str(version), Public())


def get_api(api_name, version=1):
    switcher = {
        'binance.com': BinanceApi(version),
        'bitfinex.com': BitfinexApi(version),
        'wex.nz': WexApi(version),
        'yobit.io': YobitApi(version),
        'hitbtc.com': HitBTCApi(version),
    }
    return switcher.get(api_name, None), list(switcher.keys())
