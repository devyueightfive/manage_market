from marketAPI.apiForBitfinexMarket import PublicRequests


class Public(PublicRequests):
    @staticmethod
    def requestTicker(forCryptoCoin: str, forCurrencyCoin: str, fromURL: str):
        """24 hour price change statistics."""
        response = PublicRequests.requestTicker(forCryptoCoin, forCurrencyCoin, fromURL)
        tradePair = Public.getTradePairSymbolFrom(forCryptoCoin, forCurrencyCoin)
        return {tradePair: {'avg': float(response['mid']),
                            'buy': float(response['bid']),
                            'high': float(response['high']),
                            'last': float(response['last_price']),
                            'low': float(response['low']),
                            'sell': float(response['ask']),
                            'updated': int(float(response['timestamp'])),
                            'vol': float(response['volume']),
                            'vol_cur': float(0)
                            }
                }

    @staticmethod
    def requestTrades(forCryptoCoin: str, forCurrencyCoin: str, fromURL: str, withRowLimit=999):
        """Get recent trades (up to last 999)."""

        def convert(tradeResponse):
            for trade in tradeResponse:
                trade['type'] = 'bid' if trade.get('type') == 'buy' else 'ask'
            tradePair = Public.getTradePairSymbolFrom(forCryptoCoin, forCurrencyCoin)
            convertedTrades = {tradePair: tradeResponse}
            return convertedTrades

        response = PublicRequests.requestTrades(forCryptoCoin, forCurrencyCoin, fromURL, withRowLimit=withRowLimit)
        return convert(response)
