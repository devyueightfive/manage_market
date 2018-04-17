# wallet keys = ['name', 'market', 'key', 'sign', 'robots']
class WalletModel(object):
    def __init(self, wallet: dict):
        pass


class Balance(object):
    def __init__(self):
        pass


class OrderModel(object):
    attributes = ['id', 'pair', 'type', 'start_amount',
                  'amount', 'rate', 'timestamp_created', 'status']

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
