import os
import queue
import threading
import time

import tables

from marketAPI import cryptoMarketApi

'list of available markets(urls)'
marketURLs = cryptoMarketApi.getApi(None)[1]
'list of times when market trades were updated'
updated = []
for mu in marketURLs:
    updated.append(0)
'pause between trade requests'
delayForRequests = 13  # in seconds
'list of gathered crypto coins'
cryptoCoins = ['btc', 'eth']
currencyCoins = ['usd']
tradePairs = [f"{coin}_{cur}" for coin in cryptoCoins for cur in currencyCoins]
'queue for storing trade responses'
queueForResponses = queue.Queue()

'paths'
pathToCurrentDirectory = os.path.abspath(os.curdir)
pathToDataDirectory = os.path.join(pathToCurrentDirectory, "data")
pathToTradesFile = os.path.join(pathToCurrentDirectory, "trades.h5")

'table structure'


class DescriptionForTradesTable(tables.IsDescription):
    price = tables.Float32Col()
    amount = tables.Float32Col()
    timestamp = tables.Float32Col()
    tid = tables.Int32Col()
    type = tables.StringCol(3)


'thread for saving trade responses to h5base'


class HippoCollector(threading.Thread):
    def __init__(self, withResponseQueue):
        super().__init__(daemon=True)
        self.queue = withResponseQueue

    def run(self):
        while True:
            item = self.queue.get()
            self.save(item, pathToTradesFile)
            self.queue.task_done()

    @staticmethod
    def save(item, toTradesFile):
        numberOfSavedTradeRows = 0
        with tables.open_file(toTradesFile, mode='r+') as file:
            table = file.get_node(item['group'], 'trades')
            if table.nrows:
                tidInLastTableRow = table[-1]['tid']
            else:
                tidInLastTableRow = 0

            tableRow = table.row
            for trade in item['trades']:
                if trade['tid'] > tidInLastTableRow:
                    fields = ['tid', 'type', 'timestamp', 'amount', 'price']
                    for f in fields:
                        tableRow[f] = trade.get(f)
                    # print(f"\t{trade}")
                    tableRow.append()
                    numberOfSavedTradeRows += 1
            table.flush()
            table.close()
        print(f"{time.ctime()}:[{item['group']}]: {numberOfSavedTradeRows} rows saved.")


class TradesRequester(threading.Thread):
    def __init__(self, withResponseQueue, withMarketURL):
        super().__init__(daemon=True)
        self.queue = withResponseQueue
        self.url = withMarketURL

    def run(self):
        marketAPI = cryptoMarketApi.getApi(self.url)[0]
        while True:
            try:
                self.requestTradesFrom(marketAPI)
            except Exception as err:
                print(err)
            time.sleep(delayForRequests)

    def requestTradesFrom(self, marketAPI):
        isFirstTime = True
        for crypto in cryptoCoins:
            for currency in currencyCoins:
                if isFirstTime:
                    trades = marketAPI.requestTradesInfo(crypto, currency, withRowLimit=None)
                else:
                    trades = marketAPI.requestTradesInfo(crypto, currency, withRowLimit=200)
                tradePair = f"{crypto}_{currency}"
                groupForTable = f"/{tradePair}/{self.url.replace('.', '')}"
                if trades:
                    item = {'group': groupForTable, 'trades': sorted(trades[tradePair],
                                                                     key=lambda x: x['tid'])}
                    self.queue.put(item)
                else:
                    print(f"Error for {groupForTable} trade request.")
                time.sleep(5)


def create_h5():
    """create new trade storage"""
    if not os.path.exists(pathToTradesFile):
        with tables.open_file(pathToTradesFile, mode='w', title='Crypto Trades') as h5base:
            'create groups'
            for tradePair in tradePairs:
                h5base.create_group('/', tradePair, title=f"stats for {tradePair}")
                for u in marketURLs:
                    urlGroup = h5base.create_group(f'/{tradePair}', u.replace('.', ''), title=f"market")
                    table = h5base.create_table(urlGroup, 'trades', DescriptionForTradesTable, title="trade table")
                    table.close()


if __name__ == "__main__":
    print(pathToTradesFile)
    create_h5()

    'start collector as hippo'
    hippo = HippoCollector(queueForResponses)
    hippo.start()
    'start requesters as wolves'
    wolves = []
    for url in marketURLs:
        wolf = TradesRequester(queueForResponses, url)
        wolves.append(wolf)
        wolf.start()

    'infinite loop'
    while True:
        time.sleep(100)
