# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lmslogin.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName(_fromUtf8("Login"))
        Login.resize(321, 218)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("img/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Login.setWindowIcon(icon)
        Login.setStyleSheet(_fromUtf8(""))
        self.login_username = QtGui.QLineEdit(Login)
        self.login_username.setGeometry(QtCore.QRect(10, 30, 301, 51))
        self.login_username.setObjectName(_fromUtf8("login_username"))
        self.login_password = QtGui.QLineEdit(Login)
        self.login_password.setGeometry(QtCore.QRect(10, 90, 301, 51))
        self.login_password.setEchoMode(QtGui.QLineEdit.Password)
        self.login_password.setObjectName(_fromUtf8("login_password"))
        self.login_btn = QtGui.QPushButton(Login)
        self.login_btn.setGeometry(QtCore.QRect(10, 150, 111, 51))
        self.login_btn.setAutoDefault(True)
        self.login_btn.setObjectName(_fromUtf8("login_btn"))
        self.label = QtGui.QLabel(Login)
        self.label.setGeometry(QtCore.QRect(80, 0, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.login_error = QtGui.QLabel(Login)
        self.login_error.setGeometry(QtCore.QRect(140, 160, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.login_error.setFont(font)
        self.login_error.setStyleSheet(_fromUtf8("QLabel {\n"
"color:rgb(255, 0, 0);\n"
"}"))
        self.login_error.setText(_fromUtf8(""))
        self.login_error.setTextFormat(QtCore.Qt.RichText)
        self.login_error.setObjectName(_fromUtf8("login_error"))

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        Login.setWindowTitle(_translate("Login", "MeX LMS - Login", None))
        self.login_username.setPlaceholderText(_translate("Login", "username", None))
        self.login_password.setPlaceholderText(_translate("Login", "password", None))
        self.login_btn.setText(_translate("Login", "Login", None))
        self.label.setText(_translate("Login", "Admin Login", None))

