# wallet keys = ['name', 'market', 'key', 'sign', 'robots']
class BalanceModel:
    attributes = ['coin', 'amount']
    attribute_length = [50, 90]


class OrderModel:
    attributes = ['id', 'pair', 'type', 'amount', 'rate', 'timestamp_created']
    attribute_length = [100, 50, 30, 90, 50, 150]
