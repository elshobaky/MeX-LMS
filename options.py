import os, sys, logging, json


# configuring logging
def config_logging():
	root = logging.getLogger()
	root.setLevel(logging.DEBUG)

	ch = logging.StreamHandler(sys.stdout)
	ch.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	ch.setFormatter(formatter)
	root.addHandler(ch)

# static directory
MAIN_DIR  = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(MAIN_DIR, 'mexlms.db')
DOC_DIR = os.path.expanduser('~/Documents/MeX LMS')
BACKUP_DIR = os.path.expanduser('~/Documents/MeX LMS/Backups')
EXPORT_DIR = os.path.expanduser('~/Documents/MeX LMS/Exports')

with open('options.json', 'r') as options:
	options = json.loads(options.read())
	FINE = options['fine']

try:
	os.mkdir(DOC_DIR)
	os.mkdir(BACKUP_DIR)
	os.mkdir(EXPORT_DIR)
except Exception as e:
	logging.error(e)
