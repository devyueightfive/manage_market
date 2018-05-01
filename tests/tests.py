from os import remove

from settings import pathToWalletsFile
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
        remove(pathToWalletsFile)
    except Exception as e:
        print(e.__str__())
    print('\n#1')
    print(Wallets.getWallet('John'))
    print('\n#2')
    print(Wallets.isWallet(my_wallet))
    print('\n#3')
    print(Wallets.isWallet(other_wallet))
    print('\n#4')
    print(Wallets.add(my_wallet))
    print('\n#5')
    print(Wallets.add(other_wallet))
    print('\n#6')
    print(Wallets.add(your_wallet))
    print('\n#7')
    print(Wallets.getWallet('Nebraska wex'))
    print('\n#8')
    print(Wallets.getWallet('Lucy wex'))
    print('\n#9')
    print(Wallets.getArrayOfUsedMarkets())
    print('\n#10')
    print(Wallets.getListOfWallets())
    print('\n#11')
    print(Wallets.getListOfRobotNames('Nebraska wex'))
    print('\n#12')
    print(Wallets.getListOfRobotNames('Alaska yobit'))
    print('\n#13')
    print(Wallets.getListOfRobotNames('Lucy yobit'))
    # print('\n#14')
    # print(Wallets.delete_wallet_by_name('Alaska yobit'))
    # print('\n#15')
    # print(Wallets.delete_wallet_by_name('Red yobit'))
    # print('\n#16')
    # print(Wallets.get_list_of_wallets())
    print('\n#17')
    for m in ms:
        print(Wallets.addParameterNameAndValueToWallets('markets', m))
    print('\n#18')
    print(Wallets.addParameterNameAndValueToWallets('markets', 'yobit.ru'))
    print('\n#19')
    print(Wallets.getValueRange('markets'))
    print('\n#20')
    print(Wallets.removeValue('markets', 'yobit.ru'))
    print('\n#21')
    print(Wallets.removeValue('markets', 'another.market'))
    print('\n#22')
    print(Wallets.getValueRange('markets'))
    print('\n#23')
    for p in ps:
        print(Wallets.addParameterNameAndValueToWallets('pairs', p))
