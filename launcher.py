import json
import sys

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QMovie, QPainter
from PyQt5.QtWidgets import QDialog, QMessageBox, QSlider
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout,
                             QGroupBox, QMenu, QPushButton,
                             QRadioButton, QVBoxLayout,
                             QWidget, QSlider, QLabel)

import battle
import game_over


class Main(QDialog):
    """main window"""

    def __init__(self):
        super(Main, self).__init__()
        """simple pyqt setup"""
        uic.loadUi('./launcher.ui', self)
        self.remake()
        self.speedup.clicked.connect(lambda: self.multiupgrade('speed', self.speedprice))
        self.bulletspeedup.clicked.connect(lambda: self.multiupgrade('bullet speed', self.bulletspeedprice))
        self.ratespeedup.clicked.connect(lambda: self.multiupgrade('fire rate', self.rateupgradeprice))
        self.damageup.clicked.connect(lambda: self.multiupgrade('damage', self.dmgprice))
        self.ammoup.clicked.connect(lambda: self.multiupgrade('ammo', self.ammoprice))
        self.hpup.clicked.connect(lambda: self.multiupgrade('hp', self.hpprice))
        self.start.clicked.connect(self.launch)
        self.movie = QMovie("laucher_background.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()
        self.setlevel.setMinimum(0)
        self.setlevel.setMaximum(180)
        self.setlevel.setValue(0)
        self.setlevel.setTickPosition(QSlider.TicksBelow)
        self.setlevel.setTickInterval(10)
        self.setlevel.valueChanged[int].connect(self.valuechange)
        self.editlevel.clicked.connect(self.changelevel)
        self.show()

    def remake(self):
        """that's fields where we need to do setText and because money amount changes in the game we need to re-render this"""
        with open('data.json', 'r+') as file:
            self.data = json.load(file)
        self.level.setText('difficulty: ' + self.data['level'])
        self.speedprice.setText('Price: ' + str(self.data['prices']['speed']))
        self.bulletspeedprice.setText('Price: ' + str(self.data['prices']['bullet speed']))
        self.rateupgradeprice.setText('Price: ' + str(self.data['prices']['fire rate']))
        self.coins.setText('Coins: ' + str(self.data['money']))
        self.hpprice.setText('Price: ' + str(self.data['prices']['hp']))
        self.ammoprice.setText('Price: ' + str(self.data['prices']['ammo']))
        self.dmgprice.setText('Price: ' + str(self.data['prices']['damage']))
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
        """that function sets difficulty of game"""
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
            self.level.setText('difficulty: ' + data['level'])

    def paintEvent(self, event):
        """this function used to render a gif"""
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)



    def multiupgrade(self, stat: str, text_field):
        try:
            with open('data.json', 'r+') as file:
                if self.data['money'] < self.data['prices'][stat]:
                    self.showalert('No money', 'You need more money to upgrade speed')
                    return
                self.data['upgrades'][stat] = self.data['upgrades'][stat] + 1
                self.data['money'] = self.data['money'] - self.data['prices'][stat]
                self.data['prices'][stat] = self.data['prices'][stat] + 1
                file.seek(0)
                json.dump(self.data, file, indent=4)
                file.truncate()
            text_field.setText('Price: ' + str(self.data['prices'][stat]))
        except Exception as e:
            print(e)

    """
        All functions down there are used to change specific states on the screen and edit data 
        in data.json. we decided to split these functions to make everyone understand how this works
        They're commented because if in future they well become more complex, it will be easier to work with dummy functions like that
    """

    # def upgradespeed(self):
    #     with open('data.json', 'r+') as file:
    #         if self.data['money'] < self.data['prices']['speed']:
    #             self.showalert('No money', 'You need more money to upgrade speed')
    #             return
    #         self.data['upgrades']['speed'] = self.data['upgrades']['speed'] + 1
    #         self.data['money'] = self.data['money'] - self.data['prices']['speed']
    #         self.data['prices']['speed'] = self.data['prices']['speed'] + 1
    #         file.seek(0)
    #         json.dump(self.data, file, indent=4)
    #         file.truncate()
    #     self.speedprice.setText('Price: ' + str(self.data['prices']['speed']))
    #
    # def upgradehp(self):
    #     with open('data.json', 'r+') as file:
    #         if self.data['money'] < self.data['prices']['hp']:
    #             self.showalert('No money', 'You need more money to upgrade speed')
    #             return
    #         self.data['upgrades']['hp'] = self.data['upgrades']['hp'] + 1
    #         self.data['money'] = self.data['money'] - self.data['prices']['hp']
    #         self.data['prices']['hp'] = self.data['prices']['hp'] + 1
    #         file.seek(0)
    #         json.dump(self.data, file, indent=4)
    #         file.truncate()
    #     self.hpprice.setText('Price: ' + str(self.data['prices']['hp']))
    #     self.remake()
    #
    # def upgradebulletspeed(self):
    #     with open('data.json', 'r+') as file:
    #         if self.data['money'] < self.data['prices']['bullet speed']:
    #             self.showalert('No money', 'You need more money to upgrade bullet speed')
    #             return
    #         self.data['upgrades']['bullet speed'] = self.data['upgrades']['bullet speed'] + 100
    #         self.data['money'] = self.data['money'] - self.data['prices']['bullet speed']
    #         self.data['prices']['bullet speed'] = self.data['prices']['bullet speed'] + 1
    #         file.seek(0)
    #         json.dump(self.data, file, indent=4)
    #         file.truncate()
    #     self.bulletspeedprice.setText('Price: ' + str(self.data['prices']['bullet speed']))
    #     self.remake()
    #
    # def upgradefirerate(self):
    #     with open('data.json', 'r+') as file:
    #         if self.data['money'] < self.data['prices']['fire rate']:
    #             self.showalert('No money', 'You need more money to upgrade fire rate')
    #             return
    #         if self.data['upgrades']['fire rate'] <= 0.1:
    #             self.showalert('Already fully upgraded', 'Upgrade something else')
    #             return
    #         self.data['upgrades']['fire rate'] = self.data['upgrades']['fire rate'] - 0.01
    #         self.data['money'] = self.data['money'] - self.data['prices']['fire rate']
    #         self.data['prices']['fire rate'] = self.data['prices']['fire rate'] + 1
    #         file.seek(0)
    #         json.dump(self.data, file, indent=4)
    #         file.truncate()
    #     self.rateupgradeprice.setText('Price: ' + str(self.data['prices']['fire rate']))
    #     self.remake()
    #
    # def upgradeammo(self):
    #     with open('data.json', 'r+') as file:
    #         if self.data['money'] < self.data['prices']['ammo']:
    #             self.showalert('No money', 'You need more money to upgrade speed')
    #             return
    #         self.data['upgrades']['ammo'] = self.data['upgrades']['ammo'] + 5
    #         self.data['money'] = self.data['money'] - self.data['prices']['ammo']
    #         self.data['prices']['ammo'] = self.data['prices']['ammo'] + 1
    #         file.seek(0)
    #         json.dump(self.data, file, indent=4)
    #         file.truncate()
    #     self.ammoprice.setText('Price: ' + str(self.data['prices']['ammo']))
    #     self.remake()
    #
    # def updragedmg(self):
    #     with open('data.json', 'r+') as file:
    #         if self.data['money'] < self.data['prices']['damage']:
    #             self.showalert('No money', 'You need more money to upgrade speed')
    #             return
    #         self.data['upgrades']['damage'] = self.data['upgrades']['damage'] + 5
    #         self.data['money'] = self.data['money'] - self.data['prices']['damage']
    #         self.data['prices']['damage'] = self.data['prices']['damage'] + 1
    #         file.seek(0)
    #         json.dump(self.data, file, indent=4)
    #         file.truncate()
    #     self.dmgprice.setText('Price: ' + str(self.data['prices']['damage']))
    #     self.remake()

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
        self.hide()
        battle.launchgame()
        self.show()
        self.remake()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    app.exec_()
