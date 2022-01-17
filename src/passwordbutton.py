'''
Class for the password button that show what applications/websites have
currently saved passwords.
'''

from PyQt5.QtWidgets import QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from os import remove
from os.path import join
from pyperclip import copy
from codecs import decode


class PasswordButton(QPushButton):
    def __init__(self, text, password, parent, **kwargs):
        super().__init__()

        passBtnStyle = """QPushButton {
            background-color: #333333;
            border-left: 0px solid black;
            border-right: 0px solid black;
            border-bottom: 1px solid #555555;
            border-top: 0px solid #555555;
            color: white;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #444444;
        }
        QPushButton:pressed {
            background-color: #404040;
        }
        """

        self.setText(text)
        self.password = password
        self.setFont(QFont("Arial", 18))
        self.setShortcut('Ctrl-N')
        self.setStyleSheet(passBtnStyle)
        self.clicked.connect(self.loadPassword)
        self.parent = parent
        self.contextMenu = None

    def loadPassword(self, **kwargs):
        '''
        Gets the encrypted password that corresponds to the website/application
        and copies the decrypted password to the clipboard
        '''
        filename = self.text()
        if (filename == "File not found" or
            filename == "Copied to clipboard" or
                filename == "Incorrect login password. Unable to decode"):
            return
        try:
            with open(join('PassManData', filename), 'rb') as file:
                data = file.read()
            nonce, salt, data = data[:16], data[16:32], data[32:]

            derivedKey = PBKDF2(
                self.password,
                salt,
                dkLen=32
            )
            cipher = AES.new(derivedKey, AES.MODE_EAX, nonce)
            decrypted = cipher.decrypt(data)
            copy(decode(decrypted, 'CP1252'))
            self.setText('Copied to clipboard')
            QTimer.singleShot(2000, lambda: self.setText(filename))
        except FileNotFoundError:
            self.setText('File not found')
            QTimer.singleShot(2000, lambda: self.setText(filename))
        except UnicodeDecodeError:
            self.setText('Incorrect login password. Unable to decode')
            QTimer.singleShot(2000, lambda: self.setText(filename))

    def onContextMenu(self, point):
        '''
        Handles right clicks
        '''
        self.contextMenu.exec(self.mapToGlobal(point))

    def remove(self, **kwargs):
        '''
        Handles removing the password corresponding to the buttons
        website/application
        '''
        filename = self.text()
        if (filename == "File not found" or
            filename == "Copied to clipboard" or
                filename == "Incorrect login password. Unable to decode"):
            return
        msg = QMessageBox()
        msg.setText("Are you sure that you want to delete this password file?")
        msg.setInformativeText("This action cannot be undone")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        ret = msg.exec()

        if ret == QMessageBox.Ok:
            self.parent.files.remove(filename)
            remove(join('PassManData', filename))
            self.parent.updateButtons()
