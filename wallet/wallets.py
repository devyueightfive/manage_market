import json
from builtins import staticmethod

from TraderClasses import Return
from settings import pathToWalletsFile


class Wallets:
    # data stored in wallets_file as dictionary
    # entry = {'markets':..., 'wallets':...}
    # wallet keys = ['name', 'market', 'key', 'sign', 'robots']

    @staticmethod
    def getWallet(byName: str):  # return wallet as dictionary
        try:
            with open(file=pathToWalletsFile, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        if byName not in wallets['wallets']:
            return Return(-1, 'Warning', f"'{byName}' not in 'wallets'.")
        return Return(wallets['wallets'][byName], text=f"'{byName}' wallet was selected.")

    @staticmethod
    def save(theWallet: dict):  # save wallet data in wallets_file
        if not Wallets.isWallet(theWallet).Value:
            return Return(-1, 'Error', "Given parameter is not wallet.")
        else:
            try:
                with open(file=pathToWalletsFile, mode="r") as f:
                    wallets = json.load(f)  # load entry as dictionary
            except Exception:
                wallets = {'wallets': {}}
            # save elements in data
            wallets['wallets'][theWallet['name']] = theWallet
            # save file with new data
            try:
                with open(file=pathToWalletsFile, mode="w") as f:
                    json.dump(wallets, f)
            except Exception as e:
                return Return(-1, 'Error', e.__str__())
            return Return(0, text=f"Wallet '{theWallet['name']}' saved")

    @staticmethod
    def add(theWallet):
        return Wallets.save(theWallet)

    @staticmethod
    def deleteWallet(byName):
        try:
            with open(file=pathToWalletsFile, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        if byName not in wallets['wallets']:
            return Return(-1, 'Warning', f"'{byName}' not in 'wallets'.")
        del wallets['wallets'][byName]
        # save file with new data
        try:
            with open(file=pathToWalletsFile, mode="w") as f:
                json.dump(wallets, f)
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        return Return(0, text=f"'{byName}' wallet was deleted.")

    @staticmethod
    def getDictionaryOfWallets():  # return array of wallets as dictionary
        try:
            with open(file=pathToWalletsFile, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Warning', e.__str__())
        return Return(wallets['wallets'])

    @staticmethod
    def isWallet(likeWallet: dict):
        keys = ['name', 'market', 'key', 'sign', 'robots']
        for k in keys:
            if k not in likeWallet.keys():
                return Return(False, 'Error', 'It is not wallet.')
        return Return(True)

    @staticmethod
    def getArrayOfUsedMarkets():
        try:
            with open(file=pathToWalletsFile, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        set_of_markets = set()
        for (k, v) in wallets['wallets'].items():
            set_of_markets.add(v['market'])
        # sort list
        return Return(set(sorted(set_of_markets)))

    @staticmethod
    def getListOfWallets():
        try:
            with open(file=pathToWalletsFile, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        list_of_wallets = list()
        for k in wallets['wallets'].keys():
            list_of_wallets.append(k)
        # sort list
        return Return(sorted(list_of_wallets))

    @staticmethod
    def getListOfRobotNames(byWalletName):  # return list of robot names
        try:
            with open(file=pathToWalletsFile, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return([], 'Error', e.__str__())
        if byWalletName not in wallets['wallets']:
            return Return([], 'Warning', f"'{byWalletName}' not in 'wallets'.")
        wallet = wallets['wallets'][byWalletName]
        robot_names = wallet['robots'].keys()
        return Return(list(robot_names))

    @staticmethod
    def addParameterNameAndValueToWallets(withParameterName,
                                          withParameterValue):  # save market_name in the list of supported markets
        try:
            with open(file=pathToWalletsFile, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:  # not exist file
            wallets = {'wallets': {}, withParameterName: []}
        if withParameterName not in wallets.keys():
            wallets[withParameterName] = []
        # save elements in data
        if withParameterValue not in wallets[withParameterName]:
            wallets[withParameterName].append(withParameterValue)
        # save file with new data
        try:
            with open(file=pathToWalletsFile, mode="w") as f:
                json.dump(wallets, f)
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        return Return(0, text=f"'{withParameterValue}' added to '{withParameterName}'")

    @staticmethod
    def removeValue(forParameterName, withParameterValue):
        try:
            with open(file=pathToWalletsFile, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        if withParameterValue not in wallets[forParameterName]:
            return Return(-1, 'Warning', f"'{withParameterValue}' not in '{forParameterName}'.")
        wallets[forParameterName].remove(withParameterValue)
        # save file with new data
        try:
            with open(file=pathToWalletsFile, mode="w") as f:
                json.dump(wallets, f)
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        return Return(0, text=f"'{withParameterValue}' was deleted in '{forParameterName}'.")

    @staticmethod
    def getValueRange(byParameterName):
        try:
            with open(file=pathToWalletsFile, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        parameter_set = set()
        for v in wallets[byParameterName]:
            parameter_set.add(v)
        # sort list
        return Return(set(sorted(parameter_set)))
