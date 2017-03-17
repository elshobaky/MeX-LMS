# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/bookedit.ui'
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

class Ui_BookEdit(object):
    def setupUi(self, BookEdit):
        BookEdit.setObjectName(_fromUtf8("BookEdit"))
        BookEdit.resize(524, 520)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BookEdit.setWindowIcon(icon)
        BookEdit.setStyleSheet(_fromUtf8(""))
        self.label_6 = QtGui.QLabel(BookEdit)
        self.label_6.setGeometry(QtCore.QRect(160, 10, 201, 51))
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
        self.borrow_book_btn = QtGui.QPushButton(BookEdit)
        self.borrow_book_btn.setGeometry(QtCore.QRect(200, 70, 121, 23))
        self.borrow_book_btn.setObjectName(_fromUtf8("borrow_book_btn"))
        self.layoutWidget = QtGui.QWidget(BookEdit)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 420, 431, 81))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.book_edit_error = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.book_edit_error.setFont(font)
        self.book_edit_error.setText(_fromUtf8(""))
        self.book_edit_error.setAlignment(QtCore.Qt.AlignCenter)
        self.book_edit_error.setWordWrap(True)
        self.book_edit_error.setObjectName(_fromUtf8("book_edit_error"))
        self.verticalLayout.addWidget(self.book_edit_error)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.book_delete_btn = QtGui.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.book_delete_btn.setFont(font)
        self.book_delete_btn.setCheckable(False)
        self.book_delete_btn.setAutoDefault(True)
        self.book_delete_btn.setObjectName(_fromUtf8("book_delete_btn"))
        self.horizontalLayout.addWidget(self.book_delete_btn)
        self.book_edit_cancel_btn = QtGui.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.book_edit_cancel_btn.setFont(font)
        self.book_edit_cancel_btn.setAutoDefault(True)
        self.book_edit_cancel_btn.setObjectName(_fromUtf8("book_edit_cancel_btn"))
        self.horizontalLayout.addWidget(self.book_edit_cancel_btn)
        self.book_edit_btn = QtGui.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.book_edit_btn.setFont(font)
        self.book_edit_btn.setAutoDefault(True)
        self.book_edit_btn.setFlat(False)
        self.book_edit_btn.setObjectName(_fromUtf8("book_edit_btn"))
        self.horizontalLayout.addWidget(self.book_edit_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.layoutWidget1 = QtGui.QWidget(BookEdit)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 101, 481, 311))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setFrameShape(QtGui.QFrame.NoFrame)
        self.label.setFrameShadow(QtGui.QFrame.Plain)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_6.addWidget(self.label)
        self.book_edit_id = QtGui.QLineEdit(self.layoutWidget1)
        self.book_edit_id.setReadOnly(True)
        self.book_edit_id.setObjectName(_fromUtf8("book_edit_id"))
        self.horizontalLayout_6.addWidget(self.book_edit_id)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_2.setFrameShadow(QtGui.QFrame.Plain)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.book_edit_title = QtGui.QLineEdit(self.layoutWidget1)
        self.book_edit_title.setObjectName(_fromUtf8("book_edit_title"))
        self.horizontalLayout_5.addWidget(self.book_edit_title)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        self.label_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_3.setFrameShadow(QtGui.QFrame.Plain)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.book_edit_author = QtGui.QLineEdit(self.layoutWidget1)
        self.book_edit_author.setInputMethodHints(QtCore.Qt.ImhNone)
        self.book_edit_author.setObjectName(_fromUtf8("book_edit_author"))
        self.horizontalLayout_4.addWidget(self.book_edit_author)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_9 = QtGui.QLabel(self.layoutWidget1)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_9.addWidget(self.label_9)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.book_edit_cat_id = QtGui.QLineEdit(self.layoutWidget1)
        self.book_edit_cat_id.setInputMethodHints(QtCore.Qt.ImhNone)
        self.book_edit_cat_id.setReadOnly(True)
        self.book_edit_cat_id.setObjectName(_fromUtf8("book_edit_cat_id"))
        self.horizontalLayout_3.addWidget(self.book_edit_cat_id)
        self.book_edit_cat_name = QtGui.QComboBox(self.layoutWidget1)
        self.book_edit_cat_name.setObjectName(_fromUtf8("book_edit_cat_name"))
        self.horizontalLayout_3.addWidget(self.book_edit_cat_name)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.book_edit_cat_custom_id = QtGui.QLineEdit(self.layoutWidget1)
        self.book_edit_cat_custom_id.setInputMethodHints(QtCore.Qt.ImhNone)
        self.book_edit_cat_custom_id.setReadOnly(True)
        self.book_edit_cat_custom_id.setObjectName(_fromUtf8("book_edit_cat_custom_id"))
        self.horizontalLayout_8.addWidget(self.book_edit_cat_custom_id)
        self.book_edit_cat_order = QtGui.QLineEdit(self.layoutWidget1)
        self.book_edit_cat_order.setInputMethodHints(QtCore.Qt.ImhNone)
        self.book_edit_cat_order.setObjectName(_fromUtf8("book_edit_cat_order"))
        self.horizontalLayout_8.addWidget(self.book_edit_cat_order)
        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9.addLayout(self.verticalLayout_2)
        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(1, 5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_10 = QtGui.QLabel(self.layoutWidget1)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_10.addWidget(self.label_10)
        self.book_edit_state = QtGui.QPlainTextEdit(self.layoutWidget1)
        self.book_edit_state.setObjectName(_fromUtf8("book_edit_state"))
        self.horizontalLayout_10.addWidget(self.book_edit_state)
        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_5 = QtGui.QLabel(self.layoutWidget1)
        self.label_5.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_5.setFrameShadow(QtGui.QFrame.Plain)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.book_edit_copies = QtGui.QLineEdit(self.layoutWidget1)
        self.book_edit_copies.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.book_edit_copies.setText(_fromUtf8(""))
        self.book_edit_copies.setObjectName(_fromUtf8("book_edit_copies"))
        self.horizontalLayout_2.addWidget(self.book_edit_copies)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_7 = QtGui.QLabel(self.layoutWidget1)
        self.label_7.setText(_fromUtf8(""))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_7.addWidget(self.label_7)
        self.book_edit_available = QtGui.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.book_edit_available.setFont(font)
        self.book_edit_available.setChecked(False)
        self.book_edit_available.setTristate(False)
        self.book_edit_available.setObjectName(_fromUtf8("book_edit_available"))
        self.horizontalLayout_7.addWidget(self.book_edit_available)
        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.retranslateUi(BookEdit)
        QtCore.QMetaObject.connectSlotsByName(BookEdit)

    def retranslateUi(self, BookEdit):
        BookEdit.setWindowTitle(_translate("BookEdit", "MeX LMS - Edit book", None))
        self.label_6.setText(_translate("BookEdit", "Edit Book", None))
        self.borrow_book_btn.setText(_translate("BookEdit", "Borrrow this book", None))
        self.book_delete_btn.setText(_translate("BookEdit", "Delete", None))
        self.book_edit_cancel_btn.setText(_translate("BookEdit", "Close", None))
        self.book_edit_btn.setText(_translate("BookEdit", "Save", None))
        self.label.setText(_translate("BookEdit", "ID", None))
        self.book_edit_id.setPlaceholderText(_translate("BookEdit", "ID", None))
        self.label_2.setText(_translate("BookEdit", "Title", None))
        self.book_edit_title.setPlaceholderText(_translate("BookEdit", "Title", None))
        self.label_3.setText(_translate("BookEdit", "Author", None))
        self.book_edit_author.setPlaceholderText(_translate("BookEdit", "Author", None))
        self.label_9.setText(_translate("BookEdit", "Category:", None))
        self.book_edit_cat_id.setPlaceholderText(_translate("BookEdit", "ID", None))
        self.book_edit_cat_custom_id.setPlaceholderText(_translate("BookEdit", "Custom ID", None))
        self.book_edit_cat_order.setPlaceholderText(_translate("BookEdit", "Book order in category", None))
        self.label_10.setText(_translate("BookEdit", "State:", None))
        self.label_5.setText(_translate("BookEdit", "No. of copies", None))
        self.book_edit_copies.setPlaceholderText(_translate("BookEdit", "No. of copies", None))
        self.book_edit_available.setText(_translate("BookEdit", "Available", None))

import resources_rc