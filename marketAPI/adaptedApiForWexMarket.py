from marketAPI.apiForWEXMarket import PublicRequests, TradeRequests


class Public(PublicRequests):
    @staticmethod
    def requestTicker(forCryptoCoin: str, forCurrencyCoin: str, fromURL: str):
        """24 hour price change statistics."""
        response = PublicRequests.requestTicker(forCryptoCoin, forCurrencyCoin, fromURL)
        for symbol, element in response.items():
            element['vol'], element['vol_cur'] = element['vol_cur'], element['vol']
        return response

    @staticmethod
    def requestTrades(forCryptoCoin: str, forCurrencyCoin: str, fromURL: str, withRowLimit=5000):
        """Get recent trades (up to last 1999)."""
        return PublicRequests.requestTrades(forCryptoCoin, forCurrencyCoin, fromURL, withRowLimit=withRowLimit)


class TradeApi(TradeRequests):
    @staticmethod
    def requestBalance(forWallet: dict):
        balance = {'funds': {}, 'orders': {}}
        response = TradeRequests.requestBalanceInfo(forWallet)
        if response['success'] == 1:
            funds = response.get('return', {}).get('funds', {})
            for k, v in funds.items():
                if v != 0:
                    balance['funds'][k] = v
            response = TradeRequests.requestActiveOrdersInfo(forWallet)
            if response['success'] == 1 and 'return' in response.keys():
                balance['orders'].update(response['return'])
        return balance

    @staticmethod
    def requestOrderCreation(forTradePair: str, withOrderType: str, withRate: float, withAmount: float, inWallet: dict):
        return TradeRequests.trade(inWallet, forTradePair, withOrderType, withRate, withAmount)

    @staticmethod
    def requestOrderCancellation(forOrderID: str, inWallet: dict):
        return TradeRequests.cancel_order(inWallet, forOrderID)
