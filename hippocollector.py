import os
import queue
import threading
import time

import tables

from market_api import cryptoMarketApi

'list of available markets(urls)'
urls = cryptoMarketApi.getApi(None)[1]
'list of times when market trades were updated'
updated = []
for i in urls:
    updated.append(0)
'pause between trade requests'
delay = 12
'list of gathered crypto coins'
coins = ['btc', 'eth']
currency = ['usd']
pairs = [f"{coin}_{cur}" for coin in coins for cur in currency]
'queue for storing trade responses'
q = queue.Queue()

'paths'
my_path = os.path.abspath(os.curdir)
data_directory = "\\".join([my_path, "data"])
trades_file = "\\".join([data_directory, "trades.h5"])

'table structure'


class Trades(tables.IsDescription):
    tid = tables.Int32Col()
    type = tables.StringCol(3)
    timestamp = tables.Float32Col()
    amount = tables.Float32Col()
    price = tables.Float32Col()


'thread for saving trade responses to h5base'


class HippoCollector(threading.Thread):
    def __init__(self, outer_queue):
        super().__init__(daemon=True)
        self.queue = outer_queue

    def run(self):
        while True:
            item = self.queue.get()
            self.save(item)
            self.queue.task_done()

    def save(self, item):
        pass


class WolfRetriever(threading.Thread):
    def __init__(self, outer_queue, outer_url):
        super().__init__(daemon=True)
        self.queue = outer_queue
        self.url = outer_url

    def run(self):
        wolf_api = cryptoMarketApi.getApi(self.url)[0]
        while True:
            self.catch_trades(wolf_api)
            time.sleep(delay)

    def catch_trades(self, outer_api):
        for coin in coins:
            for cur in currency:
                sheeps = outer_api.requestTradesInfo(coin, cur, withRowLimit=150)
                p = f"{coin}_{cur}"
                print(f"<{self.url}> : ({len(sheeps[p])}) : {sheeps}")
                time.sleep(3)


def create_h5():
    """create new trade storage"""
    if not os.path.exists(trades_file):
        with tables.open_file(trades_file, mode='w', title='Crypto Trades') as h5base:
            'create groups'
            for pair in pairs:
                h5base.create_group('/', pair, title=f"stats for {pair}")
                for u in urls:
                    url_group = h5base.create_group(f'/{pair}', u.replace('.', ''), title=f"market")
                    table = h5base.create_table(url_group, 'trades', Trades, title="trade table")
                    table.close()


if __name__ == "__main__":
    print(trades_file)
    create_h5()

    'start collector for storing trade responses'
    # hippo = HippoCollector(q)
    # hippo.start()

    wolves = []
    for url in urls:
        w = WolfRetriever(q, url)
        wolves.append(w)
        w.start()

    while True:
        time.sleep(100)

    # while True:
    #     for index in range(len(urls)):
    #         if (time.time() - updated[index]) > delay:
    #             updated[index] = time.time()
    #             my_api = api.get_api(urls[index])[0]
    #             for coin_from in coins:
    #                 time.sleep(1)
    #                 for coin_to in currency:
    #                     response = my_api.get_trades(coin_from, coin_to, limit=500)
    #                     data = {urls[index]: response}
    #                     q.put(data)
    #     time.sleep(1)
