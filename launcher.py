import json
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QMovie, QPainter
from PyQt5.QtWidgets import QDialog, QMessageBox, QSlider

import battle


class Main(QDialog):
    """main window"""

    def __init__(self):
        super(Main, self).__init__()
        """simple pyqt setup"""
        uic.loadUi('./launcher.ui', self)
        # setting up fixed size for screen not to look ugly
        self.setFixedWidth(1200)
        self.setFixedHeight(900)
        # setting maximum and minimum of user level selection
        self.setlevel.setMinimum(0)
        self.setlevel.setMaximum(180)
        # this functions up there used to manage hardness of the game
        self.setlevel.setTickPosition(QSlider.TicksBelow)
        self.setlevel.setTickInterval(10)
        self.setlevel.valueChanged[int].connect(self.valuechange)
        self.editlevel.clicked.connect(self.changelevel)
        # this function is used to render text on the launcher
        self.remake()
        self.speedup.clicked.connect(lambda: self.multiupgrade('speed'))
        # connecting speed upgrade button to upgrade function
        self.bulletspeedup.clicked.connect(lambda: self.multiupgrade('bullet speed'))
        # connecting bullet speed upgrade button to upgrade function
        self.ratespeedup.clicked.connect(lambda: self.multiupgrade('fire rate'))
        # connecting fire rate button to upgrade function
        self.damageup.clicked.connect(lambda: self.multiupgrade('damage'))
        # connecting damage upgrade button to upgrade function
        self.ammoup.clicked.connect(lambda: self.multiupgrade('ammo'))
        # connecting hp upgrade button to upgrade function
        self.hpup.clicked.connect(lambda: self.multiupgrade('hp'))
        # connecting game start button to function that starts game
        self.start.clicked.connect(self.launch)
        # rendering beautiful launcher background
        self.movie = QMovie("laucher_background.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()
        self.show()

    def remake(self):
        """that's fields where we need to do setText
        and because money amount changes in the game we need to re-render this"""
        with open('data.json', 'r+') as file:  # opening user data
            self.data = json.load(file)
        # setting up progress bar to current difficulty
        if self.data['level'] == 'easy':
            self.setlevel.setValue(0)
        if self.data['level'] == 'medium':
            self.setlevel.setValue(90)
        if self.data['level'] == 'hard':
            self.setlevel.setValue(180)
        # setting up difficulty text
        self.level.setText('difficulty: ' + self.data['level'])
        # setting up all prices texts
        self.speedprice.setText('Price: ' + str(self.data['prices']['speed']))
        self.bulletspeedprice.setText('Price: ' + str(self.data['prices']['bullet speed']))
        self.rateupgradeprice.setText('Price: ' + str(self.data['prices']['fire rate']))
        self.coins.setText('Coins: ' + str(self.data['money']))
        self.hpprice.setText('Price: ' + str(self.data['prices']['hp']))
        self.ammoprice.setText('Price: ' + str(self.data['prices']['ammo']))
        self.dmgprice.setText('Price: ' + str(self.data['prices']['damage']))
        # remaking limits of level changer
        self.leveleditor.setMaximum(self.data['maxprogress'])
        self.leveleditor.setValue(self.data['progress'])

    def changelevel(self):
        """this is function that changes player's progress"""
        with open('data.json', 'r+') as file:
            data = json.load(file)
            data['progress'] = self.leveleditor.value()
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def valuechange(self, value):
        """that function sets difficulty of game, connected to horizontal progress bar"""
        with open('data.json', 'r+') as file:
            data = json.load(file)
            if value > 120:
                data['level'] = 'hard'
            elif value < 60:
                data['level'] = 'easy'
            else:
                data['level'] = 'medium'
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            # setting up difficulty text
            self.level.setText('difficulty: ' + data['level'])

    def paintEvent(self, event):
        """this function used to render a gif"""
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

    def multiupgrade(self, stat: str):
        try:
            with open('data.json', 'r+') as file:
                if self.data['money'] < self.data['prices'][stat]:
                    self.showalert('No money', 'You need more money to upgrade speed')
                    return
                if stat == 'fire rate':
                    self.data['upgrades'][stat] = self.data['upgrades'][stat] - 0.01
                else:
                    self.data['upgrades'][stat] = self.data['upgrades'][stat] + 1
                self.data['money'] = self.data['money'] - self.data['prices'][stat]
                self.data['prices'][stat] = self.data['prices'][stat] + 1
                file.seek(0)
                json.dump(self.data, file, indent=4)
                file.truncate()
            self.remake()  # need to remake to re-render the money and price
            # we can split this to functions but difficulty of this is really small and it doesn't make lags so we
            # left it like that
        except Exception as e:  # if something went wrong exception will be handled and printed
            # implemented cause pyqt can't normally say where is an error
            print(e)

    def showalert(self, title, message):
        """function that shows alert if something went wrong with upgrades"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

    def launch(self):
        """function that starts game"""
        self.hide()  # hides launcher
        battle.launchgame()  # starts game
        self.show()  # displays the launcher
        self.remake()  # remakes user stats( increases money displayed on screen and also level editor max value)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    app.exec_()
