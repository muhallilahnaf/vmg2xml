# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
# Created by: PyQt5 UI code generator 5.15.9


from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
import os
import re
import chardet
from datetime import datetime
from urllib.parse import unquote


class Ui_MainWindow(object):
    # setup the ui
    def setupUi(self, MainWindow):
        # geometry vars
        self.width = 500
        self.height = 200
        self.outerMargin = 15
        self.innerWidth = self.width - 2 * (self.outerMargin)
        self.innerHeight = self.height - 2 * (self.outerMargin)
        self.menuHeight = 23
        self.verticalSpacing = 5
        self.countryCode = "+88"
        self.folder = ""
        self.output = ""
        self.xml = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n"
        self.sms = ""

        # main window
        self.MainWindow = MainWindow
        self.MainWindow.setFixedSize(self.width, self.height)
        self.MainWindow.setWindowTitle("vmg2xml")
        self.MainWindow.setWindowIcon(QtGui.QIcon("vmg2xml.ico"))

        # central parent widget
        self.centralWidget = QtWidgets.QWidget()

        # grid layout widget
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.gridLayoutWidget.setGeometry(
            QtCore.QRect(
                self.outerMargin,
                self.outerMargin,
                self.innerWidth,
                self.innerHeight - self.menuHeight,
            )
        )

        # grid layout
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(self.verticalSpacing)

        # add the components
        self.createMenuBar()
        self.createFolderButton()
        self.createCountryCode()
        self.createStartButton()

        # add central widget
        self.MainWindow.setCentralWidget(self.centralWidget)

        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    # create folder button
    def createFolderButton(self):
        self.buttonFolder = QtWidgets.QPushButton("Select Folder")
        self.buttonFolder.clicked.connect(self.folderClicked)
        self.gridLayout.addWidget(self.buttonFolder, 0, 0, 1, 1)

    # create countryCode component
    def createCountryCode(self):
        labelCountryCode = QtWidgets.QLabel("Country Code")
        self.gridLayout.addWidget(labelCountryCode, 1, 0, 1, 1)
        # input
        self.lineEditCountryCode = QtWidgets.QLineEdit()
        self.gridLayout.addWidget(self.lineEditCountryCode, 1, 1, 1, 1)
        # help text
        labelCountryCodeHelp = QtWidgets.QLabel("E.g. +88")
        labelCountryCodeHelp.setStyleSheet("color: #505050")
        self.gridLayout.addWidget(labelCountryCodeHelp, 1, 2, 1, 1)

    # create start button
    def createStartButton(self):
        self.buttonStart = QtWidgets.QPushButton("Start")
        self.buttonStart.clicked.connect(self.startClicked)
        self.gridLayout.addWidget(self.buttonStart, 2, 1, 1, 1)

    # create menu bar
    def createMenuBar(self):
        # menu bar
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.width, self.menuHeight))
        # about menu
        self.menuAbout = QtWidgets.QMenu("About")
        self.githubAction = QtWidgets.QAction(self.MainWindow)
        self.githubAction.triggered.connect(self.openGithub)
        self.githubAction.setText(
            QtCore.QCoreApplication.translate("MainWindow", "Github")
        )
        self.githubAction.setShortcut(
            QtCore.QCoreApplication.translate("MainWindow", "Ctrl+G")
        )
        self.menuAbout.addAction(self.githubAction)
        self.menubar.addMenu(self.menuAbout)
        # add menu bar
        self.MainWindow.setMenuBar(self.menubar)

    def openGithub(self):
        url = QtCore.QUrl("https://github.com/muhallilahnaf/vmg2xml")
        QtGui.QDesktopServices.openUrl(url)

    # folder button on click callback
    def folderClicked(self):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.folder = QtWidgets.QFileDialog.getExistingDirectory(
            self.MainWindow,
            "Select Folder",
            desktop,
            QtWidgets.QFileDialog.ShowDirsOnly,
        )
        labelFolder = QtWidgets.QLabel(self.folder)
        self.gridLayout.addWidget(labelFolder, 0, 1, 1, 3)

    # start button on click callback
    def startClicked(self):
        okay = self.checkCountryCode()
        if not okay:
            return
        okay = self.checkFolder()
        if not okay:
            return
        self.start()

    # check country code input
    def checkCountryCode(self):
        self.countryCode = self.lineEditCountryCode.text().strip()
        if self.countryCode == "":
            self.showMessage("Error", "Country code required.")
            return False
        match = re.search(r"\+\d+", self.countryCode)
        if not match:
            self.showMessage("Error", "Invalid country code.")
            return False
        return True

    # show message prompt
    def showMessage(self, title, msg):
        msgBox = QtWidgets.QMessageBox(self.MainWindow)
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        buttonClicked = msgBox.exec_()

    # check selected folder
    def checkFolder(self):
        if self.folder == "":
            self.showMessage("Error", "Select a folder containing the vmg files.")
            return False
        return True

    # start process
    def start(self):
        self.buttonStart.setEnabled(False)
        self.convert()
        self.save()
        self.buttonStart.setEnabled(True)

    # vmg -> xml conversion
    def convert(self):

        count = 0
        for file in os.listdir(self.folder):
            if file.lower().endswith(".vmg"):

                # calculate message count
                count = count + 1

                fname = os.path.join(self.folder, file)

                # default encoding
                encoding = "utf-8"
                with open(fname, "rb") as f:
                    content = f.read()
                    encoding = chardet.detect(content).get("encoding")  # guess encoding

                # open with guessed encoding
                with open(fname, "r", encoding=encoding) as f:

                    # assuming vmg file names are in the format: date_contactname.vmg
                    [timestamp, contact] = file.split("_")

                    # unix timestamp from date
                    timestamp = int(
                        datetime.strptime(timestamp, "%Y%m%d%H%M%S").timestamp()
                    )

                    # if contact not saved in phonebook, contact=(Unknown)
                    contact = re.sub(".vmg", "", contact, flags=re.IGNORECASE)
                    if contact.startswith(self.countryCode):
                        contact = "(Unknown)"

                    content = f.read()

                    # read status
                    read = 0
                    match = re.search(r"X-IRMC-STATUS.+\n", content)
                    if match:
                        readText = match.group()
                        readText = readText.replace("X-IRMC-STATUS:", "").strip()
                        if readText == "READ":
                            read = 0
                        if readText == "UNREAD":
                            read = 1

                    # message type
                    msgtype = 1
                    match = re.search(r"X-MESSAGE-TYPE.+\n", content)
                    if match:
                        typeText = match.group()
                        typeText = typeText.replace("X-MESSAGE-TYPE:", "").strip()
                        if typeText == "DELIVER":
                            msgtype = 1
                        if typeText == "SUBMIT":
                            msgtype = 2

                    # contact number
                    number = ""
                    match = re.search(r"CELL.+\n", content)
                    if match:
                        number = match.group()
                        number = number.replace("CELL:", "").strip()
                    if number == "":
                        match = re.search(r"TEL.+\n", content)
                        if match:
                            number = match.group()
                            number = number.replace("TEL:", "").strip()

                    # date convert from {16.03.2024 16:15:17} to {16 Mar 2024 4:15:17 pm}
                    date = ""
                    match = re.search(r"VBODY\nDate:.+\n", content)
                    if match:
                        date = match.group()
                        date = date.replace("VBODY\nDate:", "").strip()
                        date_part, time_part = date.split(" ")
                        date_obj = datetime.strptime(date_part, "%d.%m.%Y")
                        formatted_date = date_obj.strftime("%d %b %Y")
                        time_with_meridiem = f"{time_part} {'pm' if int(time_part.split(':')[0]) >= 12 else 'am'}"
                        date = f"{formatted_date} {time_with_meridiem}"

                    # message body
                    body = ""
                    match = re.search(
                        r"TEXT;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:[\S\s]+END:VBODY",
                        content,
                    )
                    if match:
                        body = match.group()
                        body = (
                            body.replace(
                                "TEXT;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:", ""
                            )
                            .replace("END:VBODY", "")
                            .replace("=\n", "")
                            .replace("=0A", "\n")
                            .strip()
                        )
                        # for text other than english
                        # if body.startswith("="):
                        #     body = body.replace("=", "%")
                        #     body = unquote(body)

                    line = f'<sms protocol="0" address="{number}" date="{timestamp}" type="{msgtype}" subject="null" body="{body}" toa="null" sc_toa="null" service_center="null" read="{read}" status="-1" locked="0" date_sent="{timestamp}" sub_id="-1" readable_date="{date}" contact_name="{contact}" />\n'

                    self.sms = self.sms + line

        self.xml = (
            self.xml
            + f'<smses count="{count}" backup_set="3ff83320-2c57-44c2-bdd5-7eae6758fcef" backup_date="1711616976109" type="full">\n'
            + self.sms
            + "</smses>"
        )

    # save xml file
    def save(self):
        folder = os.path.join(os.path.expanduser("~"), "Desktop")
        fname = QtWidgets.QFileDialog().getSaveFileName(
            self.MainWindow, "Save File", folder, "XML Files (*.xml)"
        )[0]
        if fname == "":
            return False
        with open(fname, "w", encoding="utf-8") as f:
            f.write(self.xml)
        self.showMessage("Saved", f"Output saved in file:\n{fname}")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
