import os
import time

import tables

import settings

tradePair = 'eth_usd'
url = 'wex.nz'.replace('.', '')

dayInSeconds = 60 * 60 * 24
trades24h = None

if __name__ == '__main__':
    if os.path.exists(settings.pathToTradesFile):
        with tables.open_file(settings.pathToTradesFile, 'r') as file:
            where = f'/{tradePair}/{url}'
            tableWithTrades = file.get_node(where, 'trades')
            lastDayInSeconds = time.time() - dayInSeconds
            print(time.ctime(lastDayInSeconds))
            trades24h = [dict(tid=row['tid'], type=row['type'], timestamp=row['timestamp'], price=row['price'],
                              amount=row['amount']) for row in
                         tableWithTrades.where(f'timestamp >= {int(lastDayInSeconds)}')]
            tableWithTrades.close()

    if trades24h:
        print(len(trades24h))
        print(time.ctime(trades24h[0]['timestamp']))
        print(time.ctime(trades24h[-1]['timestamp']))
