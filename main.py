import sys
import os
import logging
import datetime
import time
import csv
import threading
from config import (config, APP_TITLE, REQ_ADMIN_LOGIN,
                    LOCALE, locale_options, TRANS_DIR,
                    default_layout_direction, default_trans_file,
                    STYLE, style_options, stylesheets, STYLE_DIR,
                    BASE_ADMIN_ROLES,
                    FINE, BORROW_PERIOD,
                    BACKUP_ON_EXIT, BACKUP_CSV_FILES,
                    BACKUP_DB_FILE, MAIN_DIR,
                    DB_PATH, BACKUP_DIR, EXPORT_DIR,
                    REP_TEMPL_DIR)
from db.models import init_db, Admin, Member, Cat, Book, Borrow
import db.models
from shutil import copyfile
from PyQt4 import QtGui, QtCore
from gui import (logingui, maingui, adminedit,
                 memberedit, bookedit, catedit, borrowedit,
                 backupgui)
from gdrive import gdrive
from assets.unicode_csv import UnicodeWriter
import imp

# report templates
import jinja2
from PyQt4.QtWebKit import QWebView

# internationalization
translate = QtCore.QCoreApplication.translate

# Jinja2 template environment
template_dir = os.path.join(REP_TEMPL_DIR, 'templates')
css_dir = os.path.join(REP_TEMPL_DIR, 'css')
env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


def render_template(template_file, **kwargs):
    template = env.get_template(template_file)
    css = ''
    with open(os.path.join(css_dir, 'bootstrap.css'), 'r') as bootstrap:
        css += bootstrap.read()
    with open(os.path.join(css_dir, 'style.css'), 'r') as style:
        css += style.read()
    return template.render(css=css, **kwargs)


MOD_MASK = (QtCore.Qt.CTRL | QtCore.Qt.ALT | QtCore.Qt.SHIFT | QtCore.Qt.META)


class Browser(QWebView):

    def __init__(self, parent=None):
        super(Browser, self).__init__(parent)
        self.printKeyPressed.connect(self.print_pdf)

    def render(self, template_file, **kwargs):
        html = render_template(template_file, **kwargs)
        self.setHtml(html)
        self.show()
        self.setWindowTitle(self.title())

    printKeyPressed = QtCore.pyqtSignal(str)

    def keyPressEvent(self, event):
        keyname = ''
        key = event.key()
        modifiers = int(event.modifiers())
        if (modifiers and modifiers & MOD_MASK == modifiers and
            key > 0 and key != QtCore.Qt.Key_Shift and key != QtCore.Qt.Key_Alt and
                key != QtCore.Qt.Key_Control and key != QtCore.Qt.Key_Meta):

            keyname = QtGui.QKeySequence(modifiers + key).toString()

            # print('event.text(): %r' % event.text())
            # print('event.key(): %d, %#x, %s' % (key, key, keyname))
        if keyname == 'Ctrl+P':
            self.printKeyPressed.emit(keyname)

    def print_pdf(self, ignore):
        file_name = 'report-{}.pdf'.format(int(time.time()))
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printer.setPageSize(QtGui.QPrinter.A4)
        printer.setColorMode(QtGui.QPrinter.Color)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(file_name)
        self.page().mainFrame().print_(printer)
        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_dir, file_name)
        os.system("start " + file_path)


class LoginWindwo(QtGui.QMainWindow, logingui.Ui_Login):

    def __init__(self, parent=None):
        super(LoginWindwo, self).__init__(parent)
        self.setupUi(self)
        # bind buttons action
        self.login_btn.clicked.connect(self.login)
        self.login_btn.setAutoDefault(True)
        self.login_username.returnPressed.connect(self.login_btn.click)
        self.login_password.returnPressed.connect(self.login_btn.click)

    def login(self):
        username = unicode(self.login_username.text())
        password = unicode(self.login_password.text())
        l_admin = Admin.login(username, password)
        if l_admin:
            global admin, admin_roles
            db.models.current_admin = l_admin
            admin = l_admin
            admin_roles = admin.roles
            main_window.initialize()
            main_window.show()
            self.close()
        else:
            self.login_error.setText(self.tr('In correct login'))


class QPlainTextEditLogger(logging.Handler):

    def __init__(self, parent=None):
        super(QPlainTextEditLogger, self).__init__()
        self.widget = main_window.log_viewer

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

    def write(self, m):
        pass


