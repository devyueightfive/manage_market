from os import remove

from settings import wallets_file
from wallet.wallets import Wallets

if __name__ == '__main__':
    my_wallet = {'name': 'Nebraska wex',
                 'market': 'wex.nz',
                 'key': 'weweqwe334sadsd',
                 'sign': 'weqwewqe',
                 'robots': {'Edges': {},
                            'Fast': {}}
                 }
    your_wallet = {'name': 'Alaska yobit',
                   'market': 'yobit.io',
                   'key': 'weweqwe334sadsd',
                   'sign': 'weqwewqe',
                   'robots': {}
                   }
    other_wallet = {'name': 'John wex',
                    'market': 'binance.nz',
                    'key': 'weweqwe334sadsd',
                    'sign': 'weqwewqe'}

    ms = ['wex.nz', 'yobit.io']
    ps = ['btc_usd', 'eth_usd']

    print('\n#0')
    try:
        remove(wallets_file)
    except Exception as e:
        print(e.__str__())
    print('\n#1')
    print(Wallets.get_wallet_by_name('John'))
    print('\n#2')
    print(Wallets.is_wallet(my_wallet))
    print('\n#3')
    print(Wallets.is_wallet(other_wallet))
    print('\n#4')
    print(Wallets.add_wallet(my_wallet))
    print('\n#5')
    print(Wallets.add_wallet(other_wallet))
    print('\n#6')
    print(Wallets.add_wallet(your_wallet))
    print('\n#7')
    print(Wallets.get_wallet_by_name('Nebraska wex'))
    print('\n#8')
    print(Wallets.get_wallet_by_name('Lucy wex'))
    print('\n#9')
    print(Wallets.get_set_of_used_markets())
    print('\n#10')
    print(Wallets.get_list_of_wallets())
    print('\n#11')
    print(Wallets.get_list_of_robot_names_by_wallet_name('Nebraska wex'))
    print('\n#12')
    print(Wallets.get_list_of_robot_names_by_wallet_name('Alaska yobit'))
    print('\n#13')
    print(Wallets.get_list_of_robot_names_by_wallet_name('Lucy yobit'))
    # print('\n#14')
    # print(Wallets.delete_wallet_by_name('Alaska yobit'))
    # print('\n#15')
    # print(Wallets.delete_wallet_by_name('Red yobit'))
    # print('\n#16')
    # print(Wallets.get_list_of_wallets())
    print('\n#17')
    for m in ms:
        print(Wallets.add_parameter_value('markets', m))
    print('\n#18')
    print(Wallets.add_parameter_value('markets', 'yobit.ru'))
    print('\n#19')
    print(Wallets.value_range_of_parameter('markets'))
    print('\n#20')
    print(Wallets.delete_parameter_value('markets', 'yobit.ru'))
    print('\n#21')
    print(Wallets.delete_parameter_value('markets', 'another.market'))
    print('\n#22')
    print(Wallets.value_range_of_parameter('markets'))
    print('\n#23')
    for p in ps:
        print(Wallets.add_parameter_value('pairs', p))
