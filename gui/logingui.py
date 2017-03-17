# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logingui.ui'
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
        Login.resize(344, 223)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Login.setWindowIcon(icon)
        Login.setStyleSheet(_fromUtf8(""))
        self.label_6 = QtGui.QLabel(Login)
        self.label_6.setGeometry(QtCore.QRect(90, 10, 151, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_6.setFrameShadow(QtGui.QFrame.Plain)
        self.label_6.setLineWidth(1)
        self.label_6.setMidLineWidth(0)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.layoutWidget = QtGui.QWidget(Login)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 60, 301, 91))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.login_username = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_username.sizePolicy().hasHeightForWidth())
        self.login_username.setSizePolicy(sizePolicy)
        self.login_username.setObjectName(_fromUtf8("login_username"))
        self.verticalLayout.addWidget(self.login_username)
        self.login_password = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_password.sizePolicy().hasHeightForWidth())
        self.login_password.setSizePolicy(sizePolicy)
        self.login_password.setEchoMode(QtGui.QLineEdit.Password)
        self.login_password.setObjectName(_fromUtf8("login_password"))
        self.verticalLayout.addWidget(self.login_password)
        self.layoutWidget1 = QtGui.QWidget(Login)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 160, 301, 51))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.login_btn = QtGui.QPushButton(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_btn.sizePolicy().hasHeightForWidth())
        self.login_btn.setSizePolicy(sizePolicy)
        self.login_btn.setAutoDefault(True)
        self.login_btn.setObjectName(_fromUtf8("login_btn"))
        self.horizontalLayout.addWidget(self.login_btn)
        self.login_error = QtGui.QLabel(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_error.sizePolicy().hasHeightForWidth())
        self.login_error.setSizePolicy(sizePolicy)
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
        self.horizontalLayout.addWidget(self.login_error)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        Login.setWindowTitle(_translate("Login", "MeX - Login", None))
        self.label_6.setText(_translate("Login", "Admin Login", None))
        self.login_username.setPlaceholderText(_translate("Login", "username", None))
        self.login_password.setPlaceholderText(_translate("Login", "password", None))
        self.login_btn.setText(_translate("Login", "Login", None))

import resources_rc
