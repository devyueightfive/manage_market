"""https://wex.nz/api/3/docs"""

import hashlib
import hmac
import http.client
import json
import time
import urllib.parse

from marketAPI.HttpRequests import RestRequests

# globals
timeLimitForRequest = 10


class PublicRequests(RestRequests):

    @staticmethod
    def requestMarketInfo(fromURL):
        return PublicRequests.__publicRequest(fromURL, 'info')

    @staticmethod
    def requestTicker(forCryptoCoin, forCurrencyCoin, fromURL):
        """24 hour price change statistics."""
        return PublicRequests.__publicRequest(fromURL, f'ticker/{forCryptoCoin}_{forCurrencyCoin}')

    @staticmethod
    def requestDepth(forCryptoCoin, forCurrencyCoin, fromURL, withRowLimit=None):
        if withRowLimit:  # 150 Default / 5000 Max
            return PublicRequests.__publicRequest(fromURL,
                                                  f'depth/{forCryptoCoin}_{forCurrencyCoin}?limit={withRowLimit}')
        else:
            return PublicRequests.__publicRequest(fromURL, f'depth/{forCryptoCoin}_{forCurrencyCoin}')

    @staticmethod
    def requestTrades(forCryptoCoin, forCurrencyCoin, fromURL, withRowLimit=None):
        """Get recent trades (up to last 5000)."""
        if withRowLimit:
            return PublicRequests.__publicRequest(fromURL,
                                                  f'trades/{forCryptoCoin}_{forCurrencyCoin}?limit={withRowLimit}')
        else:
            return PublicRequests.__publicRequest(fromURL, f'trades/{forCryptoCoin}_{forCurrencyCoin}')

    @staticmethod
    def __publicRequest(toURL, withMethodName):
        URIEndpoint = toURL
        apiPoint = 'api/3'
        return RestRequests.publicRequest(URIEndpoint, apiPoint, withMethodName, timeLimitForRequest)


class TradeRequests:
    no_once = int(time.time())

    @staticmethod
    def signature(market: dict, params: dict):
        sig = hmac.new(market['sign'].encode(), params.encode(), hashlib.sha512)
        return sig.hexdigest()

    @staticmethod
    def api_call(market: dict, method_name: str, params: dict):
        params['method'] = method_name
        params['nonce'] = str(TradeRequests.no_once)
        TradeRequests.no_once += 1
        params = urllib.parse.urlencode(params)
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Key': market['key'],
                   'Sign': TradeRequests.signature(market, params)}
        conn = http.client.HTTPSConnection(market['market'], timeout=timeLimitForRequest)
        conn.request('POST', '/tapi', params, headers)
        response = conn.getresponse().read().decode()
        data = json.loads(response)
        conn.close()
        return data

    @staticmethod
    def requestBalanceInfo(forWallet: dict):
        return TradeRequests.api_call(forWallet, 'getInfo', {})

    @staticmethod
    def trade(wallet: dict, tpair: str, ttype: str, trate: float, tamount: float):
        params = {'pair': tpair, 'type': ttype, 'rate': trate, 'amount': tamount}
        return TradeRequests.api_call(wallet, 'Trade', params)

    @staticmethod
    def requestActiveOrdersInfo(inWallet: dict, forTradePair=None):
        if forTradePair:
            params = {'pair': forTradePair}
            return TradeRequests.api_call(inWallet, 'ActiveOrders', params)
        else:
            return TradeRequests.api_call(inWallet, 'ActiveOrders', {})

    @staticmethod
    def order_info(wallet: dict, order_id: str):
        params = {'order_id': order_id}
        return TradeRequests.api_call(wallet, 'OrderInfo', params)

    @staticmethod
    def cancel_order(wallet: dict, order_id: str):
        params = {'order_id': order_id}
        return TradeRequests.api_call(wallet, 'CancelOrder', params)

    @staticmethod
    def trade_history(wallet, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend, tpair):
        params = {'from': tfrom, 'count': tcount, 'from_id': tfrom_id, 'end_id': tend_id, 'order': torder,
                  'since': tsince, 'end': tend, 'pair': tpair}
        return TradeRequests.api_call(wallet, 'TradeHistory', params)

    @staticmethod
    def trans_history(wallet, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend):
        params = {'from': tfrom, 'count': tcount, 'from_id': tfrom_id, 'end_id': tend_id, 'order': torder,
                  'since': tsince, 'end': tend}
        return TradeRequests.api_call(wallet, 'TransHistory', params)

    @staticmethod
    def coin_deposit_address(wallet, coin_name):
        params = {'coinName': coin_name}
        return TradeRequests.api_call(wallet, 'CoinDepositAddress', params)

    @staticmethod
    def withdraw_coin(wallet, coin_name, amount,
                      address):  # Requires a special API key. See Trade API docs for more information.
        params = {'coinName': coin_name, 'amount': amount, 'address': address}
        return TradeRequests.api_call(wallet, 'WithdrawCoin', params)

    @staticmethod
    def create_coupon(wallet, currency, amount,
                      receiver):  # Requires a special API key. See Trade API docs for more information.
        params = {'currency': currency, 'amount': amount, 'receiver': receiver}
        return TradeRequests.api_call(wallet, 'CreateCoupon', params)

    @staticmethod
    def redeem_coupon(wallet,
                      coupon):  # Requires a special API key. See Trade API docs for more information.
        params = {'coupon': coupon}
        return TradeRequests.api_call(wallet, 'RedeemCoupon', params)
