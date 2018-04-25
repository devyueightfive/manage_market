# wallet keys = ['name', 'market', 'key', 'sign', 'robots']
class WalletModel(object):
    def __init(self, wallet: dict):
        pass


class BalanceModel(object):
    attributes = ['coin', 'amount']
    attribute_length = [50, 90]

    def __init__(self):
        self.funds = {}
        self.orders = {}


class OrderModel(object):
    attributes = ['id', 'pair', 'type',
                  'amount', 'rate', 'timestamp_created']
    attribute_length = [100, 50, 30, 90, 50, 150]

    def __init__(self):
        self.id = None
        self.pair = None
        self.type = None  # buy/sell
        self.start_amount = None  # starting amount at order creation
        self.amount = None  # order amount remaining to buy or to sell
        self.rate = None  # price of buying or selling
        self.timestamp_created = None  # order creation time
        self.status = None  # 0 - active,
        # 1 - fulfilled and closed,
        # 2 - cancelled,
        # 3 - cancelled after partially fulfilled.
