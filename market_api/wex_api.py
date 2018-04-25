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

    @staticmethod
    def depth(market_name, dfrom, dto, limit=None):
        if limit:  # 150 Default / 5000 Max
            return Public.api_call(market_name, f'depth/{dfrom}_{dto}?limit={limit}')
        else:
            return Public.api_call(market_name, f'depth/{dfrom}_{dto}')

    @staticmethod
    def trades(market_name, dfrom, dto, limit=None):
        if limit:
            return Public.api_call(market_name, f'trades/{dfrom}_{dto}?limit={limit}')
        else:
            return Public.api_call(market_name, f'trades/{dfrom}_{dto}')


class TradeApi:
    no_once = int(time.time())

    @staticmethod
    def signature(market: dict, params: dict):
        sig = hmac.new(market['sign'].encode(), params.encode(), hashlib.sha512)
        return sig.hexdigest()

    @staticmethod
    def api_call(market: dict, method_name: str, params: dict):
        params['method'] = method_name
        params['nonce'] = str(TradeApi.no_once)
        TradeApi.no_once += 1
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
    def getinfo(wallet: dict):
        return TradeApi.api_call(wallet, 'getInfo', {})

    @staticmethod
    def trade(wallet: dict, tpair: str, ttype: str, trate: float, tamount: float):
        params = {'pair': tpair, 'type': ttype, 'rate': trate, 'amount': tamount}
        return TradeApi.api_call(wallet, 'Trade', params)

    @staticmethod
    def active_orders(wallet: dict, tpair=None):
        if tpair:
            params = {'pair': tpair}
            return TradeApi.api_call(wallet, 'ActiveOrders', params)
        else:
            return TradeApi.api_call(wallet, 'ActiveOrders', {})

    @staticmethod
    def order_info(wallet: dict, order_id: str):
        params = {'order_id': order_id}
        return TradeApi.api_call(wallet, 'OrderInfo', params)

    @staticmethod
    def cancel_order(wallet: dict, order_id: str):
        params = {'order_id': order_id}
        return TradeApi.api_call(wallet, 'CancelOrder', params)

    @staticmethod
    def trade_history(wallet, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend, tpair):
        params = {'from': tfrom, 'count': tcount, 'from_id': tfrom_id, 'end_id': tend_id, 'order': torder,
                  'since': tsince, 'end': tend, 'pair': tpair}
        return TradeApi.api_call(wallet, 'TradeHistory', params)

    @staticmethod
    def trans_history(wallet, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend):
        params = {'from': tfrom, 'count': tcount, 'from_id': tfrom_id, 'end_id': tend_id, 'order': torder,
                  'since': tsince, 'end': tend}
        return TradeApi.api_call(wallet, 'TransHistory', params)

    @staticmethod
    def coin_deposit_address(wallet, coin_name):
        params = {'coinName': coin_name}
        return TradeApi.api_call(wallet, 'CoinDepositAddress', params)

    @staticmethod
    def withdraw_coin(wallet, coin_name, amount,
                      address):  # Requires a special API key. See Trade API docs for more information.
        params = {'coinName': coin_name, 'amount': amount, 'address': address}
        return TradeApi.api_call(wallet, 'WithdrawCoin', params)

    @staticmethod
    def create_coupon(wallet, currency, amount,
                      receiver):  # Requires a special API key. See Trade API docs for more information.
        params = {'currency': currency, 'amount': amount, 'receiver': receiver}
        return TradeApi.api_call(wallet, 'CreateCoupon', params)

    @staticmethod
    def redeem_coupon(wallet,
                      coupon):  # Requires a special API key. See Trade API docs for more information.
        params = {'coupon': coupon}
        return TradeApi.api_call(wallet, 'RedeemCoupon', params)
