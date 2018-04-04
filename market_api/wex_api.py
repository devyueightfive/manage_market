# https://github.com/devyueightfive
# used api from https://github.com/acidvegas/btc-e
# utf-8

import hashlib
import hmac
import http.client
import json
import time
import urllib.parse

# globals
http_timeout = 10


class Public:
    @staticmethod
    def api_call(market_name, method_name):
        conn = http.client.HTTPSConnection(market_name, timeout=http_timeout)
        conn.request('GET', '/api/3/' + method_name)
        response = conn.getresponse().read().decode()
        data = json.loads(response)
        conn.close()
        return data

    @staticmethod
    def info(market_name, ):
        return Public.api_call(market_name, 'info')

    @staticmethod
    def ticker(market_name, tfrom, tto):
        return Public.api_call(market_name, f'ticker/{tfrom}_{tto}')

    # example
    # {'eth_usd': {'avg': 405.804125,
    #              'buy': 393.275,
    #              'high': 425.48325,
    #              'last': 392.17251,
    #              'low': 386.125,
    #              'sell': 391.08001,
    #              'updated': 1522849214,
    #              'vol': 3237730.99523,
    #              'vol_cur': 7941.64073}}

    @staticmethod
    def depth(market_name, dfrom, dto, limit=None):
        if limit:  # 150 Default / 5000 Max
            return Public.api_call(market_name, f'depth/{dfrom}_{dto}?limit={limit}')
        else:
            return Public.api_call(market_name, f'depth/{dfrom}_{dto}')

    @staticmethod
    def trades(market_name, dfrom, dto, limit=None):
        return Public.api_call(market_name, f'trades/{dfrom}_{dto}?limit=5000')
    # {
    #   "type": "bid",
    #   "price": 6990.02,
    #   "amount": 0.00253002,
    #   "tid": 22646685,
    #   "timestamp": 1522857021
    # }


class TradeApi:
    @staticmethod
    def signature(market, params):
        sig = hmac.new(market['sign'].encode(), params.encode(), hashlib.sha512)
        return sig.hexdigest()

    @staticmethod
    def api_call(market, method_name, params):
        params['method'] = method_name
        params['nonce'] = str(time.time()).split('.')[0]
        params = urllib.parse.urlencode(params)
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Key': market['key'],
                   'Sign': TradeApi.signature(market, params)}
        conn = http.client.HTTPSConnection(market['market'], timeout=http_timeout)
        conn.request('POST', '/tapi', params, headers)
        response = conn.getresponse().read().decode()
        data = json.loads(response)
        conn.close()
        return data

    @staticmethod
    def getinfo(market):
        return TradeApi.api_call(market, 'getInfo', {})

    @staticmethod
    def trade(market, tpair, ttype, trate, tamount):
        params = {'pair': tpair, 'type': ttype, 'rate': trate, 'amount': tamount}
        return TradeApi.api_call(market, 'Trade', params)

    @staticmethod
    def active_orders(market, tpair=None):
        if tpair:
            params = {'pair': tpair}
            return TradeApi.api_call(market, 'ActiveOrders', params)
        else:
            return TradeApi.api_call(market, 'ActiveOrders', {})

    @staticmethod
    def order_info(market, order_id):
        params = {'order_id': order_id}
        return TradeApi.api_call(market, 'OrderInfo', params)

    @staticmethod
    def cancel_order(market, order_id):
        params = {'order_id': order_id}
        return TradeApi.api_call(market, 'CancelOrder', params)

    @staticmethod
    def trade_history(market, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend, tpair):
        params = {'from': tfrom, 'count': tcount, 'from_id': tfrom_id, 'end_id': tend_id, 'order': torder,
                  'since': tsince, 'end': tend, 'pair': tpair}
        return TradeApi.api_call(market, 'TradeHistory', params)

    @staticmethod
    def trans_history(market, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend):
        params = {'from': tfrom, 'count': tcount, 'from_id': tfrom_id, 'end_id': tend_id, 'order': torder,
                  'since': tsince, 'end': tend}
        return TradeApi.api_call(market, 'TransHistory', params)

    @staticmethod
    def coin_deposit_address(market, coin_name):
        params = {'coinName': coin_name}
        return TradeApi.api_call(market, 'CoinDepositAddress', params)

    @staticmethod
    def withdraw_coin(market, coin_name, amount,
                      address):  # Requires a special API key. See Trade API docs for more information.
        params = {'coinName': coin_name, 'amount': amount, 'address': address}
        return TradeApi.api_call(market, 'WithdrawCoin', params)

    @staticmethod
    def create_coupon(market, currency, amount,
                      receiver):  # Requires a special API key. See Trade API docs for more information.
        params = {'currency': currency, 'amount': amount, 'receiver': receiver}
        return TradeApi.api_call(market, 'CreateCoupon', params)

    @staticmethod
    def redeem_coupon(market,
                      coupon):  # Requires a special API key. See Trade API docs for more information.
        params = {'coupon': coupon}
        return TradeApi.api_call(market, 'RedeemCoupon', params)
