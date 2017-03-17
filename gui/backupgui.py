# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/backupgui.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(507, 263)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.log_viewer = QtGui.QPlainTextEdit(self.centralwidget)
        self.log_viewer.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setObjectName(_fromUtf8("log_viewer"))
        self.verticalLayout.addWidget(self.log_viewer)
        self.cancel_btn = QtGui.QPushButton(self.centralwidget)
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.verticalLayout.addWidget(self.cancel_btn)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MeX-LMS Backup", None))
        self.cancel_btn.setText(_translate("MainWindow", "Close", None))

import resources_rc