class MainWindow(QtGui.QMainWindow, maingui.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # sync navigation listwidget with main_tabs stacked widget
        self.nav_list.setCurrentRow(0)
        self.main_tabs.setCurrentIndex(0)
        self.nav_list.currentRowChanged.connect(self.navigate)
        # assign variables
        self.books_cats = None
        # init and update tabs
        # self.initialize()

    def initialize(self):
        # # # settings tabs
        self.settings_tabs.setCurrentIndex(0)
        global admin
        self.admin = admin
        # # admin tab
        if self.admin:
            self.admin_tab.setEnabled(True)
            self.init_admin_tab()
            self.update_admin_tab()
        else:
            self.admin_tab.setEnabled(False)
            self.settings_tabs.setCurrentIndex(1)
        # # options tab
        self.init_options_tab()
        self.update_options_tab()
        # # members tab
        self.members_tabs.setCurrentIndex(0)
        self.init_members_tab()
        self.update_members_tab()
        # # books tab
        self.books_tabs.setCurrentIndex(0)
        self.init_books_tab()
        self.update_books_tab()
        # cats tab
        self.init_cats_tab()
        self.update_cats_tab()
        # # borrows tab
        self.borrows_tabs.setCurrentIndex(0)
        self.init_borrows_tab()
        self.update_borrows_tab()

    def initialize_admin(self):
        global admin
        self.admin = admin
        # # admin tab
        if self.admin:
            self.admin_tab.setEnabled(True)
            self.init_admin_tab()
            self.update_admin_tab()
        else:
            self.admin_tab.setEnabled(False)
            self.settings_tabs.setCurrentIndex(1)

    def config_logging(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logTextBox = QPlainTextEditLogger(self)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        logTextBox.setFormatter(formatter)
        logger.addHandler(logTextBox)

    def navigate(self, item):
        row = self.nav_list.currentRow()
        self.main_tabs.setCurrentIndex(row)

    # Admins Tab #####
    def init_admin_tab(self):
        # admin search ###
        self.admin_search_btn.clicked.connect(self.update_admin_tab)
        # connect pressing enter in line_edit with button action
        self.admin_search_id.returnPressed.connect(self.admin_search_btn.click)
        self.admin_search_username.returnPressed.connect(
            self.admin_search_btn.click)
        # admin add ###
        self.admin_add_btn.clicked.connect(self.add_admin)
        # connect pressing enter in line_edit with button action
        self.admin_add_username.returnPressed.connect(self.admin_add_btn.click)
        self.admin_add_password.returnPressed.connect(self.admin_add_btn.click)
        # admin edit ###
        self.admin_edit_btn.clicked.connect(self.edit_admin)
        # connect pressing enter in line_edit with button action
        self.admin_edit_username.returnPressed.connect(
            self.admin_edit_btn.click)
        self.admin_edit_old_password.returnPressed.connect(
            self.admin_edit_btn.click)
        self.admin_edit_new_password.returnPressed.connect(
            self.admin_edit_btn.click)
        # admin table ###
        self.admins_table.horizontalHeader().setStretchLastSection(True)
        self.admins_table.doubleClicked.connect(self.admins_table_clicked)

    def update_admin_tab(self):
        # add admin roles
        """
        for role in BASE_ADMIN_ROLES:
            self.admin_add_roles.addItem('>'.join(role.split('>')[2:]))
        """
        # self.admin_add_error.setStyleSheet('color: red')
        # self.admin_add_error.setText('')
        global admin
        self.admin_edit_username.setText(admin.username)
        aid = unicode(self.admin_search_id.text())
        aid = int(aid) if aid.isdigit() else 0
        username = unicode(self.admin_search_username.text())
        admins = Admin.get(id=aid, username_like=username)
        self.admins_table.clearContents()
        self.admins_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.admins_table.setRowCount(len(admins))
        self.admins_table.setColumnCount(2)
        for n in range(len(admins)):
            self.admins_table.setItem(
                n, 0, QtGui.QTableWidgetItem(unicode(admins[n].id)))
            self.admins_table.setItem(
                n, 1, QtGui.QTableWidgetItem(admins[n].username))

    def add_admin(self):
        self.admin_add_error.setStyleSheet('color: red')
        self.admin_add_error.setText('')
        username = unicode(self.admin_add_username.text())
        password = unicode(self.admin_add_password.text())
        roles = BASE_ADMIN_ROLES
        if not (username and password):
            self.admin_add_error.setText(self.tr('invalid data'))
            return
        a = Admin.add(username, password, roles)
        if type(a) in [str, QtCore.QString]:
            self.admin_add_error.setText(a)
            return
        self.admin_add_error.setStyleSheet('color: green')
        self.admin_add_error.setText(self.tr('Admin added'))
        self.update_admin_tab()

    def edit_admin(self):
        self.admin_edit_error.setStyleSheet('color: red')
        self.admin_add_error.setText('')
        global admin
        old_password = unicode(self.admin_edit_old_password.text())
        new_password = unicode(self.admin_edit_new_password.text())
        a = Admin.login(admin.username, old_password)
        if not a:
            self.admin_edit_error.setText(self.tr('wrong old password'))
            return
        if not new_password:
            self.admin_edit_error.setText(self.tr('invalid new password'))
            return
        admin.password = new_password
        admin = admin.update()
        self.admin_edit_error.setStyleSheet('color: green')
        self.admin_edit_error.setText(self.tr('Admin edited'))
        self.update_admin_tab()

    def admins_table_clicked(self):
        index = self.admins_table.selectedIndexes()[0]
        admin_id = int(self.admins_table.model().data(index).toString())
        ladmin = Admin.by_id(admin_id)
        if not ladmin:
            return self.admin_not_found()
        admin_window.view_admin(ladmin)

    def admin_not_found(self):
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(self.tr("ERROR!"))
        msg.setIcon(QtGui.QMessageBox.Critical)
        msg.setText(self.tr("Requsted admin not found!"))
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        return msg.exec_()

    # Options Tab #####
    def init_options_tab(self):
        self.db_backup_btn.clicked.connect(self.db_backup)
        self.db_restore_btn.clicked.connect(self.db_restore)
        self.db_csv_export_btn.clicked.connect(self.db_csv_export)
        self.cloud_backup_save_btn.clicked.connect(self.cloud_backup_save)
        self.cloud_backup_btn.clicked.connect(self.cloud_backup)
        # edit options
        # self.req_admin_login_edit.setEnabled(False)
        self.options_edit_fine.setText(str(FINE))
        self.options_edit_fine.returnPressed.connect(self.options_edit_btn.click)
        self.options_edit_borrow_period.setText(str(BORROW_PERIOD))
        self.options_edit_borrow_period.returnPressed.connect(self.options_edit_btn.click)
        self.options_edit_btn.clicked.connect(self.edit_options)

    def update_options_tab(self):
        # self.db_error.setStyleSheet('color: red')
        # self.cloud_backup_error.setStyleSheet('color: red')
        self.req_admin_login_edit.setChecked(REQ_ADMIN_LOGIN)
        # backup
        self.cloud_backup_error.setStyleSheet('color: red')
        self.cloud_backup_error.setText('')
        self.backup_on_exit.setChecked(BACKUP_ON_EXIT)
        self.backup_csv_files.setChecked(BACKUP_CSV_FILES)
        self.backup_db_file.setChecked(BACKUP_DB_FILE)
        if LOCALE in locale_options:
            self.locale_edit.setCurrentIndex(locale_options.index(LOCALE))
        if STYLE in style_options:
            self.style_edit.setCurrentIndex(style_options.index(STYLE))

    def cloud_backup_save(self):
        self.cloud_backup_error.setStyleSheet('color: red')
        self.cloud_backup_error.setText('')
        backup_on_exit = self.backup_on_exit.isChecked()
        backup_csv_files = self.backup_csv_files.isChecked()
        backup_db_file = self.backup_db_file.isChecked()
        config.update(backup_on_exit=backup_on_exit,
                      backup_csv_files=backup_csv_files,
                      backup_db_file=backup_db_file)
        global BACKUP_ON_EXIT, BACKUP_CSV_FILES, BACKUP_DB_FILE
        BACKUP_ON_EXIT = backup_on_exit
        BACKUP_CSV_FILES = backup_csv_files
        BACKUP_DB_FILE = backup_db_file
        self.cloud_backup_error.setStyleSheet('color: green')
        self.cloud_backup_error.setText(self.tr('changes has been saved'))
        self.update_options_tab()
        logging.info('backup settings saved')

    def run_cloud_backup(self):
        logging.info('starting cloud backup ...')
        backup_window.start()
        logging.info('cloud backup finished')

    def cloud_backup(self):
        logging.info('starting cloud backup ....')
        self.cloud_backup_error.setStyleSheet('color: green')
        self.cloud_backup_error.setText(self.tr('starting backup ...'))
        files = []
        if BACKUP_DB_FILE:
            db_file = {"file_path": DB_PATH}
            db_file["title"] = '{}_db_backup_{}.mexdb'.format(APP_TITLE, datetime.datetime.now().date())
            files.append(db_file)
        if BACKUP_CSV_FILES:
            export_dir = os.path.join(MAIN_DIR, 'Backup')
            db_tables = [Member, Book, Borrow, Admin]
            file_names = ['Members_{}.csv', 'Books_{}.csv', 'Borrows_{}.csv', 'Admins_{}.csv']
            file_names = [x.format(datetime.datetime.now().date())
                          for x in file_names]
            for n in range(len(db_tables)):
                records = db_tables[n].get()
                file_path = os.path.join(export_dir, file_names[n])
                files.append({"file_path": file_path, "title": file_names[n]})
                with open(file_path, 'wb') as outfile:
                    outcsv = UnicodeWriter(
                        outfile, delimiter=',', quoting=csv.QUOTE_ALL)
                    outcsv.writerow(
                        [column.name for column in db_tables[n].__mapper__.columns]
                    )
                    for curr in records:
                        row = []
                        for column in db_tables[n].__mapper__.columns:
                            item = getattr(curr, column.name)
                            if isinstance(item, datetime.datetime):
                                item = item.strftime('%d-%m-%Y %I:%M:%S %p')
                            row.append(unicode(item))
                        outcsv.writerow(row)
        for f in files:
            try:
                gdrive.upload_file(f['file_path'], title=f['title'])
            except Exception as e:
                logging.error(e)
                self.cloud_backup_error.setStyleSheet('color: red')
                self.cloud_backup_error.setText(self.tr('Backup Failed'))
        self.cloud_backup_error.setStyleSheet('color: green')
        self.cloud_backup_error.setText(self.tr('backup finished'))
        logging.info('cloud backup finished')

    def db_backup(self):
        self.db_error.setStyleSheet('color: red')
        self.db_error.setText('')
        new_db_name = '{}_db_backup_{}.mexdb'.format(APP_TITLE, datetime.datetime.now().date())
        default_dst = os.path.join(BACKUP_DIR, new_db_name)
        dst = QtGui.QFileDialog.getSaveFileName(
            self, self.tr('Save File'), default_dst, "MeX DB files (*.mexdb *.db)")
        if not dst:
            self.db_error.setText(self.tr('No directory specified'))
            return
        try:
            copyfile(DB_PATH, dst)
            self.db_error.setStyleSheet('color: green')
            self.db_error.setText(self.tr('database backup completed successfully!'))
            logging.info('database backup completed successfully!')
        except Exception as e:
            logging.error(e)
            self.db_error.setText(self.tr('database backup failed!'))

    def restore_confirm(self):
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(self.tr("WARNING!"))
        msg.setIcon(QtGui.QMessageBox.Warning)
        msg.setText(self.tr("Are you sure you want to restore this database ?"))
        msg.setInformativeText(self.tr("If you aren't sure press no and backup first"))
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        return msg.exec_()

    def db_restore(self):
        self.db_error.setStyleSheet('color: red')
        self.db_error.setText('')
        file_name = QtGui.QFileDialog.getOpenFileName(
            self, self.tr('Open File'), BACKUP_DIR, "MeX DB files (*.mexdb *.db)")
        if not file_name:
            self.db_error.setText(self.tr('No directory selected!'))
            return
        do_restore = self.restore_confirm() == 16384
        try:
            if do_restore:
                copyfile(file_name, DB_PATH)
                self.initialize()
                self.db_error.setStyleSheet('color: green')
                self.db_error.setText(self.tr('database restore completed successfully!'))
                logging.info('database restore completed successfully!')
            else:
                self.db_error.setText(self.tr('database restore cancelled!'))
        except Exception as e:
            logging.error(e)
            self.db_error.setText(self.tr('database restore failed!'))

    def edit_options(self):
        self.options_edit_error.setStyleSheet('color: red')
        self.options_edit_error.setText('')
        # request admin login on startup option
        req_admin_login = self.req_admin_login_edit.isChecked()
        # locale
        locale = locale_options[self.locale_edit.currentIndex()]
        # style
        style = style_options[self.style_edit.currentIndex()]
        # fine
        fine = str(self.options_edit_fine.text())
        try:
            fine = float(fine)
        except Exception as e:
            logging.error(e)
            self.options_edit_error.setText(self.tr('invlid fine value'))
            return
        borrow_period = unicode(self.options_edit_borrow_period.text())
        try:
            borrow_period = int(borrow_period)
        except Exception as e:
            logging.error(e)
            self.options_edit_error.setText(self.tr('invalid borrow period'))
            return
        cfg = config.update(app_title=None,
                            req_admin_login=req_admin_login,
                            locale=locale,
                            style=style,
                            fine=fine,
                            borrow_period=borrow_period)
        if type(cfg) in [str, QtCore.QString]:
            self.options_edit_error.setText(cfg)
            return
        # update global variables
        global REQ_ADMIN_LOGIN, LOCALE, STYLE, FINE, BORROW_PERIOD
        REQ_ADMIN_LOGIN = req_admin_login
        LOCALE = locale
        # config_locale(locale=LOCALE)
        STYLE = style
        FINE = fine
        BORROW_PERIOD = borrow_period
        # config_style(style=STYLE)
        self.options_edit_error.setStyleSheet('color: green')
        self.options_edit_error.setText(
            self.tr('Options saved successfully and will take effect next startup!'))
        self.update_options_tab()
        logging.info('options updated')

    def db_csv_export(self):
        self.db_error.setStyleSheet('color: red')
        self.db_error.setText('')
        export_options = ['Entire Database', 'Members', 'Books', 'Borrows', 'Admins']
        db_tables = []
        file_names = []
        export_dir = EXPORT_DIR
        table = export_options[self.db_csv_export_table.currentIndex()]
        if table == 'Entire Database':
            db_tables = [Member, Book, Borrow, Admin]
        elif table == 'Members':
            db_tables.append(Member)
        elif table == 'Books':
            db_tables.append(Book)
        elif table == 'Borrows':
            db_tables.append(Borrow)
        elif table == 'Admins':
            db_tables.append(Admin)
        if len(db_tables) == 1:
            file_name = '{}_{}.csv'.format(
                table, datetime.datetime.now().date())
            default_dst = os.path.join(EXPORT_DIR, file_name)
            dst = QtGui.QFileDialog.getSaveFileName(
                self, self.tr('Save File'), default_dst, "csv files (*.csv)")
            export_dir, file_name = os.path.split(str(dst))
            file_names = [file_name]
        elif len(db_tables) > 1:
            export_dir = QtGui.QFileDialog.getExistingDirectory(
                self,
                self.tr("Select a folder"),
                EXPORT_DIR,
                QtGui.QFileDialog.ShowDirsOnly
            )
            export_dir = str(export_dir)
            file_names = ['Members_{}.csv', 'Books_{}.csv', 'Borrows_{}.csv', 'Admins_{}.csv']
            file_names = [x.format(datetime.datetime.now().date())
                          for x in file_names]
        logging.info('exporting databse to csv files ......')
        for n in range(len(db_tables)):
            records = db_tables[n].get()
            file_path = os.path.join(export_dir, file_names[n])
            with open(file_path, 'wb') as outfile:
                outcsv = UnicodeWriter(
                    outfile, delimiter=';', quoting=csv.QUOTE_ALL)
                outcsv.writerow(
                    [column.name for column in db_tables[n].__mapper__.columns]
                )
                for curr in records:
                    row = []
                    for column in db_tables[n].__mapper__.columns:
                        row.append(unicode(getattr(curr, column.name)))
                    outcsv.writerow(row)
        self.db_error.setStyleSheet('color: green')
        self.db_error.setText(self.tr('Export completed successfully!'))
        logging.info('Database export completed')

    # Members tab #####
    def init_members_tab(self):
        # member search ###
        self.member_search_btn.clicked.connect(self.update_members_tab)
        # connect pressing enter in line_edit with button action
        self.member_search_id.returnPressed.connect(self.member_search_btn.click)
        self.member_search_name.returnPressed.connect(self.member_search_btn.click)
        self.member_search_email.returnPressed.connect(self.member_search_btn.click)
        self.member_search_mob.returnPressed.connect(self.member_search_btn.click)
        # member add ###
        self.member_add_btn.clicked.connect(self.add_member)
        # connect pressing enter in line_edit with button action
        self.member_add_name.returnPressed.connect(self.member_add_btn.click)
        self.member_add_email.returnPressed.connect(self.member_add_btn.click)
        self.member_add_mob.returnPressed.connect(self.member_add_btn.click)
        # member table ###
        self.members_table.horizontalHeader().setStretchLastSection(True)
        self.members_table.doubleClicked.connect(self.members_table_clicked)

    def update_members_tab(self):
        # self.member_add_error.setStyleSheet('color: red')
        members = []
        mid = unicode(self.member_search_id.text())
        mid = int(mid) if mid.isdigit() else 0
        name = unicode(self.member_search_name.text())
        email = unicode(self.member_search_email.text())
        mob = unicode(self.member_search_mob.text())
        members = Member.get(mid=mid, name=name, email=email, mob=mob)
        self.members_table.clearContents()
        self.members_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.members_table.setRowCount(len(members))
        self.members_table.setColumnCount(6)
        for n in range(len(members)):
            self.members_table.setItem(n, 0, QtGui.QTableWidgetItem(unicode(members[n].id)))
            self.members_table.setItem(n, 1, QtGui.QTableWidgetItem(members[n].name))
            self.members_table.setItem(n, 2, QtGui.QTableWidgetItem(members[n].fine or '0'))
            self.members_table.setItem(n, 3, QtGui.QTableWidgetItem(members[n].email or ''))
            self.members_table.setItem(n, 4, QtGui.QTableWidgetItem(members[n].mob or ''))
            self.members_table.setItem(n, 5, QtGui.QTableWidgetItem(members[n].note or ''))

    def add_member(self):
        self.member_add_error.setStyleSheet('color: red')
        self.member_add_error.setText('')
        name = unicode(self.member_add_name.text())
        email = unicode(self.member_add_email.text())
        mob = unicode(self.member_add_mob.text())
        note = unicode(self.member_add_note.toPlainText())
        if not name:
            self.member_add_error.setText(self.tr('invalid name'))
            return
        m = Member.add(name=name, email=email, mob=mob, note=note)
        if type(m) in [str, QtCore.QString]:
            self.member_add_error.setText(m)
            return
        self.member_add_error.setStyleSheet('color: green')
        self.member_add_error.setText(self.tr('Member Added'))
        self.update_members_tab()
        
        # clear member data after correct save.
        self.member_add_name.setText('')
        self.member_add_email.setText('')
        self.member_add_mob.setText('')
        self.member_add_note.clear()

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

    # Books tab #####
    def init_books_tab(self):
        # add categories option
        self.update_book_cats()
        # book search ###
        self.book_search_btn.clicked.connect(self.update_books_tab)
        # connect pressing enter in line_edit with button action
        self.book_search_id.returnPressed.connect(self.book_search_btn.click)
        self.book_search_title.returnPressed.connect(self.book_search_btn.click)
        self.book_search_author.returnPressed.connect(self.book_search_btn.click)
        self.book_search_cat_id.returnPressed.connect(self.book_search_btn.click)
        self.book_search_cat_custom_id.returnPressed.connect(self.book_search_btn.click)
        self.book_search_cat_order.returnPressed.connect(self.book_search_btn.click)
        # book add ###
        self.book_add_copies.setText('1')
        self.book_add_btn.clicked.connect(self.add_book)
        # book table ###
        self.books_table.horizontalHeader().setStretchLastSection(True)
        self.books_table.doubleClicked.connect(self.books_table_clicked)
        # connect pressing enter in line_edit with button action
        self.book_add_title.returnPressed.connect(self.book_add_btn.click)
        self.book_add_author.returnPressed.connect(self.book_add_btn.click)
        self.book_add_cat_id.returnPressed.connect(self.book_add_btn.click)
        self.book_add_cat_custom_id.returnPressed.connect(self.book_add_btn.click)
        self.book_add_cat_order.returnPressed.connect(self.book_add_btn.click)
        self.book_add_copies.returnPressed.connect(self.book_add_btn.click)
        # cat_name change event
        self.book_add_cat_name.currentIndexChanged.connect(self.book_add_cat_name_changed)

    def update_book_cats(self):
        self.books_cats = Cat.get_cats_dict()
        self.book_add_cat_name.clear()
        self.book_search_cat_name.clear()
        # book_window.book_edit_cat_name.clear()
        cat_names = ['None']
        cat_names += [cat['name'] for cat in self.books_cats]
        self.book_add_cat_name.addItems(cat_names)
        self.book_search_cat_name.addItems(cat_names)
        # book_window.book_edit_cat_name.addItems(cat_names)

    def book_add_cat_name_changed(self):
        cat_index = self.book_add_cat_name.currentIndex()
        if cat_index <= 0:
            cat_id = ''
            cat_custom_id = ''
        else:
            cat_index -= 1
            cat_id = self.books_cats[cat_index]['id']
            cat_custom_id = self.books_cats[cat_index]['custom_id']
        self.book_add_cat_id.setText(unicode(cat_id))
        self.book_add_cat_custom_id.setText(cat_custom_id)

    def update_books_tab(self):
        books = []
        bid = unicode(self.book_search_id.text())
        bid = int(bid) if bid.isdigit() else 0
        title = unicode(self.book_search_title.text())
        author = unicode(self.book_search_author.text())
        cat_id = unicode(self.book_search_cat_id.text())
        cat_id = int(cat_id) if cat_id.isdigit() else cat_id
        cat_index = self.book_search_cat_name.currentIndex() - 1
        cat_name = self.books_cats[cat_index]['name'] if cat_index >= 0 else None
        cat_custom_id = unicode(self.book_search_cat_custom_id.text())
        cat_order = unicode(self.book_search_cat_order.text())
        cat_order = int(cat_order) if cat_order.isdigit() else cat_order
        available = self.book_search_available.isChecked()
        not_available = self.book_search_not_available.isChecked()
        if available == not_available:
            available = None
        elif not_available:
            available = False
        books = Book.get(bid=bid, title=title, author=author,
                         cat_id=cat_id, cat_name=cat_name,
                         cat_custom_id=cat_custom_id, cat_order=cat_order,
                         available=available)
        self.books_table.clearContents()
        self.books_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.books_table.setRowCount(len(books))
        self.books_table.setColumnCount(7)
        for n in range(len(books)):
            self.books_table.setItem(n, 0, QtGui.QTableWidgetItem(unicode(books[n].id)))
            self.books_table.setItem(n, 1, QtGui.QTableWidgetItem(books[n].title))
            self.books_table.setItem(n, 2, QtGui.QTableWidgetItem(unicode(books[n].available)))
            self.books_table.setItem(n, 3, QtGui.QTableWidgetItem(unicode(books[n].copies)))
            self.books_table.setItem(n, 4, QtGui.QTableWidgetItem(unicode(books[n].author)))
            # category format
            cat_name = unicode(books[n].cat_name) or ''
            cat_order = unicode(books[n].cat_order) or ''
            cat_custom_id = unicode(books[n].cat_custom_id) or ''
            category = u'{} - {}/{}'.format(cat_name, cat_order, cat_custom_id)
            self.books_table.setItem(n, 5, QtGui.QTableWidgetItem(category))
            self.books_table.setItem(n, 6, QtGui.QTableWidgetItem(unicode(books[n].state)))

    def add_book(self):
        self.book_add_error.setStyleSheet('color: red')
        self.book_add_error.setText('')
        title = unicode(self.book_add_title.text())
        author = unicode(self.book_add_author.text())
        cat_id = unicode(self.book_add_cat_id.text())
        cat_id = int(cat_id) if cat_id.isdigit() else 0
        cat_order = unicode(self.book_add_cat_order.text())
        cat_order = int(cat_order) if cat_order.isdigit() else None
        state = unicode(self.book_add_state.toPlainText())
        copies = unicode(self.book_add_copies.text())
        copies = int(copies) if copies.isdigit() else copies
        available = self.book_add_available.isChecked()
        b = Book.add(title=title, author=author,
                     cat_id=cat_id, cat_order=cat_order, state=state,
                     copies=copies, available=available)
        if type(b) in [str, QtCore.QString]:
            self.book_add_error.setText(b)
            return
        self.book_add_error.setStyleSheet('color: green')
        self.book_add_error.setText(self.tr('Book Added'))
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

    # Cats Tab #####
    def init_cats_tab(self):
        # cat search ###
        self.cat_search_btn.clicked.connect(self.update_cats_tab)
        # connect pressing enter in line_edit with button action
        self.cat_search_id.returnPressed.connect(self.cat_search_btn.click)
        self.cat_search_name.returnPressed.connect(self.cat_search_btn.click)
        self.cat_search_custom_id.returnPressed.connect(self.cat_search_btn.click)
        # cat add ###
        self.cat_add_btn.clicked.connect(self.add_cat)
        # connect pressing enter in line_edit with button action
        self.cat_add_name.returnPressed.connect(self.cat_add_btn.click)
        self.cat_add_custom_id.returnPressed.connect(self.cat_add_btn.click)
        # cat table ###
        self.cats_table.horizontalHeader().setStretchLastSection(True)
        self.cats_table.doubleClicked.connect(self.cats_table_clicked)

    def update_cats_tab(self):
        self.update_book_cats()
        cid = unicode(self.cat_search_id.text())
        cid = int(cid) if cid.isdigit() else 0
        name = unicode(self.cat_search_name.text())
        custom_id = unicode(self.cat_search_custom_id.text())

        cats = Cat.get(id=cid, name=name, custom_id=custom_id)
        self.cats_table.clearContents()
        self.cats_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.cats_table.setRowCount(len(cats))
        self.cats_table.setColumnCount(3)
        for n in range(len(cats)):
            self.cats_table.setItem(n, 0, QtGui.QTableWidgetItem(unicode(cats[n].id)))
            self.cats_table.setItem(n, 1, QtGui.QTableWidgetItem(cats[n].name))
            self.cats_table.setItem(n, 2, QtGui.QTableWidgetItem(unicode(cats[n].custom_id) or ''))

    def add_cat(self):
        self.cat_add_error.setStyleSheet('color: red')
        self.cat_add_error.setText('')
        name = unicode(self.cat_add_name.text())
        custom_id = unicode(self.cat_add_custom_id.text())

        c = Cat.add(name=name, custom_id=custom_id)
        if type(c) in [str, QtCore.QString]:
            self.cat_add_error.setText(c)
            return
        self.cat_add_error.setStyleSheet('color: green')
        self.cat_add_error.setText(self.tr('Category added'))
        self.update_cats_tab()

    def cats_table_clicked(self):
        index = self.cats_table.selectedIndexes()[0]
        cat_id = int(self.cats_table.model().data(index).toString())
        lcat = Cat.by_id(cat_id)
        if not lcat:
            return self.cat_not_found()
        cat_window.view_cat(lcat)

    def cat_not_found(self):
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(self.tr("ERROR!"))
        msg.setIcon(QtGui.QMessageBox.Critical)
        msg.setText(self.tr("Requsted category not found!"))
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        return msg.exec_()

    # Borrows tab #####
    def init_borrows_tab(self):
        # borrow search ###
        self.borrow_search_btn.clicked.connect(self.update_borrows_tab)
        # connect pressing enter in line_edit with button action
        self.borrow_search_id.returnPressed.connect(self.borrow_search_btn.click)
        self.borrow_search_book_id.returnPressed.connect(self.borrow_search_btn.click)
        self.borrow_search_book_title.returnPressed.connect(self.borrow_search_btn.click)
        self.borrow_search_member_id.returnPressed.connect(self.borrow_search_btn.click)
        self.borrow_search_member_name.returnPressed.connect(self.borrow_search_btn.click)
        # borrow add ###
        today_date = datetime.datetime.now().date()
        self.borrow_add_start.setDate(today_date)
        self.borrow_add_end.setDate(today_date + datetime.timedelta(days=BORROW_PERIOD))
        self.borrow_add_btn.clicked.connect(self.add_borrow)
        # connect pressing enter in line_edit with button action
        self.borrow_add_book_id.returnPressed.connect(self.borrow_add_btn.click)
        self.borrow_add_member_id.returnPressed.connect(self.borrow_add_btn.click)
        self.borrow_add_book_id.editingFinished.connect(self.borrow_add_book_id_changed)
        self.borrow_add_member_id.editingFinished.connect(self.borrow_add_member_id_changed)
        # borrow table ###
        self.borrows_table.horizontalHeader().setStretchLastSection(True)
        self.borrows_table.doubleClicked.connect(self.borrows_table_clicked)

    def update_borrows_tab(self):
        borrows = []
        bid = unicode(self.borrow_search_id.text())
        bid = int(bid) if bid.isdigit() else 0
        book_id = unicode(self.borrow_search_book_id.text())
        book_id = int(book_id) if book_id.isdigit() else 0
        book_title = unicode(self.borrow_search_book_title.text())
        member_id = unicode(self.borrow_search_member_id.text())
        member_id = int(member_id) if member_id.isdigit() else 0
        member_name = unicode(self.borrow_search_member_name.text())
        start = self.borrow_search_start.date().toPyDate()
        if start == datetime.date(2000, 1, 1):
            start = None
        end = self.borrow_search_end.date().toPyDate()
        if end == datetime.date(2000, 1, 1):
            end = None
        active = self.borrow_search_active.isChecked()
        not_active = self.borrow_search_not_active.isChecked()
        if active == not_active:
            active = None
        elif not_active:
            active = False
        from_date = self.borrow_search_from.date().toPyDate()
        if from_date == datetime.date(2000, 1, 1):
            from_date = None
        to_date = self.borrow_search_to.date().toPyDate()
        if to_date == datetime.date(2000, 1, 1):
            to_date = None
        borrows = Borrow.get(bid=bid, book_id=book_id, book_title=book_title, member_id=member_id, member_name=member_name, start=start, end=end, active=active, from_date=from_date, to_date=to_date)
        self.borrows_table.clearContents()
        self.borrows_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.borrows_table.setRowCount(len(borrows))
        self.borrows_table.setColumnCount(10)
        for n in range(len(borrows)):
            self.borrows_table.setItem(n, 0, QtGui.QTableWidgetItem(unicode(borrows[n].id)))
            self.borrows_table.setItem(n, 1, QtGui.QTableWidgetItem(unicode(borrows[n].book_id)))
            self.borrows_table.setItem(n, 2, QtGui.QTableWidgetItem(borrows[n].book_title))
            self.borrows_table.setItem(n, 3, QtGui.QTableWidgetItem(unicode(borrows[n].member_id)))
            self.borrows_table.setItem(n, 4, QtGui.QTableWidgetItem(borrows[n].member_name))
            self.borrows_table.setItem(n, 5, QtGui.QTableWidgetItem(unicode(borrows[n].start)))
            self.borrows_table.setItem(n, 6, QtGui.QTableWidgetItem(unicode(borrows[n].end)))
            self.borrows_table.setItem(n, 7, QtGui.QTableWidgetItem(unicode(borrows[n].active)))
            self.borrows_table.setItem(n, 8, QtGui.QTableWidgetItem(unicode(borrows[n].created_by)))
            self.borrows_table.setItem(n, 9, QtGui.QTableWidgetItem(unicode(borrows[n].updated_by)))

    def borrow_add_book_id_changed(self):
        book_id = unicode(self.borrow_add_book_id.text())
        book_id = int(book_id) if book_id.isdigit() else 0
        book = Book.by_id(book_id)
        if not book:
            self.borrow_add_error.setText(self.tr('invalid book id'))
            return
        self.borrow_add_book_title.setText(book.title)

    def borrow_add_member_id_changed(self):
        member_id = unicode(self.borrow_add_member_id.text())
        member_id = int(member_id) if member_id.isdigit() else 0
        member = Member.by_id(member_id)
        if not member:
            self.borrow_add_error.setText(self.tr('invalid memeber id'))
            return
        self.borrow_add_member_name.setText(member.name)

    def add_borrow(self):
        self.borrow_add_error.setStyleSheet('color: red')
        self.borrow_add_error.setText('')
        book_id = unicode(self.borrow_add_book_id.text())
        book_id = int(book_id) if book_id.isdigit() else 0
        member_id = unicode(self.borrow_add_member_id.text())
        member_id = int(member_id) if member_id.isdigit() else 0
        start = self.borrow_add_start.date().toPyDate()
        if start == datetime.date(2000, 1, 1):
            start = None
        end = self.borrow_add_end.date().toPyDate()
        if end == datetime.date(2000, 1, 1):
            end = None
        active = self.borrow_add_active.isChecked()
        if self.admin:
            created_by = '{}({})'.format(self.admin.id, self.admin.username)
        else:
            created_by = ''
        m = Borrow.add(book_id=book_id, member_id=member_id,
                       start=start, end=end, active=active,
                       created_by=created_by)
        if type(m) in [str, QtCore.QString]:
            self.borrow_add_error.setText(m)
            return
        self.borrow_add_error.setStyleSheet('color: green')
        self.borrow_add_error.setText(self.tr('Borrow Added'))
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


class AdminWindow(QtGui.QMainWindow, adminedit.Ui_AdminEdit):

    def __init__(self, parent=None):
        super(AdminWindow, self).__init__(parent)
        self.setupUi(self)
        # bind buttons action ##########
        self.admin_edit_cancel_btn.clicked.connect(self.close)
        self.admin_edit_btn.clicked.connect(self.edit_admin)
        self.admin_delete_btn.clicked.connect(self.delete_admin)

        self.admin_edit_id.returnPressed.connect(self.admin_edit_btn.click)
        self.admin_edit_username.returnPressed.connect(
            self.admin_edit_btn.click)
        self.admin_edit_password.returnPressed.connect(
            self.admin_edit_btn.click)

    def view_admin(self, ladmin):
        self.admin_edit_error.setStyleSheet('color: red')
        self.admin_edit_error.setText('')
        self.admin_edit_id.setText(str(ladmin.id))
        self.admin_edit_username.setText(ladmin.username)
        self.admin_edit_password.setText('')
        self.show()

    def edit_admin(self):
        self.admin_edit_error.setStyleSheet('color: green')
        self.admin_edit_error.setText('')
        admin_id = str(self.admin_edit_id.text())
        admin_id = int(admin_id) if admin_id.isdigit() else 0
        ladmin = Admin.by_id(admin_id)
        if not admin:
            main_window.admin_not_found()
            self.close()
            return
        ladmin.password = unicode(self.admin_edit_password.text())
        a = ladmin.update()
        if type(a) in [str, QtCore.QString]:
            self.admin_edit_error.setStyleSheet('color: red')
            self.admin_edit_error.setText(a)
            return
        self.admin_edit_error.setStyleSheet('color: green')
        self.admin_edit_error.setText(self.tr('Your changes has been saved.'))
        main_window.update_admin_tab()

    def delete_confirm(self):
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(self.tr("WARNING!"))
        msg.setIcon(QtGui.QMessageBox.Question)
        msg.setText(self.tr("Are you sure you want to delete this admin ?"))
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        return msg.exec_()

    def delete_done(self):
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(self.tr("DONE!"))
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(self.tr("Admin deleted successfully!"))
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


class MemberWindow(QtGui.QMainWindow, memberedit.Ui_MemberEdit):
    def __init__(self, parent=None):
        super(MemberWindow, self).__init__(parent)
        self.setupUi(self)
        # bind buttons action ##########
        self.borrow_book_btn.clicked.connect(self.borrow_book)
        self.member_edit_cancel_btn.clicked.connect(self.close)
        self.member_edit_btn.clicked.connect(self.edit_member)
        self.member_delete_btn.clicked.connect(self.delete_member)

        self.member_edit_id.returnPressed.connect(self.member_edit_btn.click)
        self.member_edit_name.returnPressed.connect(self.member_edit_btn.click)
        self.member_edit_email.returnPressed.connect(self.member_edit_btn.click)
        self.member_edit_mob.returnPressed.connect(self.member_edit_btn.click)
        self.member_edit_fine.returnPressed.connect(self.member_edit_btn.click)

    def borrow_book(self):
        member_id = self.member_edit_id.text()
        main_window.nav_list.setCurrentRow(3)
        main_window.borrows_tabs.setCurrentIndex(1)
        main_window.borrow_add_member_id.setText(member_id)
        main_window.borrow_add_member_id_changed()
        self.close()

    def view_member(self, member):
        self.member_edit_error.setStyleSheet('color: red')
        self.member_edit_error.setText('')
        self.member_edit_id.setText(str(member.id))
        self.member_edit_name.setText(member.name)
        self.member_edit_email.setText(member.email or '')
        self.member_edit_mob.setText(member.mob or '')
        self.member_edit_fine.setText(member.fine or '')
        self.member_edit_note.document().setPlainText(member.note or '')
        self.show()

    def edit_member(self):
        self.member_edit_error.setStyleSheet('color: red')
        self.member_edit_error.setText('')
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
        note = unicode(self.member_edit_note.toPlainText())
        m = member.update(name=name, email=email, mob=mob, fine=fine, note=note)
        if type(m) in [str, QtCore.QString]:
            self.member_edit_error.setStyleSheet('color: red')
            self.member_edit_error.setText(m)
            return
        self.member_edit_error.setStyleSheet('color: green')
        self.member_edit_error.setText(self.tr('Your changes has been saved.'))
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


class BookWindow(QtGui.QMainWindow, bookedit.Ui_BookEdit):
    def __init__(self, parent=None):
        super(BookWindow, self).__init__(parent)
        self.setupUi(self)
        # bind buttons action ##########
        self.borrow_book_btn.clicked.connect(self.borrow_book)
        self.book_edit_cancel_btn.clicked.connect(self.close)
        self.book_edit_btn.clicked.connect(self.edit_book)
        self.book_delete_btn.clicked.connect(self.delete_book)

        self.book_edit_id.returnPressed.connect(self.book_edit_btn.click)
        self.book_edit_title.returnPressed.connect(self.book_edit_btn.click)
        self.book_edit_author.returnPressed.connect(self.book_edit_btn.click)
        self.book_edit_cat_id.returnPressed.connect(self.book_edit_btn.click)
        self.book_edit_cat_custom_id.returnPressed.connect(self.book_edit_btn.click)
        self.book_edit_cat_order.returnPressed.connect(self.book_edit_btn.click)
        self.book_edit_copies.returnPressed.connect(self.book_edit_btn.click)

        self.book_edit_cat_name.currentIndexChanged.connect(self.book_edit_cat_name_changed)

    def book_edit_cat_name_changed(self):
        cat_index = self.book_edit_cat_name.currentIndex()
        if cat_index <= 0:
            cat_id = ''
            cat_custom_id = ''
        else:
            cat_index -= 1
            cat_id = main_window.books_cats[cat_index]['id']
            cat_custom_id = main_window.books_cats[cat_index]['custom_id']
        self.book_edit_cat_id.setText(unicode(cat_id))
        self.book_edit_cat_custom_id.setText(cat_custom_id)

    def borrow_book(self):
        book_id = self.book_edit_id.text()
        main_window.nav_list.setCurrentRow(3)
        main_window.borrows_tabs.setCurrentIndex(1)
        main_window.borrow_add_book_id.setText(book_id)
        main_window.borrow_add_book_id_changed()
        self.close()

    def view_book(self, book):
        self.book_edit_error.setStyleSheet('color: red')
        self.book_edit_error.setText('')
        self.book_edit_cat_name.clear()
        cat_names = ['None']
        cat_names += [cat['name'] for cat in main_window.books_cats]
        self.book_edit_cat_name.addItems(cat_names)
        self.book_edit_id.setText(str(book.id))
        self.book_edit_title.setText(book.title)
        self.book_edit_author.setText(book.author or '')
        self.book_edit_cat_id.setText(str(book.cat_id) or '')
        if book.cat_name:
            self.book_edit_cat_name.setCurrentIndex(cat_names.index(book.cat_name))
        else:
            self.book_edit_cat_name.setCurrentIndex(0)
        self.book_edit_cat_custom_id.setText(book.cat_custom_id or '')
        self.book_edit_cat_order.setText(str(book.cat_order) or '')
        self.book_edit_state.setPlainText(book.state or '')
        self.book_edit_copies.setText(str(book.copies))
        available = QtCore.Qt.Checked if book.available else QtCore.Qt.Unchecked
        self.book_edit_available.setCheckState(available)
        self.show()

    def edit_book(self):
        self.book_edit_error.setStyleSheet('color: red')
        self.book_edit_error.setText('')
        book_id = str(self.book_edit_id.text())
        book_id = int(book_id) if book_id.isdigit() else 0
        book = Book.by_id(book_id)
        if not book:
            main_window.book_not_found()
            self.close()
            return
        title = unicode(self.book_edit_title.text())
        author = unicode(self.book_edit_author.text())
        cat_id = unicode(self.book_edit_cat_id.text())
        cat_id = int(cat_id) if cat_id.isdigit() else 0
        cat_order = unicode(self.book_edit_cat_order.text())
        cat_order = int(cat_order) if cat_order.isdigit() else 0
        state = unicode(self.book_edit_state.toPlainText())
        copies = str(self.book_edit_copies.text())
        copies = int(copies) if copies.isdigit() else ''
        available = self.book_edit_available.isChecked()
        b = book.update(title=title, author=author,
                        cat_id=cat_id, cat_order=cat_order, state=state,
                        copies=copies, available=available)
        if type(b) in [str, QtCore.QString]:
            self.book_edit_error.setStyleSheet('color: red')
            self.book_edit_error.setText(b)
            return
        self.book_edit_error.setStyleSheet('color: green')
        self.book_edit_error.setText(self.tr('Your changes has been saved.'))
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


class CatWindow(QtGui.QMainWindow, catedit.Ui_CatEdit):

    def __init__(self, parent=None, main_window=None):
        super(CatWindow, self).__init__(parent)
        self.setupUi(self)
        # bind buttons action ##########
        self.cat_edit_cancel_btn.clicked.connect(self.close)
        self.cat_edit_btn.clicked.connect(self.edit_cat)
        self.cat_delete_btn.clicked.connect(self.delete_cat)

        self.cat_edit_id.returnPressed.connect(self.cat_edit_btn.click)
        self.cat_edit_name.returnPressed.connect(self.cat_edit_btn.click)
        self.cat_edit_custom_id.returnPressed.connect(self.cat_edit_btn.click)

    def view_cat(self, lcat):
        self.cat_edit_error.setStyleSheet('color: red')
        self.cat_edit_error.setText('')
        self.cat_edit_id.setText(str(lcat.id))
        self.cat_edit_name.setText(lcat.name)
        self.cat_edit_custom_id.setText(lcat.custom_id or '')
        self.show()

    def edit_cat(self):
        self.cat_edit_error.setStyleSheet('color: red')
        self.cat_edit_error.setText('')
        cat_id = str(self.cat_edit_id.text())
        cat_id = int(cat_id) if cat_id.isdigit() else 0
        name = unicode(self.cat_edit_name.text())
        custom_id = unicode(self.cat_edit_custom_id.text())
        cat = Cat.by_id(cat_id)
        if not cat:
            main_window.cat_not_found()
            self.close()
            return
        self.cat_edit_error.setStyleSheet('color: green')
        self.cat_edit_error.setText(self.tr('saving ....'))
        c = cat.update(name=name, custom_id=custom_id)
        if type(c) in [str, QtCore.QString]:
            self.cat_edit_error.setStyleSheet('color: red')
            self.cat_edit_error.setText(c)
            return
        self.cat_edit_error.setStyleSheet('color: green')
        self.cat_edit_error.setText(self.tr('Your changes has been saved.'))
        main_window.update_cats_tab()
        main_window.update_books_tab()

    def delete_confirm(self):
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(self.tr("WARNING!"))
        msg.setIcon(QtGui.QMessageBox.Question)
        msg.setText(self.tr("Are you sure you want to delete this category ?"))
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        return msg.exec_()

    def delete_done(self):
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(self.tr("DONE!"))
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(self.tr("Category deleted successfully!"))
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        return msg.exec_()

    def delete_cat(self):
        do_delete = self.delete_confirm() == 16384
        cat_id = str(self.cat_edit_id.text())
        cat_id = int(cat_id) if cat_id.isdigit() else 0
        if do_delete:
            Cat.delete(cat_id)
            self.delete_done
            main_window.update_cats_tab()
            self.close()


class BorrowWindow(QtGui.QMainWindow, borrowedit.Ui_BorrowEdit):
    def __init__(self, parent=None):
        super(BorrowWindow, self).__init__(parent)
        self.setupUi(self)
        # bind buttons action ##########
        self.borrow_edit_cancel_btn.clicked.connect(self.close)
        self.borrow_edit_btn.clicked.connect(self.edit_borrow)
        self.borrow_delete_btn.clicked.connect(self.delete_borrow)

        self.borrow_edit_id.returnPressed.connect(self.borrow_edit_btn.click)
        self.borrow_edit_book_id.returnPressed.connect(self.borrow_edit_btn.click)
        self.borrow_edit_member_id.returnPressed.connect(self.borrow_edit_btn.click)

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
        self.borrow_edit_error.setStyleSheet('color: red')
        self.borrow_edit_error.setText('')
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
        if main_window.admin:
            updated_by = '{}({})'.format(main_window.admin.id, main_window.admin.username)
        else:
            updated_by = ''
        b = borrow.update(book_id=book_id, member_id=member_id,
                          start=start, end=end, active=active,
                          updated_by=updated_by)
        if type(b) in [str, QtCore.QString]:
            self.borrow_edit_error.setStyleSheet('color: red')
            self.borrow_edit_error.setText(b)
            return
        self.borrow_edit_error.setStyleSheet('color: green')
        self.borrow_edit_error.setText(self.tr('Your changes has been saved.'))
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


class BackupThread(QtCore.QThread):

    def run(self):
        backup_window.cloud_backup()


class BackupRunnable(QtCore.QRunnable):

    def run(self):
        app = QtCore.QCoreApplication.instance()
        backup_window.cloud_backup()
        app.quit()


class BackupWindow(QtGui.QMainWindow, backupgui.Ui_MainWindow):

    def __init__(self, parent=None):
        super(BackupWindow, self).__init__(parent)
        self.setupUi(self)
        self.log_viewer.clear()
        self.cancel_btn.clicked.connect(self.close)

    def write(self, msg):
        self.log_viewer.appendPlainText(msg)

    def start(self):
        self.show()
        self.write(self.tr('starting cloud backup ....'))
        """
        thread = BackupThread()
        thread.finished.connect(self.finish)
        thread.start()
        """
        runnable = BackupRunnable()
        QtCore.QThreadPool.globalInstance().start(runnable)

    def finish(self):
        self.write(self.tr('cloud backup finished'))
        self.write(self.tr('you can close the window now'))

    def cloud_backup(self):
        logging.info('starting cloud backup ....')
        files = self.create_backup_files()
        files = []
        print "uploading files"
        for f in files:
            try:
                gdrive.upload_file(f['file_path'], title=f['title'])
            except Exception as e:
                logging.error(e)
        logging.info('cloud backup finished')

    def create_backup_files(self):
        files = []
        if BACKUP_DB_FILE:
            db_file = {"file_path": DB_PATH}
            db_file["title"] = '{}_db_backup_{}.mexdb'.format(APP_TITLE, datetime.datetime.now().date())
            files.append(db_file)
        if BACKUP_CSV_FILES:
            export_dir = os.path.join(MAIN_DIR, 'Backup')
            db_tables = [Member, Book, Borrow, Admin]
            file_names = ['Members_{}.csv', 'Books_{}.csv', 'Borrows_{}.csv', 'Admins_{}.csv']
            file_names = [x.format(datetime.datetime.now().date())
                          for x in file_names]
            for n in range(len(db_tables)):
                records = db_tables[n].get()
                file_path = os.path.join(export_dir, file_names[n])
                files.append({"file_path": file_path, "title": file_names[n]})
                with open(file_path, 'wb') as outfile:
                    outcsv = UnicodeWriter(
                        outfile, delimiter=',', quoting=csv.QUOTE_ALL)
                    outcsv.writerow(
                        [column.name for column in db_tables[n].__mapper__.columns]
                    )
                    for curr in records:
                        row = []
                        for column in db_tables[n].__mapper__.columns:
                            item = getattr(curr, column.name)
                            if isinstance(item, datetime.datetime):
                                item = item.strftime('%d-%m-%Y %I:%M:%S %p')
                            row.append(unicode(item))
                        outcsv.writerow(row)
        return files


class CronThread(threading.Thread):

    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        Borrow.calc_fines()
        main_window.update_members_tab()


def check_first_time_run():
    try:
        admins = Admin.get(n=1)
        if not admins:
            Admin.add('admin', 'admin', BASE_ADMIN_ROLES)
    except Exception as e:
        logging.error(e)


def config_locale(locale=LOCALE):
    if locale == 'Arabic':
        layout_direction = QtCore.Qt.RightToLeft
        trans_file = 'ar.qm'
        # translator for built-in qt strings
        translator = QtCore.QTranslator(app)
        translator.load(os.path.join(TRANS_DIR, 'qt_ar.qm'))
        app.installTranslator(translator)
    elif locale == 'English':
        layout_direction = QtCore.Qt.LeftToRight
        trans_file = 'en.qm'
    else:
        layout_direction = default_layout_direction
        trans_file = default_trans_file
    trans_file_path = os.path.join(TRANS_DIR, trans_file)
    # install my specific translations
    translator = QtCore.QTranslator(app)
    translator.load(trans_file_path)
    app.installTranslator(translator)
    return layout_direction


def config_layout(layout_direction=QtCore.Qt.LeftToRight):
    for window in app_windows:
        try:
            window.setLayoutDirection(layout_direction)
            # window.set_layout_direction(layout_direction)
            widgets = window.findChildren(QtGui.QWidget)
            for w in widgets:
                w.setLayoutDirection(layout_direction)
        except Exception as e:
            logging.error(e)


def config_style(style=STYLE):
    if style not in style_options:
        return
    style_data = stylesheets[STYLE]
    # load stylesheet file
    style_sheet = ''
    style_file_path = os.path.join(STYLE_DIR, style_data['file'])
    with open(style_file_path, 'r') as style_file:
        style_sheet = style_file.read()
    # load rc file if exists
    rc_file = style_data['rc']
    if rc_file:
        rc_file_path = os.path.join(STYLE_DIR, rc_file)
        imp.load_source('style_rc', rc_file_path)
    for window in app_windows:
        window.setStyleSheet(style_sheet)


def create_detailed_full_roles():
    base_roles = [{'view': True, 'edit': True}, {}]
    base_widgets = (QtGui.QStackedWidget, QtGui.QTabWidget)
    # permissions for entire app
    roles = list(base_roles)
    windows_roles = {}
    for window in main_app_windows:
        window_roles = list(base_roles)
        window_name = str(window.objectName())
        # print window_name
        # stacked widgets
        satcked_widgets = window.findChildren(base_widgets, QtCore.QRegExp(r'.*_tabs'))
        widgets_roles = {}
        for widget in satcked_widgets:
            widget_roles = list(base_roles)
            widget_name = str(widget.objectName())
            pages = [widget.widget(n) for n in range(widget.count())]
            pages_roles = {}
            for page in pages:
                page_roles = list(base_roles)
                page_name = str(page.objectName())
                pages_roles[page_name] = page_roles
            widget_roles[1] = pages_roles
            widgets_roles[widget_name] = widget_roles
        window_roles[1] = widgets_roles
        windows_roles[window_name] = window_roles
    roles[1] = windows_roles
    return roles


def create_full_roles_list():
    windows = main_app_windows
    return ['{}>{}>{}>{}'.format(win.objectName(),
                                 wid.objectName(),
                                 pag.objectName(),
                                 # twd.objectName(),
                                 tab.objectName())
            for win in windows
            for wid in win.findChildren(QtGui.QStackedWidget)
            for pag in [wid.widget(n) for n in range(wid.count())]
            for twd in pag.findChildren(QtGui.QTabWidget)
            for tab in [twd.widget(n) for n in range(twd.count())]]
    """
    roles = []
    for window in main_app_windows:
        window_name = str(window.objectName())
        # print window_name
        # stacked widgets
        satcked_widgets = window.findChildren(QtGui.QStackedWidget, QtCore.QRegExp(r'.*_tabs'))
        for widget in satcked_widgets:
            widget_name = str(widget.objectName())
            pages = [widget.widget(n) for n in range(widget.count())]
            for page in pages:
                page_name = str(page.objectName())
                tab_widgets = page.findChildren(QtGui.QTabWidget, QtCore.QRegExp('.*_tabs'))
                for tab_widget in tab_widgets:
                    tab_widget_name = str(tab_widget.objectName())
                    tabs = [tab_widget.widget(n) for n in range(tab_widget.count())]
                    for tab in tabs:
                        tab_name = str(tab.objectName())
                        roles.append('{}>>{}>>{}>>{}>>{}'.format(window_name,
                                                                 widget_name,
                                                                 page_name,
                                                                 tab_widget_name,
                                                                 tab_name))
                if not tab_widgets:
                    roles.append('{}>>{}>>{}'.format(window_name,
                                                     widget_name,
                                                     page_name))
    return roles
    """


def config_admin_roles(dev=True):
    global admin_roles, BASE_ADMIN_ROLES
    if dev:  # update base roles while devleping the app
        BASE_ADMIN_ROLES = create_full_roles_list()
        config.update_admin_roles(BASE_ADMIN_ROLES)
    admin_roles = BASE_ADMIN_ROLES  # will be changed if admin login


def tests():
    """
    from db import excel_import
    excel_import.run()
    """
    main_window.cloud_backup()
    sys.exit()


if __name__ == '__main__':
    init_db()
    # tests()
    admin = None
    admin_roles = None
    check_first_time_run()
    app = QtGui.QApplication(sys.argv)
    layout_direction = config_locale(locale=LOCALE)
    login_window = LoginWindwo()
    main_window = MainWindow()
    # tests()
    admin_window = AdminWindow()
    member_window = MemberWindow()
    book_window = BookWindow()
    cat_window = CatWindow()
    borrow_window = BorrowWindow()
    backup_window = BackupWindow()
    # tests()
    # config logging
    main_window.config_logging()
    # cron jobs
    CronThread('mex-cron').start()
    # config style and locale
    app_windows = [login_window, main_window,
                   admin_window, member_window,
                   book_window, cat_window, borrow_window,
                   backup_window]
    # config admin roles
    main_app_windows = [main_window, admin_window,
                        member_window, book_window,
                        cat_window, borrow_window,
                        backup_window]
    # config_admin_roles(dev=True)
    config_layout(layout_direction=layout_direction)
    config_style(style=STYLE)
    # view app
    if REQ_ADMIN_LOGIN:
        login_window.show()
    else:
        main_window.initialize()
        main_window.show()
    end = app.exec_()
    if BACKUP_ON_EXIT:
        main_window.cloud_backup()
    sys.exit(end)
