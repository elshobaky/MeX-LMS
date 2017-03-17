import os
import sys
import logging
import json


# internationalization
"""
to make .ts file use pylupdate4 :
    ex. pylupdate4 main.py -ts trans/ar.ts
to convert .ts to .qm use lrelease :
    ex. lrelease trans/ar.ts

"""
from PyQt4 import QtCore
translate = QtCore.QCoreApplication.translate

locale_options = ['Arabic', 'English']
default_layout_direction = QtCore.Qt.LeftToRight
default_trans_file = 'en.qm'

# stylesheets dic {'style name': 'style file'}
# if the style is not a single file or a separate lib like qdarkstyle
# replace the file name with a list containing the style as the first element
stylesheets = {'Default': {'file': 'default.stylesheet', 'rc': ''},
               'Dark Orange': {'file': 'darkorange.stylesheet', 'rc': 'darkorange_rc.py'},
               'Dark Green': {'file': 'darkgreen.stylesheet', 'rc': ''},
               'Dark Blue': {'file': 'darkblue.qss', 'rc': 'darkblue_rc.py'}}
style_options = ['Default', 'Dark Orange', 'Dark Green', 'Dark Blue']


class Config():
    def __init__(self):
        with open('config.json', 'r') as config:
            self.config = json.loads(config.read())
        self.project_name = self.config['project_name']
        self.app_title = self.config['app_title']
        self.req_admin_login = self.config['req_admin_login']
        self.base_admin_roles = self.config['base_admin_roles']
        self.locale = self.config['locale']
        self.style = self.config['style']
        self.fine = self.config['fine']
        self.borrow_period = self.config['borrow_period']
        self.backup_on_exit = self.config['backup_on_exit']
        self.backup_csv_files = self.config['backup_csv_files']
        self.backup_db_file = self.config['backup_db_file']

    def update(self, app_title=None, req_admin_login=None,
               locale=None, style=None,
               fine=None, borrow_period=None,
               backup_on_exit=None, backup_csv_files=None,
               backup_db_file=None):
        if app_title:
            self.app_title = self.config['app_title'] = app_title
        if req_admin_login is not None:
            self.req_admin_login = self.config['req_admin_login'] = req_admin_login
        if locale:
            if locale not in locale_options:
                return translate('config', 'invalid language')
            self.locale = self.config['locale'] = locale
        if style:
            if style not in style_options:
                return translate('config', 'invalidd style')
            self.style = self.config['style'] = style
        if fine is not None:
            if not isinstance(borrow_period, int):
                return translate('config', 'invalid borrow period')
            self.fine = self.config['fine'] = fine
        if borrow_period is not None:
            self.borrow_period = self.config['borrow_period'] = borrow_period
        if backup_on_exit is not None:
            self.backup_on_exit = self.config['backup_on_exit'] = backup_on_exit
        if backup_csv_files is not None:
            self.backup_csv_files = self.config['backup_csv_files'] = backup_csv_files
        if backup_db_file is not None:
            self.backup_db_file = self.config['backup_db_file'] = backup_db_file
        with open('config.json', 'w') as config:
            config.write(json.dumps(self.config))
        return self

    def update_admin_roles(self, roles=None):
        if not roles:
            return
        self.base_admin_roles = self.config['base_admin_roles'] = roles
        with open('config.json', 'w') as config:
            config.write(json.dumps(self.config))


config = Config()

PROJECT_NAME = config.project_name
APP_TITLE = config.app_title
REQ_ADMIN_LOGIN = config.req_admin_login
LOCALE = config.locale
STYLE = config.style
FINE = config.fine
BORROW_PERIOD = config.borrow_period
# Backup settings
BACKUP_ON_EXIT = config.backup_on_exit
BACKUP_CSV_FILES = config.backup_csv_files
BACKUP_DB_FILE = config.backup_db_file

# base admin roles
BASE_ADMIN_ROLES = config.base_admin_roles

# static directory
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(MAIN_DIR)

DB_PATH = os.path.join(MAIN_DIR, 'mex.db')
DOC_DIR = os.path.expanduser('~/Documents/{}'.format(PROJECT_NAME))
BACKUP_DIR = os.path.expanduser('~/Documents/{}/Backups'.format(PROJECT_NAME))
EXPORT_DIR = os.path.expanduser('~/Documents/{}/Exports'.format(PROJECT_NAME))
REP_TEMPL_DIR = os.path.join(MAIN_DIR, 'report_templates')
STYLE_DIR = os.path.join(os.path.join(MAIN_DIR, 'gui'), 'style')
TRANS_DIR = os.path.join(MAIN_DIR, 'trans')

try:
    os.mkdir(os.path.join(MAIN_DIR, 'Backup'))
except Exception as e:
    logging.error(e)
try:
    os.mkdir(DOC_DIR)
    os.mkdir(BACKUP_DIR)
    os.mkdir(EXPORT_DIR)
except OSError:
    pass
except Exception as e:
    logging.error(e)
