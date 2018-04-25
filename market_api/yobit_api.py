# https://github.com/devyueightfive
# used api from https://github.com/acidvegas/btc-e
# utf-8

import market_api.wex_api as wex

"""YOBIT API looks like WEX API. 
"""


class Public(wex.Public):
    pass


class TradeApi(wex.TradeApi):
    pass
