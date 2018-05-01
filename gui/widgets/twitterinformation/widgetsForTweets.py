import math

from PyQt5 import QtWidgets, QtCore

import settings


class TweetsModel(object):
    def __init__(self, listOfTweets: list):
        self._listOfTweets = listOfTweets

    def height(self):
        return len(self._listOfTweets)

    def listOfTweets(self):
        return self._listOfTweets


class ListOfTweetsModel(QtCore.QAbstractListModel):
    def __init__(self, tweetsModel: TweetsModel):
        super().__init__(parent=None)
        self._tweets = tweetsModel

    def setTweets(self, tweetsModel: TweetsModel):
        self._tweets = tweetsModel
        self.modelReset()

    def rowCount(self, parent=None, *args, **kwargs):
        return self._tweets.height()

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def data(self, QModelIndex, role=None):
        if role == QtCore.Qt.DisplayRole:
            return self._tweets.listOfTweets()[QModelIndex.row()].get('screen_name', "Hello!")


class TweetWidget(QtWidgets.QWidget):
    shiftFromBorders = 22
    height = 120

    def __init__(self, parent=None, **params):
        super().__init__(parent, **params)
        self._labelForTweet = QtWidgets.QTextEdit(self)
        self._labelForTweet.move(0, 0)

    def setTweet(self, tweet: dict):
        # self._labelForTweet.setTextFormat(QtCore.Qt.RichText)
        self._labelForTweet.setStyleSheet(
            "background-color:white;border-radius:10px;border: 1px solid gray;padding: 2 4px;")
        text = tweet.get('text', "")
        self.height = (math.ceil(len(text) / 34) + 2) * 15 + 50
        name = tweet.get('screen_name', "")
        source = settings.pathToTwitterImage
        url = tweet.get('url', "")
        timeCreatedAt = tweet.get('created_at', "")
        text = f'<span>' \
               f'<a href = "{url}">' \
               f'<img src = "{source}" height = "20" width = "20"></img>' \
               f'<span style= "color:blue">@{name}</span>' \
               f'</a>' \
               f'<p style = "background-color:white;color:black;text-align:left;">{text}</p>' \
               f'<p style = "text-align:right;">{timeCreatedAt}</p>' \
               f'</span>'
        pass
        self._labelForTweet.setText(text)
        self._labelForTweet.resize(self.parent().geometry().width() - self.shiftFromBorders,
                                   self.height)
        self.adjustSize()

    def minimumSizeHint(self):
        return QtCore.QSize(self.geometry().width(),
                            self.geometry().height())


class ListOfTweetWidgets(QtWidgets.QListWidget):
    shiftFromTop = 18
    shiftFromBorders = 3

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.height = parent.geometry().height()
        self.width = parent.geometry().width()
        self.setGeometryOptions()

    def setGeometryOptions(self):
        geometry = QtCore.QRect(self.shiftFromBorders,
                                self.shiftFromTop,
                                self.width - 2 * self.shiftFromBorders,
                                self.height - self.shiftFromTop)
        self.setGeometry(geometry)
        print(f"ListOfTweetsWidget : {geometry}")
        self.setStyleSheet("background-color: #F1F1F1;")
