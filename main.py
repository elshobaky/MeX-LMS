import sys, logging, datetime
from PyQt4 import QtGui, QtCore
from data_models import init_db, Admin, Member, Book, Borrow
from gui import lmslogin, lmsgui, lmsbookedit, lmsmemberedit, lmsadminedit, lmsborrowedit

class LoginWindwo(QtGui.QMainWindow, lmslogin.Ui_Login):
	def __init__(self, parent=None):
		super(LoginWindwo, self).__init__(parent)
		self.setupUi(self)
		#bind buttons action
		self.login_btn.clicked.connect(self.login)
		self.login_btn.setAutoDefault(True)
		self.login_username.returnPressed.connect(self.login_btn.click)
		self.login_password.returnPressed.connect(self.login_btn.click)

	def login(self):
		username = unicode(self.login_username.text())
		password = unicode(self.login_password.text())
		l_admin = Admin.login(username, password)
		if l_admin:
			global admin
			admin = l_admin
			main_window.update_tabs()
			main_window.show()
			self.close()
		else:
			self.login_error.setText('In correct login')




class MainApp(QtGui.QMainWindow, lmsgui.Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainApp, self).__init__(parent)
		self.setupUi(self)
		########## bind buttons action ##########
		##### books_tab #####
		### book search ###
		self.book_search_btn.clicked.connect(self.update_books_tab)
		# connect pressing enter in line_edit with button action
		self.book_search_id.returnPressed.connect(self.book_search_btn.click)
		self.book_search_title.returnPressed.connect(self.book_search_btn.click)
		self.book_search_author.returnPressed.connect(self.book_search_btn.click)
		self.book_search_publisher.returnPressed.connect(self.book_search_btn.click)
		### book add ###
		self.book_add_btn.clicked.connect(self.add_book)
		### book table ###
		self.books_table.doubleClicked.connect(self.books_table_clicked)
		# connect pressing enter in line_edit with button action
		self.book_add_title.returnPressed.connect(self.book_add_btn.click)
		self.book_add_author.returnPressed.connect(self.book_add_btn.click)
		self.book_add_publisher.returnPressed.connect(self.book_add_btn.click)
		self.book_add_copies.returnPressed.connect(self.book_add_btn.click)
		##### members_tab #####
		### member search ###
		self.member_search_btn.clicked.connect(self.update_members_tab)
		# connect pressing enter in line_edit with button action
		self.member_search_id.returnPressed.connect(self.member_search_btn.click)
		self.member_search_name.returnPressed.connect(self.member_search_btn.click)
		self.member_search_email.returnPressed.connect(self.member_search_btn.click)
		self.member_search_mob.returnPressed.connect(self.member_search_btn.click)
		### member add ###
		self.member_add_btn.clicked.connect(self.add_member)
		# connect pressing enter in line_edit with button action
		self.member_add_name.returnPressed.connect(self.member_add_btn.click)
		self.member_add_email.returnPressed.connect(self.member_add_btn.click)
		self.member_add_mob.returnPressed.connect(self.member_add_btn.click)
		### member table ###
		self.members_table.doubleClicked.connect(self.members_table_clicked)
		##### borrows_tab #####
		### borrow search ###
		self.borrow_search_btn.clicked.connect(self.update_borrows_tab)
		# connect pressing enter in line_edit with button action
		self.borrow_search_id.returnPressed.connect(self.borrow_search_btn.click)
		self.borrow_search_book_id.returnPressed.connect(self.borrow_search_btn.click)
		self.borrow_search_member_id.returnPressed.connect(self.borrow_search_btn.click)
		### borrow add ###
		self.borrow_add_btn.clicked.connect(self.add_borrow)
		# connect pressing enter in line_edit with button action
		self.borrow_add_book_id.returnPressed.connect(self.borrow_add_btn.click)
		self.borrow_add_member_id.returnPressed.connect(self.borrow_add_btn.click)
		### borrow table ###
		self.borrows_table.doubleClicked.connect(self.borrows_table_clicked)
		##### admin_tab #####
		### admin search ###
		self.admin_search_btn.clicked.connect(self.update_admin_tab)
		# connect pressing enter in line_edit with button action
		self.admin_search_id.returnPressed.connect(self.admin_search_btn.click)
		self.admin_search_username.returnPressed.connect(self.admin_search_btn.click)
		### admin add ###
		self.admin_add_btn.clicked.connect(self.add_admin)
		# connect pressing enter in line_edit with button action
		self.admin_add_username.returnPressed.connect(self.admin_add_btn.click)
		self.admin_add_password.returnPressed.connect(self.admin_add_btn.click)
		### admin edit ###
		self.admin_edit_btn.clicked.connect(self.edit_admin)
		# connect pressing enter in line_edit with button action
		self.admin_edit_username.returnPressed.connect(self.admin_edit_btn.click)
		self.admin_edit_old_password.returnPressed.connect(self.admin_edit_btn.click)
		self.admin_edit_new_password.returnPressed.connect(self.admin_edit_btn.click)
		### admin table ###
		self.admins_table.doubleClicked.connect(self.admins_table_clicked)

	def update_tabs(self):
		self.update_admin_tab()
		self.update_books_tab()
		self.update_members_tab()
		self.update_borrows_tab()

	##### Books Tab #####
	def update_books_tab(self):
		books = []
		bid = unicode(self.book_search_id.text())
		bid = int(bid) if bid.isdigit() else 0
		title = unicode(self.book_search_title.text())
		author = unicode(self.book_search_author.text())
		publisher = unicode(self.book_search_publisher.text())
		available = self.book_search_available.isChecked()
		not_available = self.book_search_not_available.isChecked()
		if available == not_available:
			available = None
		elif not_available:
			available = False
		books = Book.get_all(bid=bid, title=title, author=author, publisher=publisher, available=available)
		self.books_table.clearContents()
		self.books_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
		self.books_table.setRowCount(len(books))
		self.books_table.setColumnCount(6)
		for n in range(len(books)):
			self.books_table.setItem(n, 0, QtGui.QTableWidgetItem(unicode(books[n].id)))
			self.books_table.setItem(n, 1, QtGui.QTableWidgetItem(books[n].title))
			self.books_table.setItem(n, 2, QtGui.QTableWidgetItem(unicode(books[n].available)))
			self.books_table.setItem(n, 3, QtGui.QTableWidgetItem(unicode(books[n].copies)))
			self.books_table.setItem(n, 4, QtGui.QTableWidgetItem(unicode(books[n].author)))
			self.books_table.setItem(n, 5, QtGui.QTableWidgetItem(unicode(books[n].publisher)))

	def add_book(self):
		self.book_add_error.setStyleSheet('color: red')
		title = unicode(self.book_add_title.text())
		author  = unicode(self.book_add_author.text())
		publisher = unicode(self.book_add_publisher.text())
		copies = unicode(self.book_add_copies.text())
		available = self.book_add_available.isChecked()
		if not title:
			self.book_add_error.setText('invalid title')
			return
		if not copies:
			copies = '1'
		if not copies.isdigit():
			self.book_add_error.setText('invalid copies no.')
			return
		else:
			copies = int(copies)
		b = Book(title=title, author=author, publisher=publisher, copies=copies, available=available)
		b = b.put()
		self.book_add_error.setStyleSheet('color: green')
		self.book_add_error.setText('Book Added')
		self.update_books_tab()

	def books_table_clicked(self):
		index = self.books_table.selectedIndexes()[0]
		book_id = int(self.books_table.model().data(index).toString())
		book = Book.by_id(book_id)
		if not book:
			return self.book_not_found()
		book_window.view_book(book)

	def book_not_found(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("ERROR!")
		msg.setIcon(QtGui.QMessageBox.Critical)
		msg.setText("Requsted book not found!")
		msg.setStandardButtons(QtGui.QMessageBox.Ok)
		return msg.exec_()

	##### Members Tab #####
	def update_members_tab(self):
		members = []
		mid = unicode(self.member_search_id.text())
		mid = int(mid) if mid.isdigit() else 0
		name = unicode(self.member_search_name.text())
		email = unicode(self.member_search_email.text())
		mob = unicode(self.member_search_mob.text())
		members = Member.get_all(mid=mid, name=name, email=email, mob=mob)
		self.members_table.clearContents()
		self.members_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
		self.members_table.setRowCount(len(members))
		self.members_table.setColumnCount(5)
		for n in range(len(members)):
			self.members_table.setItem(n, 0, QtGui.QTableWidgetItem(unicode(members[n].id)))
			self.members_table.setItem(n, 1, QtGui.QTableWidgetItem(members[n].name))
			self.members_table.setItem(n, 2, QtGui.QTableWidgetItem(members[n].fine or '0'))
			self.members_table.setItem(n, 3, QtGui.QTableWidgetItem(members[n].email or ''))
			self.members_table.setItem(n, 4, QtGui.QTableWidgetItem(members[n].mob or ''))

	def add_member(self):
		self.member_add_error.setStyleSheet('color: red')
		name = unicode(self.member_add_name.text())
		email = unicode(self.member_add_email.text())
		mob = unicode(self.member_add_mob.text())
		if not name:
			self.member_add_error.setText('invalid name')
			return
		m = Member.add(name=name, email=email, mob=mob)
		if isinstance(m, str):
			self.member_add_error.setText(m)
			return
		self.member_add_error.setStyleSheet('color: green')
		self.member_add_error.setText('Member Added')
		self.update_members_tab()

	def members_table_clicked(self):
		index = self.members_table.selectedIndexes()[0]
		member_id = int(self.members_table.model().data(index).toString())
		member = Member.by_id(member_id)
		if not member:
			return self.member_not_found()
		member_window.view_member(member)

	def member_not_found(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("ERROR!")
		msg.setIcon(QtGui.QMessageBox.Critical)
		msg.setText("Requsted member not found!")
		msg.setStandardButtons(QtGui.QMessageBox.Ok)
		return msg.exec_()

	##### Borrows Tab #####
	def update_borrows_tab(self):
		borrows = []
		bid = unicode(self.borrow_search_id.text())
		bid = int(bid) if bid.isdigit() else 0
		book_id = unicode(self.borrow_search_book_id.text())
		book_id = int(book_id) if book_id.isdigit() else 0
		member_id = unicode(self.borrow_search_member_id.text())
		member_id = int(member_id) if member_id.isdigit() else 0
		start = self.borrow_search_start.date().toPyDate()
		if start == datetime.date(2000,1,1): start = None
		end = self.borrow_search_end.date().toPyDate()
		if end == datetime.date(2000,1,1): end = None
		active = self.borrow_search_active.isChecked()
		not_active = self.borrow_search_not_active.isChecked()
		if active == not_active:
			active = None
		elif not_active:
			active = False
		from_date = self.borrow_search_from.date().toPyDate()
		if from_date == datetime.date(2000,1,1): from_date = None
		to_date = self.borrow_search_to.date().toPyDate()
		if to_date == datetime.date(2000,1,1): to_date = None
		borrows = Borrow.get_all(bid=bid, book_id=book_id, member_id=member_id, start=start, end=end, active=active, from_date=from_date, to_date=to_date)
		self.borrows_table.clearContents()
		self.borrows_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
		self.borrows_table.setRowCount(len(borrows))
		self.borrows_table.setColumnCount(6)
		for n in range(len(borrows)):
			self.borrows_table.setItem(n, 0, QtGui.QTableWidgetItem(unicode(borrows[n].id)))
			self.borrows_table.setItem(n, 1, QtGui.QTableWidgetItem(unicode(borrows[n].book_id)))
			self.borrows_table.setItem(n, 2, QtGui.QTableWidgetItem(unicode(borrows[n].member_id)))
			self.borrows_table.setItem(n, 3, QtGui.QTableWidgetItem(unicode(borrows[n].start)))
			self.borrows_table.setItem(n, 4, QtGui.QTableWidgetItem(unicode(borrows[n].end)))
			self.borrows_table.setItem(n, 5, QtGui.QTableWidgetItem(unicode(borrows[n].active)))

	def add_borrow(self):
		self.borrow_add_error.setStyleSheet('color: red')
		book_id = unicode(self.borrow_add_book_id.text())
		member_id = unicode(self.borrow_add_member_id.text())
		start = self.borrow_add_start.date().toPyDate()
		if start == datetime.date(2000,1,1): start = None
		end = self.borrow_add_end.date().toPyDate()
		if end == datetime.date(2000,1,1): end = None
		active = self.borrow_add_active.isChecked()
		m = Borrow.add(book_id=book_id, member_id=member_id, start=start, end=end, active=active)
		if isinstance(m, str):
			self.borrow_add_error.setText(m)
			return
		self.borrow_add_error.setStyleSheet('color: green')
		self.borrow_add_error.setText('Borrow Added')
		self.update_borrows_tab()

	def borrows_table_clicked(self):
		index = self.borrows_table.selectedIndexes()[0]
		borrow_id = int(self.borrows_table.model().data(index).toString())
		borrow = Borrow.by_id(borrow_id)
		if not borrow:
			return self.borrow_not_found()
		borrow_window.view_borrow(borrow)

	def borrow_not_found(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("ERROR!")
		msg.setIcon(QtGui.QMessageBox.Critical)
		msg.setText("Requsted borrow not found!")
		msg.setStandardButtons(QtGui.QMessageBox.Ok)
		return msg.exec_()

	##### Admins Tab #####
	def update_admin_tab(self):
		global admin
		self.admin_edit_username.setText(admin.username)
		aid = unicode(self.admin_search_id.text())
		aid = int(aid) if aid.isdigit() else 0
		username = unicode(self.admin_search_username.text())
		admins = Admin.get_all(aid=aid, username=username)
		self.admins_table.clearContents()
		self.admins_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
		self.admins_table.setRowCount(len(admins))
		self.admins_table.setColumnCount(2)
		for n in range(len(admins)):
			self.admins_table.setItem(n, 0, QtGui.QTableWidgetItem(unicode(admins[n].id)))
			self.admins_table.setItem(n, 1, QtGui.QTableWidgetItem(admins[n].username))

	def add_admin(self):
		self.admin_add_error.setStyleSheet('color: red')
		username = unicode(self.admin_add_username.text())
		password = unicode(self.admin_add_password.text())
		if not (username and password):
			self.admin_add_error.setText('invalid data')
			return
		a = Admin.add(username, password)
		if isinstance(a, str):
			self.admin_add_error.setText(a)
			return
		self.admin_add_error.setStyleSheet('color: green')
		self.admin_add_error.setText('Admin added')
		self.update_admin_tab()

	def edit_admin(self):
		self.admin_edit_error.setStyleSheet('color: red')
		global admin
		old_password = unicode(self.admin_edit_old_password.text())
		new_password = unicode(self.admin_edit_new_password.text())
		a = Admin.login(admin.username, old_password)
		if not a:
			self.admin_edit_error.setText('wrong old password')
			return
		if not new_password:
			self.admin_edit_error.setText('invalid new password')
			return
		admin.password = new_password
		admin = admin.update()
		self.admin_edit_error.setStyleSheet('color: green')
		self.admin_edit_error.setText('Admin edited')
		self.update_admin_tab()

	def admins_table_clicked(self):
		index = self.admins_table.selectedIndexes()[0]
		admin_id = int(self.admins_table.model().data(index).toString())
		ladmin = Admin.by_id(admin_id)
		if not ladmin:
			return self.admin_not_found()
		admin_window.view_admin(ladmin)

	def member_not_found(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("ERROR!")
		msg.setIcon(QtGui.QMessageBox.Critical)
		msg.setText("Requsted admin not found!")
		msg.setStandardButtons(QtGui.QMessageBox.Ok)
		return msg.exec_()



class BookWindow(QtGui.QMainWindow, lmsbookedit.Ui_BookEdit):
	def __init__(self, parent=None):
		super(BookWindow, self).__init__(parent)
		self.setupUi(self)
		########## bind buttons action ##########
		self.book_edit_cancel_btn.clicked.connect(self.close)
		self.book_edit_btn.clicked.connect(self.edit_book)
		self.book_delete_btn.clicked.connect(self.delete_book)

	def view_book(self, book):
		self.book_edit_error.setStyleSheet('color: red')
		self.book_edit_error.setText('')
		self.book_edit_id.setText(str(book.id))
		self.book_edit_title.setText(book.title)
		self.book_edit_author.setText(book.author or '')
		self.book_edit_publisher.setText(book.publisher or '')
		self.book_edit_copies.setText(str(book.copies))
		available = QtCore.Qt.Checked if book.available else QtCore.Qt.Unchecked
		self.book_edit_available.setCheckState(available)
		self.show()

	def edit_book(self):
		book_id = str(self.book_edit_id.text())
		book_id = int(book_id) if book_id.isdigit() else 0
		book = Book.by_id(book_id)
		if not book:
			main_window.book_not_found()
			self.close()
			return
		title = unicode(self.book_edit_title.text())
		author = unicode(self.book_edit_author.text())
		publisher = unicode(self.book_edit_publisher.text())
		copies = str(self.book_edit_copies.text())
		copies = int(copies) if copies.isdigit() else ''
		available = self.book_edit_available.isChecked()
		b = book.update(title=title, author=author, publisher=publisher, copies=copies, available=available)
		if isinstance(b, str):
			self.book_edit_error.setStyleSheet('color: red')
			self.book_edit_error.setText(b)
			return
		self.book_edit_error.setStyleSheet('color: green')
		self.book_edit_error.setText('Your changes has been saved.')
		main_window.update_books_tab()

	def delete_confirm(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("WARNING!")
		msg.setIcon(QtGui.QMessageBox.Question)
		msg.setText("Are you sure you want to delete this book ?")
		msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		return msg.exec_()

	def delete_done(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("DONE!")
		msg.setIcon(QtGui.QMessageBox.Information)
		msg.setText("Book deleted successfully!")
		msg.setStandardButtons(QtGui.QMessageBox.Ok)
		return msg.exec_()

	def delete_book(self):
		do_delete = self.delete_confirm() == 16384
		book_id = str(self.book_edit_id.text())
		book_id = int(book_id) if book_id.isdigit() else 0
		if do_delete:
			Book.delete(book_id)
			self.delete_done
			main_window.update_books_tab()
			self.close()

class MemberWindow(QtGui.QMainWindow, lmsmemberedit.Ui_MemberEdit):
	def __init__(self, parent=None):
		super(MemberWindow, self).__init__(parent)
		self.setupUi(self)
		########## bind buttons action ##########
		self.member_edit_cancel_btn.clicked.connect(self.close)
		self.member_edit_btn.clicked.connect(self.edit_member)
		self.member_delete_btn.clicked.connect(self.delete_member)

	def view_member(self, member):
		self.member_edit_error.setStyleSheet('color: red')
		self.member_edit_error.setText('')
		self.member_edit_id.setText(str(member.id))
		self.member_edit_name.setText(member.name)
		self.member_edit_email.setText(member.email or '')
		self.member_edit_mob.setText(member.mob or '')
		self.member_edit_fine.setText(member.mob or '')
		self.show()

	def edit_member(self):
		member_id = str(self.member_edit_id.text())
		member_id = int(member_id) if member_id.isdigit() else 0
		member = Member.by_id(member_id)
		if not member:
			main_window.member_not_found()
			self.close()
			return
		name = unicode(self.member_edit_name.text())
		email = unicode(self.member_edit_email.text())
		if email == member.email:
			email = None
		mob = unicode(self.member_edit_mob.text())
		if mob == member.mob:
			mob = None
		fine = unicode(self.member_edit_fine.text())
		m = member.update(name=name, email=email, mob=mob, fine=fine)
		if isinstance(m, str):
			self.member_edit_error.setStyleSheet('color: red')
			self.member_edit_error.setText(m)
			return
		self.member_edit_error.setStyleSheet('color: green')
		self.member_edit_error.setText('Your changes has been saved.')
		main_window.update_members_tab()

	def delete_confirm(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("WARNING!")
		msg.setIcon(QtGui.QMessageBox.Question)
		msg.setText("Are you sure you want to delete this member ?")
		msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		return msg.exec_()

	def delete_done(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("DONE!")
		msg.setIcon(QtGui.QMessageBox.Information)
		msg.setText("Member deleted successfully!")
		msg.setStandardButtons(QtGui.QMessageBox.Ok)
		return msg.exec_()

	def delete_member(self):
		do_delete = self.delete_confirm() == 16384
		member_id = str(self.member_edit_id.text())
		member_id = int(member_id) if member_id.isdigit() else 0
		if do_delete:
			Member.delete(member_id)
			self.delete_done
			main_window.update_members_tab()
			self.close()


class BorrowWindow(QtGui.QMainWindow, lmsborrowedit.Ui_BorrowEdit):
	def __init__(self, parent=None):
		super(BorrowWindow, self).__init__(parent)
		self.setupUi(self)
		########## bind buttons action ##########
		self.borrow_edit_cancel_btn.clicked.connect(self.close)
		self.borrow_edit_btn.clicked.connect(self.edit_borrow)
		self.borrow_delete_btn.clicked.connect(self.delete_borrow)

	def view_borrow(self, borrow):
		self.borrow_edit_error.setStyleSheet('color: red')
		self.borrow_edit_error.setText('')
		self.borrow_edit_id.setText(str(borrow.id))
		self.borrow_edit_book_id.setText(str(borrow.book_id))
		self.borrow_edit_member_id.setText(str(borrow.member_id))
		self.borrow_edit_start.setDate(borrow.start)
		self.borrow_edit_end.setDate(borrow.end)
		active = QtCore.Qt.Checked if borrow.active else QtCore.Qt.Unchecked
		self.borrow_edit_active.setCheckState(active)
		self.show()

	def edit_borrow(self):
		borrow_id = str(self.borrow_edit_id.text())
		borrow_id = int(borrow_id) if borrow_id.isdigit() else 0
		borrow = Borrow.by_id(borrow_id)
		if not borrow:
			main_window.borrow_not_found()
			self.close()
			return
		book_id = str(self.borrow_edit_book_id.text())
		book_id = int(book_id) if book_id.isdigit() else 0
		member_id = str(self.borrow_edit_member_id.text())
		member_id = int(member_id) if member_id.isdigit() else 0
		start = self.borrow_edit_start.date().toPyDate()
		end = self.borrow_edit_end.date().toPyDate()
		active = self.borrow_edit_active.isChecked()
		b = borrow.update(book_id=book_id, member_id=member_id, start=start, end=end, active=active)
		if isinstance(b, str):
			self.borrow_edit_error.setStyleSheet('color: red')
			self.borrow_edit_error.setText(b)
			return
		self.borrow_edit_error.setStyleSheet('color: green')
		self.borrow_edit_error.setText('Your changes has been saved.')
		main_window.update_borrows_tab()

	def delete_confirm(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("WARNING!")
		msg.setIcon(QtGui.QMessageBox.Question)
		msg.setText("Are you sure you want to delete this borrow ?")
		msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		return msg.exec_()

	def delete_done(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("DONE!")
		msg.setIcon(QtGui.QMessageBox.Information)
		msg.setText("Borrow deleted successfully!")
		msg.setStandardButtons(QtGui.QMessageBox.Ok)
		return msg.exec_()

	def delete_borrow(self):
		do_delete = self.delete_confirm() == 16384
		borrow_id = str(self.borrow_edit_id.text())
		borrow_id = int(borrow_id) if borrow_id.isdigit() else 0
		if do_delete:
			Borrow.delete(borrow_id)
			self.delete_done
			main_window.update_borrows_tab()
			self.close()


class AdminWindow(QtGui.QMainWindow, lmsadminedit.Ui_AdminEdit):
	def __init__(self, parent=None):
		super(AdminWindow, self).__init__(parent)
		self.setupUi(self)
		########## bind buttons action ##########
		self.admin_edit_cancel_btn.clicked.connect(self.close)
		self.admin_edit_btn_2.clicked.connect(self.edit_admin)
		self.admin_delete_btn.clicked.connect(self.delete_admin)

	def view_admin(self, ladmin):
		self.admin_edit_error_2.setStyleSheet('color: red')
		self.admin_edit_error_2.setText('')
		self.admin_edit_id.setText(str(ladmin.id))
		self.admin_edit_username_2.setText(ladmin.username)
		self.admin_edit_password.setText('')
		self.show()

	def edit_admin(self):
		admin_id = str(self.admin_edit_id.text())
		admin_id = int(admin_id) if admin_id.isdigit() else 0
		ladmin = Admin.by_id(admin_id)
		if not admin:
			main_window.admin_not_found()
			self.close()
			return
		ladmin.password = unicode(self.admin_edit_password.text())
		a = ladmin.update()
		if isinstance(a, str):
			self.admin_edit_error_2.setStyleSheet('color: red')
			self.admin_edit_error_2.setText(a)
			return
		self.admin_edit_error_2.setStyleSheet('color: green')
		self.admin_edit_error_2.setText('Your changes has been saved.')
		main_window.update_admin_tab()

	def delete_confirm(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("WARNING!")
		msg.setIcon(QtGui.QMessageBox.Question)
		msg.setText("Are you sure you want to delete this admin ?")
		msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		return msg.exec_()

	def delete_done(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("DONE!")
		msg.setIcon(QtGui.QMessageBox.Information)
		msg.setText("Admin deleted successfully!")
		msg.setStandardButtons(QtGui.QMessageBox.Ok)
		return msg.exec_()

	def delete_admin(self):
		do_delete = self.delete_confirm() == 16384
		admin_id = str(self.admin_edit_id.text())
		admin_id = int(admin_id) if admin_id.isdigit() else 0
		if do_delete:
			Admin.delete(admin_id)
			self.delete_done
			main_window.update_admin_tab()
			self.close()


def check_run_first_time_run():
	try:
		init_db()
		admins = Admin.get_all()
		if not admins:
			Admin.add('admin', 'admin')
	except Exception as e:
		logging.error(e)


if __name__ == '__main__':
	admin = None
	check_run_first_time_run()
	app = QtGui.QApplication(sys.argv)
	login_window = LoginWindwo()
	main_window = MainApp()
	book_window = BookWindow()
	member_window = MemberWindow()
	borrow_window = BorrowWindow()
	admin_window = AdminWindow()
	login_window.show()
	app.exec_()