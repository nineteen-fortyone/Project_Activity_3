import sys
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QDesktopWidget
from PyQt5.QtWidgets import (QApplication, QPushButton, QLabel)
from PyQt5 import *
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *

import urllib.parse
import requests

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Map Quest"
        self.width = 1200
        self.height = 950

        self.main_api = "https://www.mapquestapi.com/directions/v2/route?"
        self.key = "EGU9NUedu933fZ58f7A4PahkQjArbjeu"

        self.initWindow()

    def initWindow(self):
        self.resize(self.width, self.height)
        self.setWindowTitle(self.title)

        self.center()
        self.labels()
        self.txtEdit()
        self.buttons()
        
        self.show()

    #move window to center
    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def labels(self):
        self.titleLabel = QLabel("Map Quest", self)
        self.titleLabel.setGeometry(QRect(460,50, 900, 100))
        self.titleLabel.setStyleSheet("QWidget { color: Black}")
        self.titleLabel.setFont(QtGui.QFont('Sanserif', 30, QtGui.QFont.Bold))

        self.startLocLabel = QLabel("Starting Location:", self)
        self.startLocLabel.setGeometry(QRect(150,200, 500, 100))
        self.startLocLabel.setStyleSheet("QWidget { color: Black}")
        self.startLocLabel.setFont(QtGui.QFont('Sanserif', 20, QtGui.QFont.Bold))

        self.destinationLabel = QLabel("Destination:", self)
        self.destinationLabel.setGeometry(QRect(150,200+100, 500, 100))
        self.destinationLabel.setStyleSheet("QWidget { color: Black}")
        self.destinationLabel.setFont(QtGui.QFont('Sanserif', 20, QtGui.QFont.Bold))

    def txtEdit(self):
        self.startLocEdit = QLineEdit(self)
        self.startLocEdit.setGeometry(QRect(150+320,210, 550, 75))
        self.startLocEdit.setStyleSheet("QWidget { color: Black}")
        self.startLocEdit.setFont(QtGui.QFont('Sanserif', 20, QtGui.QFont.Bold))

        self.destinationEdit = QLineEdit(self)
        self.destinationEdit.setGeometry(QRect(150+320,210+100, 550, 75))
        self.destinationEdit.setStyleSheet("QWidget { color: Black}")
        self.destinationEdit.setFont(QtGui.QFont('Sanserif', 20, QtGui.QFont.Bold))

    def buttons(self):
        self.submitButton = QPushButton('Submit', self)
        #self.submitButton.setIcon(QtGui.QIcon('Icons/plus.png'))
        self.submitButton.setGeometry(QRect(460+45,310+200, 200, 100))
        self.submitButton.setStyleSheet("QWidget { color: Black}")
        self.submitButton.setFont(QtGui.QFont('Sanserif', 20, QtGui.QFont.Bold))
        self.submitButton.clicked.connect(self.process)
        

        self.backButton = QPushButton('Back', self)
        #self.submitButton.setIcon(QtGui.QIcon('Icons/plus.png'))
        self.backButton.setGeometry(QRect(460+45,310+500, 200, 100))
        self.backButton.setStyleSheet("QWidget { color: Black}")
        self.backButton.setFont(QtGui.QFont('Sanserif', 20, QtGui.QFont.Bold))
        self.backButton.clicked.connect(self.backWindow)
        self.backButton.hide()

    def process(self):
        orig = self.startLocEdit.text()
        dest = self.destinationEdit.text()

        self.url = self.main_api + urllib.parse.urlencode({"key":self.key, "from":orig, "to":dest}) 

        self.json_data = requests.get(self.url).json()

        print("URL: " + (self.url))

        self.json_data = requests.get(self.url).json()
        self.json_status = self.json_data["info"]["statuscode"]

        self.resultLabel = QLabel("Result", self)
        self.resultLabel.setGeometry(QRect(460+80,50, 900, 100))
        self.resultLabel.setStyleSheet("QWidget { color: Black}")
        self.resultLabel.setFont(QtGui.QFont('Sanserif', 30, QtGui.QFont.Bold))
        
        self.resultTextEdit = QTextEdit(self)
        self.resultTextEdit.setReadOnly(True)
        self.resultTextEdit.setGeometry(QRect(100,100+50, 1000, 550))
        self.resultTextEdit.setStyleSheet("QWidget { color: Black}")
        self.resultTextEdit.setFont(QtGui.QFont('Sanserif', 10, QtGui.QFont.Bold))
        
        if self.json_status == 0:
            self.titleLabel.hide()
            self.startLocEdit.hide()
            self.startLocLabel.hide()
            self.destinationLabel.hide()
            self.destinationEdit.hide()
            self.submitButton.hide()

            self.resultLabel.show()
            self.resultTextEdit.show()
            self.backButton.show()

            self.resultTextEdit.append("API Status: " + str(self.json_status) + " = A successful route call.")
            self.resultTextEdit.append("=======================================================================")
            self.resultTextEdit.append("Directions from " + (orig) + " to " + (dest))
            self.resultTextEdit.append("Trip Duration:   " + (self.json_data["route"]["formattedTime"]))
            self.resultTextEdit.append("Miles:           " + str(self.json_data["route"]["distance"]))
            self.resultTextEdit.append("Fuel Used (Gal): " + str(self.json_data["route"]["fuelUsed"]))
            self.resultTextEdit.append("=======================================================================")
            self.resultTextEdit.append("Kilometers:      " + str("{:.2f}".format((self.json_data["route"]["distance"])*1.61)))
            self.resultTextEdit.append("Fuel Used (Ltr): " + str("{:.2f}".format((self.json_data["route"]["fuelUsed"])*3.78)))
            

            for each in self.json_data["route"]["legs"][0]["maneuvers"]:
                self.resultTextEdit.append((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
            self.resultTextEdit.append("=======================================================================")

        elif self.json_status == 402:
            self.titleLabel.hide()
            self.startLocEdit.hide()
            self.startLocLabel.hide()
            self.destinationLabel.hide()
            self.destinationEdit.hide()
            self.submitButton.hide()

            self.resultLabel.show()
            self.resultTextEdit.show()
            self.backButton.show()


            self.resultTextEdit.append("************************************************************************")
            self.resultTextEdit.append("Status Code: " + str(self.json_status) + "; Invalid user inputs for one or both locations.")
            self.resultTextEdit.append("************************************************************************")
        elif self.json_status == 611:
            self.titleLabel.hide()
            self.startLocEdit.hide()
            self.startLocLabel.hide()
            self.destinationLabel.hide()
            self.destinationEdit.hide()
            self.submitButton.hide()

            self.resultLabel.show()
            self.resultTextEdit.show()
            self.backButton.show()


            self.resultTextEdit.append("************************************************************************")
            self.resultTextEdit.append("Status Code: " + str(self.json_status) + "; Missing an entry for one or both locations.")
            self.resultTextEdit.append("************************************************************************")
        else:
            self.titleLabel.hide()
            self.startLocEdit.hide()
            self.startLocLabel.hide()
            self.destinationLabel.hide()
            self.destinationEdit.hide()
            self.submitButton.hide()

            self.resultLabel.show()
            self.resultTextEdit.show()
            self.backButton.show()

            self.resultTextEdit.append("************************************************************************")
            self.resultTextEdit.append("For Staus Code: " + str(self.json_status) + "; Refer to:")
            self.resultTextEdit.append("https://developer.mapquest.com/documentation/directions-api/status-codes")
            self.resultTextEdit.append("************************************************************************\n")

    def backWindow(self):
        self.titleLabel.show()
        self.startLocEdit.show()
        self.startLocEdit.setText("")

        self.startLocLabel.show()
        self.destinationLabel.show()
        self.destinationEdit.show()
        self.destinationEdit.setText("")
        
        self.submitButton.show()

        self.resultLabel.hide()
        self.resultTextEdit.hide()
        self.resultTextEdit.setText("")

        self.backButton.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())

