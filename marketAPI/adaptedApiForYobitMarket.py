from marketAPI.apiForYobitMarket import PublicRequests, TradeRequests

http_timeout = 15

convertibleCoins = ['btc', 'eth', 'doge', 'waves', 'usd', 'rur']
currencyCoins = ['usd', 'rur']


class Public(PublicRequests):
    @staticmethod
    def requestTicker(forCryptoCoin: str, forCurrencyCoin: str, fromURL: str):
        """24 hour price change statistics."""
        response = PublicRequests.requestTicker(forCryptoCoin, forCurrencyCoin, fromURL)
        for symbol, element in response.items():
            element['vol'], element['vol_cur'] = element['vol_cur'], element['vol']
        return response

    @staticmethod
    def requestTrades(forCryptoCoin: str, forCurrencyCoin: str, fromURL: str, withRowLimit=1999):
        """Get recent trades (up to last 1999)."""
        return PublicRequests.requestTrades(forCryptoCoin, forCurrencyCoin, fromURL, withRowLimit=withRowLimit)


class TradeApi(TradeRequests):
    @staticmethod
    def requestBalance(forWallet: dict):
        balance = {'funds': {}, 'orders': {}}
        response = TradeRequests.requestBalanceInfo(forWallet)
        if response['success'] == 1:
            funds = response.get('return', {}).get('funds', {})
            for cryptoCoin, amount in funds.items():
                if amount != 0:
                    balance['funds'][cryptoCoin] = amount
            fundsIncludedInOrders = response.get('return', {}).get('funds_incl_orders', {})
            cryptoCoinsInOrders = [cryptoCoin for cryptoCoin, amount in fundsIncludedInOrders.items() if amount]
            for coin in cryptoCoinsInOrders:
                for convertibleCoin in convertibleCoins:
                    if coin != convertibleCoin and coin not in currencyCoins:
                        tradePair = f"{coin}_{convertibleCoin}"
                        response = TradeRequests.requestActiveOrdersInfo(forWallet, tradePair)
                        if response['success'] == 1 and 'return' in response.keys():
                            balance['orders'].update(response['return'])
        return balance

    @staticmethod
    def requestOrderCreation(forTradePair: str, withOrderType: str, withRate: float, withAmount: float, inWallet: dict):
        return TradeRequests.trade(inWallet, forTradePair, withOrderType, withRate, withAmount)

    @staticmethod
    def requestOrderCancellation(forOrderID: str, inWallet: dict):
        return TradeRequests.cancel_order(inWallet, forOrderID)
