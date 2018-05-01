from PyQt5 import QtWidgets, QtCore

import sharedData
from gui.widgets.twitterinformation import widgetsForTweets


class TwitterNews(QtWidgets.QWidget):

    def __init__(self, x, y, width, height, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._box = QtWidgets.QGroupBox('Tweets', self)
        self.setGeometryForMainBox()
        self._listOfTweets = widgetsForTweets.ListOfTweetWidgets(parent=self._box)
        self.setSlots()

    def setGeometryForMainBox(self):
        print("WidgetForTwitterNews: ", (self.x, self.y, self.width, self.height))
        geometry = QtCore.QRect(self.x,
                                self.y,
                                self.width,
                                self.height)
        self.setGeometry(geometry)

        geometry = QtCore.QRect(self.parent().shiftFromBorder,
                                self.parent().shiftFromBorder,
                                self.width - 2 * self.parent().shiftFromBorder,
                                self.height - 2 * self.parent().shiftFromBorder)
        self._box.setGeometry(geometry)

    def updateListOfTweets(self):
        self._listOfTweets.clear()
        tweets = sharedData.tweets.value
        for tweet in tweets:
            item = QtWidgets.QListWidgetItem(self._listOfTweets)
            tweetWidget = widgetsForTweets.TweetWidget(self._listOfTweets)
            tweetWidget.setTweet(tweet)
            item.setSizeHint(tweetWidget.minimumSizeHint())
            self._listOfTweets.addItem(item)
            self._listOfTweets.setItemWidget(item, tweetWidget)

    def setSlots(self):
        sharedData.tweets.changed.connect(self.updateListOfTweets)
