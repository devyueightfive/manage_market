import os

pathToCurrentDirectory = os.path.abspath(os.curdir)
pathToData = os.path.join(pathToCurrentDirectory, "data")
pathToJson = os.path.join(pathToData, "json")
pathToImg = os.path.join(pathToData, "img")

pathToTradesFile = os.path.join(pathToData, 'trades.h5')

pathToWalletsFile = os.path.join(pathToJson, "wallets.json")
pathToBalanceFile = os.path.join(pathToJson, "balance.json")
pathToActiveOrdersFile = os.path.join(pathToJson, "active_orders.json")
pathToTwitterAccounts = os.path.join(pathToJson, "twitterScreenNames.json")

pathToTwitterImage = os.path.join(pathToImg, "twitter-logo.jpg")
