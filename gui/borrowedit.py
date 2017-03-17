# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/borrowedit.ui'
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

class Ui_BorrowEdit(object):
    def setupUi(self, BorrowEdit):
        BorrowEdit.setObjectName(_fromUtf8("BorrowEdit"))
        BorrowEdit.resize(509, 385)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BorrowEdit.setWindowIcon(icon)
        BorrowEdit.setStyleSheet(_fromUtf8(""))
        self.label_6 = QtGui.QLabel(BorrowEdit)
        self.label_6.setGeometry(QtCore.QRect(150, 10, 211, 41))
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
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.layoutWidget = QtGui.QWidget(BorrowEdit)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 60, 461, 221))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setFrameShape(QtGui.QFrame.NoFrame)
        self.label.setFrameShadow(QtGui.QFrame.Plain)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.borrow_edit_id = QtGui.QLineEdit(self.layoutWidget)
        self.borrow_edit_id.setReadOnly(True)
        self.borrow_edit_id.setObjectName(_fromUtf8("borrow_edit_id"))
        self.horizontalLayout_2.addWidget(self.borrow_edit_id)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_2.setFrameShadow(QtGui.QFrame.Plain)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.borrow_edit_book_id = QtGui.QLineEdit(self.layoutWidget)
        self.borrow_edit_book_id.setObjectName(_fromUtf8("borrow_edit_book_id"))
        self.horizontalLayout_3.addWidget(self.borrow_edit_book_id)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_3.setFrameShadow(QtGui.QFrame.Plain)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.borrow_edit_member_id = QtGui.QLineEdit(self.layoutWidget)
        self.borrow_edit_member_id.setInputMethodHints(QtCore.Qt.ImhNone)
        self.borrow_edit_member_id.setObjectName(_fromUtf8("borrow_edit_member_id"))
        self.horizontalLayout_4.addWidget(self.borrow_edit_member_id)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_4.setFrameShadow(QtGui.QFrame.Plain)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_5.addWidget(self.label_4)
        self.borrow_edit_start = QtGui.QDateEdit(self.layoutWidget)
        self.borrow_edit_start.setCalendarPopup(True)
        self.borrow_edit_start.setObjectName(_fromUtf8("borrow_edit_start"))
        self.horizontalLayout_5.addWidget(self.borrow_edit_start)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_5.setFrameShadow(QtGui.QFrame.Plain)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_6.addWidget(self.label_5)
        self.borrow_edit_end = QtGui.QDateEdit(self.layoutWidget)
        self.borrow_edit_end.setCalendarPopup(True)
        self.borrow_edit_end.setObjectName(_fromUtf8("borrow_edit_end"))
        self.horizontalLayout_6.addWidget(self.borrow_edit_end)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_7 = QtGui.QLabel(self.layoutWidget)
        self.label_7.setText(_fromUtf8(""))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout.addWidget(self.label_7)
        self.borrow_edit_active = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.borrow_edit_active.setFont(font)
        self.borrow_edit_active.setChecked(False)
        self.borrow_edit_active.setTristate(False)
        self.borrow_edit_active.setObjectName(_fromUtf8("borrow_edit_active"))
        self.horizontalLayout.addWidget(self.borrow_edit_active)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.layoutWidget1 = QtGui.QWidget(BorrowEdit)
        self.layoutWidget1.setGeometry(QtCore.QRect(50, 290, 421, 91))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.borrow_edit_error = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.borrow_edit_error.setFont(font)
        self.borrow_edit_error.setText(_fromUtf8(""))
        self.borrow_edit_error.setAlignment(QtCore.Qt.AlignCenter)
        self.borrow_edit_error.setWordWrap(True)
        self.borrow_edit_error.setObjectName(_fromUtf8("borrow_edit_error"))
        self.verticalLayout_2.addWidget(self.borrow_edit_error)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.borrow_delete_btn = QtGui.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.borrow_delete_btn.setFont(font)
        self.borrow_delete_btn.setCheckable(False)
        self.borrow_delete_btn.setAutoDefault(True)
        self.borrow_delete_btn.setObjectName(_fromUtf8("borrow_delete_btn"))
        self.horizontalLayout_7.addWidget(self.borrow_delete_btn)
        self.borrow_edit_cancel_btn = QtGui.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.borrow_edit_cancel_btn.setFont(font)
        self.borrow_edit_cancel_btn.setAutoDefault(True)
        self.borrow_edit_cancel_btn.setObjectName(_fromUtf8("borrow_edit_cancel_btn"))
        self.horizontalLayout_7.addWidget(self.borrow_edit_cancel_btn)
        self.borrow_edit_btn = QtGui.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.borrow_edit_btn.setFont(font)
        self.borrow_edit_btn.setAutoDefault(True)
        self.borrow_edit_btn.setFlat(False)
        self.borrow_edit_btn.setObjectName(_fromUtf8("borrow_edit_btn"))
        self.horizontalLayout_7.addWidget(self.borrow_edit_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.retranslateUi(BorrowEdit)
        QtCore.QMetaObject.connectSlotsByName(BorrowEdit)

    def retranslateUi(self, BorrowEdit):
        BorrowEdit.setWindowTitle(_translate("BorrowEdit", "MeX LMS - Edit borrow", None))
        self.label_6.setText(_translate("BorrowEdit", "Edit Borrow", None))
        self.label.setText(_translate("BorrowEdit", "ID", None))
        self.borrow_edit_id.setPlaceholderText(_translate("BorrowEdit", "ID", None))
        self.label_2.setText(_translate("BorrowEdit", "Book ID", None))
        self.borrow_edit_book_id.setPlaceholderText(_translate("BorrowEdit", "Book ID", None))
        self.label_3.setText(_translate("BorrowEdit", "Member ID", None))
        self.borrow_edit_member_id.setPlaceholderText(_translate("BorrowEdit", "Member ID", None))
        self.label_4.setText(_translate("BorrowEdit", "Start", None))
        self.label_5.setText(_translate("BorrowEdit", "End", None))
        self.borrow_edit_active.setText(_translate("BorrowEdit", "Active", None))
        self.borrow_delete_btn.setText(_translate("BorrowEdit", "Delete", None))
        self.borrow_edit_cancel_btn.setText(_translate("BorrowEdit", "Close", None))
        self.borrow_edit_btn.setText(_translate("BorrowEdit", "Save", None))

import resources_rc