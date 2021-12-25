import PyQt5
import json
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtWidgets, uic
import sys
import battle


class Main(QDialog):
    """main window"""

    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('./launcher.ui', self)
        self.show()
        with open('data.json', 'r+') as file:
            self.data = json.load(file)
        self.speedprice.setText('Price: ' + str(self.data['prices']['speed']))
        self.speedup.clicked.connect(self.upgradespeed)
        self.bulletspeedprice.setText('Price: ' + str(self.data['prices']['bullet speed']))
        self.bulletspeedup.clicked.connect(self.upgradebulletspeed)
        self.rateupgradeprice.setText('Price: ' + str(self.data['prices']['fire rate']))
        self.ratespeedup.clicked.connect(self.upgradespeedrate)
        self.start.clicked.connect(self.launch)

    def upgradespeed(self):
        with open('data.json', 'r+') as file:
            if self.data['money'] < self.data['prices']['speed']:
                self.showalert('No money', 'You need more money to upgrade speed')
                return
            self.data['upgrades']['speed'] = self.data['upgrades']['speed'] + 10
            self.data['money'] = self.data['money'] - self.data['prices']['speed']
            self.data['prices']['speed'] = self.data['prices']['speed'] + 1
            file.seek(0)
            json.dump(self.data, file, indent=4)
            file.truncate()
        self.speedprice.setText('Price: ' + str(self.data['prices']['speed']))

    def upgradebulletspeed(self):
        with open('data.json', 'r+') as file:
            if self.data['money'] < self.data['prices']['bullet speed']:
                self.showalert('No money', 'You need more money to upgrade bullet speed')
                return
            self.data['upgrades']['bullet speed'] = self.data['upgrades']['bullet speed'] + 100
            self.data['money'] = self.data['money'] - self.data['prices']['bullet speed']
            self.data['prices']['bullet speed'] = self.data['prices']['bullet speed'] + 1
            file.seek(0)
            json.dump(self.data, file, indent=4)
            file.truncate()
        self.bulletspeedprice.setText('Price: ' + str(self.data['prices']['bullet speed']))

    def upgradespeedrate(self):
        with open('data.json', 'r+') as file:
            if self.data['money'] < self.data['prices']['fire rate']:
                self.showalert('No money', 'You need more money to upgrade fire rate')
                return
            if self.data['upgrades']['fire rate'] <= 0.1:
                self.showalert('Already fully upgraded', 'Upgrade something else')
                return
            self.data['upgrades']['fire rate'] = self.data['upgrades']['fire rate'] - 0.01
            self.data['money'] = self.data['money'] - self.data['prices']['fire rate']
            self.data['prices']['fire rate'] = self.data['prices']['fire rate'] + 1
            file.seek(0)
            json.dump(self.data, file, indent=4)
            file.truncate()
        self.rateupgradeprice.setText('Price: ' + str(self.data['prices']['speed rate']))

    def showalert(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

    def launch(self):
        self.close()
        battle.launchgame()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    app.exec_()
