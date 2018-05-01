from dateutil import parser

from marketAPI.apiForHitBTCMarket import PublicRequests


class Public(PublicRequests):
    @staticmethod
    def requestTicker(forCryptoCoin: str, forCurrencyCoin: str, fromURL: str):
        """24 hour price change statistics."""
        response = PublicRequests.requestTicker(forCryptoCoin, forCurrencyCoin, fromURL)
        pairSymbol = Public.getTradePairSymbolFrom(forCryptoCoin, forCurrencyCoin)
        return {pairSymbol: {'avg': (float(response['high']) + float(response['low'])) / 2,
                             'buy': float(response['bid']),
                             'high': float(response['high']),
                             'last': float(response['last']),
                             'low': float(response['low']),
                             'sell': float(response['ask']),
                             'updated': int(float(parser.parse(response['timestamp']).timestamp())),
                             'vol': float(response['volume']),
                             'vol_cur': float(response['volumeQuote'])
                             }
                }

    @staticmethod
    def requestTrades(forCryptoCoin: str, forCurrencyCoin: str, fromURL: str, withRowLimit=999):
        """Get recent trades (up to last 999)."""

        def convert(tradeResponse):
            tradePair = Public.getTradePairSymbolFrom(forCryptoCoin, forCurrencyCoin)
            convertedTrades = {tradePair: tradeResponse}
            adapter = {
                'type': 'side',
                'amount': 'quantity',
                'tid': 'id'
            }
            for trade in convertedTrades.get(tradePair):
                for k, v in adapter.items():
                    trade[k] = trade.get(v, 0)
                    trade.pop(v)
                trade['type'] = 'bid' if trade.get('type') == 'buy' else 'ask'
                trade['timestamp'] = int(float(parser.parse(trade.get('timestamp', 0)).timestamp()))
            return convertedTrades

        response = PublicRequests.requestTrades(forCryptoCoin, forCurrencyCoin, fromURL, withRowLimit=withRowLimit)
        return convert(response)
