import json
from builtins import staticmethod

from settings import wallets_file
from settings import Return


class Wallets:
    # data stored in wallets_file as dictionary
    # entry = {'markets':..., 'wallets':...}
    # wallet keys = ['name', 'market', 'key', 'sign', 'robots']

    @staticmethod
    def get_wallet_by_name(wallet_name):  # return wallet as dictionary
        try:
            with open(file=wallets_file, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        if wallet_name not in wallets['wallets']:
            return Return(-1, 'Warning', f"'{wallet_name}' not in 'wallets'.")
        return Return(wallets['wallets'][wallet_name], text=f"'{wallet_name}' wallet was selected.")

    @staticmethod
    def save_wallet(wallet_as_dictionary):  # save wallet data in wallets_file
        if not Wallets.is_wallet(wallet_as_dictionary).value:
            return Return(-1, 'Error', "Given parameter is not wallet.")
        else:
            try:
                with open(file=wallets_file, mode="r") as f:
                    wallets = json.load(f)  # load entry as dictionary
            except Exception:
                wallets = {'wallets': {}}
            # save elements in data
            wallets['wallets'][wallet_as_dictionary['name']] = wallet_as_dictionary
            # save file with new data
            try:
                with open(file=wallets_file, mode="w") as f:
                    json.dump(wallets, f)
            except Exception as e:
                return Return(-1, 'Error', e.__str__())
            return Return(0, text=f"Wallet '{wallet_as_dictionary['name']}' saved")

    @staticmethod
    def add_wallet(wallet_as_dictionary):
        return Wallets.save_wallet(wallet_as_dictionary)

    @staticmethod
    def delete_wallet_by_name(wallet_name):
        try:
            with open(file=wallets_file, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        if wallet_name not in wallets['wallets']:
            return Return(-1, 'Warning', f"'{wallet_name}' not in 'wallets'.")
        del wallets['wallets'][wallet_name]
        # save file with new data
        try:
            with open(file=wallets_file, mode="w") as f:
                json.dump(wallets, f)
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        return Return(0, text=f"'{wallet_name}' wallet was deleted.")

    @staticmethod
    def dictionary_of_wallets():  # return array of wallets as dictionary
        try:
            with open(file=wallets_file, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Warning', e.__str__())
        return Return(wallets['wallets'])

    @staticmethod
    def is_wallet(wallet_as_dictionary):
        keys = ['name', 'market', 'key', 'sign', 'robots']
        for k in keys:
            if k not in wallet_as_dictionary.keys():
                return Return(False, 'Error', 'It is not wallet.')
        return Return(True)

    @staticmethod
    def get_set_of_used_markets():
        try:
            with open(file=wallets_file, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        set_of_markets = set()
        for (k, v) in wallets['wallets'].items():
            set_of_markets.add(v['market'])
        # sort list
        return Return(set(sorted(set_of_markets)))

    @staticmethod
    def get_list_of_wallets():
        try:
            with open(file=wallets_file, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        list_of_wallets = list()
        for k in wallets['wallets'].keys():
            list_of_wallets.append(k)
        # sort list
        return Return(sorted(list_of_wallets))

    @staticmethod
    def get_list_of_robot_names_by_wallet_name(wallet_name):  # return list of robot names
        try:
            with open(file=wallets_file, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return([], 'Error', e.__str__())
        if wallet_name not in wallets['wallets']:
            return Return([], 'Warning', f"'{wallet_name}' not in 'wallets'.")
        wallet = wallets['wallets'][wallet_name]
        robot_names = wallet['robots'].keys()
        return Return(list(robot_names))

    @staticmethod
    def add_parameter_value(parameter_name, parameter_value):  # save market_name in the list of supported markets
        try:
            with open(file=wallets_file, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception:  # not exist file
            wallets = {'wallets': {}, parameter_name: []}
        if parameter_name not in wallets.keys():
            wallets[parameter_name] = []
        # save elements in data
        if parameter_value not in wallets[parameter_name]:
            wallets[parameter_name].append(parameter_value)
        # save file with new data
        try:
            with open(file=wallets_file, mode="w") as f:
                json.dump(wallets, f)
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        return Return(0, text=f"'{parameter_value}' added to '{parameter_name}'")

    @staticmethod
    def delete_parameter_value(parameter_name, parameter_value):
        try:
            with open(file=wallets_file, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        if parameter_value not in wallets[parameter_name]:
            return Return(-1, 'Warning', f"'{parameter_value}' not in '{parameter_name}'.")
        wallets[parameter_name].remove(parameter_value)
        # save file with new data
        try:
            with open(file=wallets_file, mode="w") as f:
                json.dump(wallets, f)
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        return Return(0, text=f"'{parameter_value}' was deleted in '{parameter_name}'.")

    @staticmethod
    def value_range_of_parameter(parameter_name):
        try:
            with open(file=wallets_file, mode="r") as f:
                wallets = json.load(f)  # load entry as dictionary
        except Exception as e:
            return Return(-1, 'Error', e.__str__())
        parameter_set = set()
        for v in wallets[parameter_name]:
            parameter_set.add(v)
        # sort list
        return Return(set(sorted(parameter_set)))
