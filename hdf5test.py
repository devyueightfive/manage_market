import os
import time

import tables

import market_api


def write_data_to_h5(trade_data: list):
    with tables.open_file(f_path, mode='r+', title='Test file') as file:
        table = file.get_node('/trade_group', 'cryptostats')
        if table.nrows:
            last_id = table[-1]['tid']
        else:
            last_id = 0
        trade = table.row
        for d in trade_data:
            if d['tid'] > last_id:
                fields = ['tid', 'type', 'timestamp', 'amount', 'price']
                for e in fields:
                    trade[e] = d.get(e)
                print(f"\t{d}")
                trade.append()
        table.flush()
        result = table.nrows
        table.close()
    return result


def read_data_from_h5():
    if os.path.exists(f_path):
        with tables.open_file(f_path, mode='r+', title='Test file') as file:
            table = file.get_node('/trade_group', 'cryptostats')
            data = [(x['tid'], x['type'], x['timestamp'], x['price'], x['amount']) for x in table.iterrows()]


if __name__ == "__main__":
    clear_h5()
    my_api = market_api.getApi(url)[0]
    last_rows = 0
    while True:
        data = my_api.requestTradesInfo(coin, currency, withRowLimit=150)
        sorted_data = sorted(data.get(pair), key=lambda t: t['tid'])
        print(len(sorted_data))
        rows = write_data_to_h5(sorted_data)
        print(f"{time.ctime()}: added {rows - last_rows}")
        last_rows = rows
        time.sleep(10)
