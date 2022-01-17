'''
Main class for the program.
'''

from sys import argv
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QApplication, QPushButton, QFrame, QSystemTrayIcon, QMenu)
from PyQt5.QtGui import QFont, QKeySequence, QIcon
from PyQt5.QtCore import Qt, QEvent, QRect
from PyQt5 import QtCore
from os import makedirs, listdir
from os.path import exists as dirExists
from os.path import join, isfile
from login import LoginScreen
from newpass import NewPasswordScreen
from addpass import AddPasswordScreen
from passwordbutton import PasswordButton


class MainScreen(QWidget):
    def __init__(self, password):
        super().__init__()
        self.password = password
        self.lastGenerated = None
        self.minimized = False
        self.scrollPos = 0
        self.entriesPerPage = 10  # changed
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        # System Tray
        icon = QIcon('icon.png')

        menu = QMenu()
        exitAct = menu.addAction("Exit")
        exitAct.triggered.connect(lambda x: self.close())

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.activated.connect(self.maximize)
        self.tray.setContextMenu(menu)
        self.tray.show()

        # Buttons
        newPassBtn = QPushButton("New Entry")
        newPassBtn.setFont(QFont("Arial", 20))
        newPassBtn.setShortcut('Ctrl-N')
        newPassBtn.clicked.connect(self.addPassword)
        newPassBtn.setShortcut(QKeySequence('Ctrl+n'))
        newPassBtn.setFocusPolicy(Qt.NoFocus)
        newPassBtn.setStyleSheet(""" QPushButton {
            background-color: #333333;
            border: 2px groove #555555;
            color: white;
            padding: px;
        }
        QPushButton:hover {
            background-color: #444444;
        }
        QPushButton:pressed {
            background-color: #404040;
        }
        """)
        layout.addWidget(newPassBtn, 0, 1)

        line = QFrame()
        line.setGeometry(QRect(320, 150, 118, 3))
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line, 1, 0, 1, 3)

        # Buttons
        self.buttons = []
        self.files = [x for x in listdir('PassManData') if (isfile(
            join('PassManData', x)) and x != 'savedpassword')]

        for x in range(self.entriesPerPage):
            self.buttons.append(PasswordButton(str(x), password, self))
            self.buttons[-1].setFocusPolicy(Qt.NoFocus)

            self.buttons[-1].contextMenu = QMenu()
            deleteAct = self.buttons[-1].contextMenu.addAction('Delete')
            deleteAct.triggered.connect(self.buttons[-1].remove)
            self.buttons[-1].setContextMenuPolicy(Qt.CustomContextMenu)
            self.buttons[-1].customContextMenuRequested.connect(
                self.buttons[-1].onContextMenu)

            layout.addWidget(self.buttons[-1], x + 2, 1, 1, 1)

        self.updateButtons()

        line1 = QFrame()
        line1.setGeometry(QRect(320, 150, 118, 3))
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line1, self.entriesPerPage + 2, 1, 1, 1)

        # Layout setup
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(5)  # changed
        layout.setContentsMargins(0, 20, 0, 0)
        self.setStyleSheet("""
                background-color: #777777;
        """
                           )
        self.setLayout(layout)
        self.resize(700, 500)  # changed
        self.setMinimumSize(QtCore.QSize(700, 500))  # changed
        self.setMaximumSize(QtCore.QSize(700, 500))
        self.setWindowTitle("Zookeeper")
        self.setWindowIcon(icon)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()

    def addPassword(self, **kwargs):
        '''
        Opens the add password screen
        '''
        addPass = AddPasswordScreen(self)
        addPass.show()

        '''
        TODO: Use this to allow a user to copy the last generated password,
        even if they forgot to save it
        '''
        if addPass.password is not None:
            self.lastGenerated = addPass.password

    def updateButtons(self):
        '''
        Updates the buttons that display the current website/applications that
        have passwords currently saved
        '''
        for i in range(len(self.buttons)):
            if i + self.scrollPos >= len(self.files):
                self.buttons[i].setVisible(False)
                continue
            self.buttons[i].setText(self.files[i + self.scrollPos])
            self.buttons[i].setVisible(True)

    def maximize(self, **kwargs):
        '''
        Maximizes the window
        '''
        self.setVisible(True)
        self.showNormal()

    def closeEvent(self, event):
        '''
        Removes the icon from the tray before the window closes
        '''
        self.tray.setVisible(False)
        event.accept()

    def wheelEvent(self, event):
        '''
        Handles mouse wheel events in order to allow scrolling through passwords
        '''
        steps = round(event.angleDelta().y() / 120) * -1
        if steps > 0:
            for _ in range(steps):
                if self.scrollPos + self.entriesPerPage < len(self.files):
                    self.scrollPos += 1
            self.updateButtons()
        else:
            for _ in range(0, steps, -1):
                if self.scrollPos > 0:
                    self.scrollPos -= 1
            self.updateButtons()

    def event(self, event):
        '''
        Handles both key input and the window minimizing, or passes the event
        to the default event handler if it's not one of those
        '''
        if (event.type() == QEvent.KeyPress):
            # Down arrow
            if event.key() == 16777237:
                if self.scrollPos + self.entriesPerPage < len(self.files):
                    self.scrollPos += 1
                    self.updateButtons()
                return True

            # Up arrow
            elif event.key() == 16777235:
                if self.scrollPos > 0:
                    self.scrollPos -= 1
                    self.updateButtons()
                return True
            else:
                return QWidget.event(self, event)

        elif (event.type() == QEvent.WindowStateChange) and self.isMinimized():
            event.ignore()
            self.setVisible(False)
            return True

        else:
            return QWidget.event(self, event)


if __name__ == '__main__':
    app = QApplication(argv)

    # Checks to be sure that there is a folder for passwords in appdata
    if not dirExists('PassManData'):
        makedirs('PassManData')

    # Attemps to find the master password hash and open the login window
    Login = None
    try:
        open(join('PassManData', 'savedpassword'), 'rb').close()

        login = LoginScreen()
    except FileNotFoundError:
        login = NewPasswordScreen()

    app.exec()

    password = login.password

    main = MainScreen(password)
    app.exec()
