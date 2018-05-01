from marketAPI.apiForBinanceMarket import PublicRequests


class Public(PublicRequests):

    @staticmethod
    def requestTicker(forCryptoCoin: str, forCurrencyCoin: str, fromURL: str):
        """24 hour price change statistics."""
        response = PublicRequests.requestTicker(forCryptoCoin, forCurrencyCoin, fromURL)
        tradePair = Public.getTradePairSymbolFrom(forCryptoCoin, forCurrencyCoin)
        return {tradePair: {'avg': (float(response['highPrice']) + float(response['lowPrice'])) / 2,
                            'buy': float(response['bidPrice']),
                            'high': float(response['highPrice']),
                            'last': float(response['lastPrice']),
                            'low': float(response['lowPrice']),
                            'sell': float(response['askPrice']),
                            'updated': int(float(response['closeTime']) / 1000),
                            'vol': float(response['volume']),
                            'vol_cur': float(response['quoteVolume'])
                            }
                }

    @staticmethod
    def requestTrades(forCryptoCoin: str, forCurrencyCoin: str, fromURL: str, withRowLimit=500):
        """Get recent trades (up to last 500)."""

        def convert(tradeResponse):
            tradePair = Public.getTradePairSymbolFrom(forCryptoCoin, forCurrencyCoin)
            convertedTrades = {tradePair: tradeResponse}
            adapter = {
                'amount': 'qty',
                'tid': 'id',
                'timestamp': 'time',
                'type': 'isBuyerMaker',
            }
            for trade in convertedTrades.get(tradePair):
                for k, v in adapter.items():
                    trade[k] = trade.get(v, 0)
                    trade.pop(v)
                trade['type'] = 'bid' if trade.get('type') == 'True' else 'ask'
                trade['timestamp'] = float(trade['timestamp']) / 1000
            return convertedTrades

        response = PublicRequests.requestTrades(forCryptoCoin, forCurrencyCoin, fromURL, withRowLimit)
        return convert(response)
