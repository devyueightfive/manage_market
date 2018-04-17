import os

my_path = os.path.abspath(os.curdir)
wallets_file = "\\".join([my_path, "json\\wallets.json"])
balance_file = "\\".join([my_path, "json\\balance.json"])
active_orders_file = "\\".join([my_path, "\\json\\active_orders.json"])
