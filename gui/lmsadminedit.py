# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lmsadminedit.ui'
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

class Ui_AdminEdit(object):
    def setupUi(self, AdminEdit):
        AdminEdit.setObjectName(_fromUtf8("AdminEdit"))
        AdminEdit.resize(509, 261)
        self.admin_edit_username_2 = QtGui.QLineEdit(AdminEdit)
        self.admin_edit_username_2.setGeometry(QtCore.QRect(150, 100, 221, 32))
        self.admin_edit_username_2.setReadOnly(True)
        self.admin_edit_username_2.setObjectName(_fromUtf8("admin_edit_username_2"))
        self.admin_edit_password = QtGui.QLineEdit(AdminEdit)
        self.admin_edit_password.setGeometry(QtCore.QRect(150, 140, 221, 32))
        self.admin_edit_password.setInputMethodHints(QtCore.Qt.ImhEmailCharactersOnly)
        self.admin_edit_password.setObjectName(_fromUtf8("admin_edit_password"))
        self.label_2 = QtGui.QLabel(AdminEdit)
        self.label_2.setGeometry(QtCore.QRect(50, 100, 91, 26))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_2.setFrameShadow(QtGui.QFrame.Plain)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(AdminEdit)
        self.label_3.setGeometry(QtCore.QRect(60, 140, 81, 26))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_3.setFrameShadow(QtGui.QFrame.Plain)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_6 = QtGui.QLabel(AdminEdit)
        self.label_6.setGeometry(QtCore.QRect(190, 10, 131, 41))
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
        self.admin_edit_btn_2 = QtGui.QPushButton(AdminEdit)
        self.admin_edit_btn_2.setGeometry(QtCore.QRect(310, 220, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.admin_edit_btn_2.setFont(font)
        self.admin_edit_btn_2.setAutoDefault(True)
        self.admin_edit_btn_2.setFlat(False)
        self.admin_edit_btn_2.setObjectName(_fromUtf8("admin_edit_btn_2"))
        self.admin_edit_cancel_btn = QtGui.QPushButton(AdminEdit)
        self.admin_edit_cancel_btn.setGeometry(QtCore.QRect(210, 220, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.admin_edit_cancel_btn.setFont(font)
        self.admin_edit_cancel_btn.setAutoDefault(True)
        self.admin_edit_cancel_btn.setObjectName(_fromUtf8("admin_edit_cancel_btn"))
        self.admin_delete_btn = QtGui.QPushButton(AdminEdit)
        self.admin_delete_btn.setGeometry(QtCore.QRect(110, 220, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.admin_delete_btn.setFont(font)
        self.admin_delete_btn.setCheckable(False)
        self.admin_delete_btn.setAutoDefault(True)
        self.admin_delete_btn.setObjectName(_fromUtf8("admin_delete_btn"))
        self.admin_edit_error_2 = QtGui.QLabel(AdminEdit)
        self.admin_edit_error_2.setGeometry(QtCore.QRect(150, 180, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.admin_edit_error_2.setFont(font)
        self.admin_edit_error_2.setText(_fromUtf8(""))
        self.admin_edit_error_2.setObjectName(_fromUtf8("admin_edit_error_2"))
        self.admin_edit_id = QtGui.QLineEdit(AdminEdit)
        self.admin_edit_id.setGeometry(QtCore.QRect(150, 60, 221, 32))
        self.admin_edit_id.setReadOnly(True)
        self.admin_edit_id.setObjectName(_fromUtf8("admin_edit_id"))
        self.label = QtGui.QLabel(AdminEdit)
        self.label.setGeometry(QtCore.QRect(110, 60, 31, 26))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setFrameShape(QtGui.QFrame.NoFrame)
        self.label.setFrameShadow(QtGui.QFrame.Plain)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(AdminEdit)
        QtCore.QMetaObject.connectSlotsByName(AdminEdit)

    def retranslateUi(self, AdminEdit):
        AdminEdit.setWindowTitle(_translate("AdminEdit", "MeX LMS - Edit Admin", None))
        self.admin_edit_username_2.setPlaceholderText(_translate("AdminEdit", "username", None))
        self.admin_edit_password.setPlaceholderText(_translate("AdminEdit", "password", None))
        self.label_2.setText(_translate("AdminEdit", "Username", None))
        self.label_3.setText(_translate("AdminEdit", "Password", None))
        self.label_6.setText(_translate("AdminEdit", "Edit Admin", None))
        self.admin_edit_btn_2.setText(_translate("AdminEdit", "Save", None))
        self.admin_edit_cancel_btn.setText(_translate("AdminEdit", "Close", None))
        self.admin_delete_btn.setText(_translate("AdminEdit", "Delete", None))
        self.admin_edit_id.setPlaceholderText(_translate("AdminEdit", "ID", None))
        self.label.setText(_translate("AdminEdit", "ID", None))

