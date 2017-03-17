import os
import json

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(MAIN_DIR, 'drive_config.json')


class Config():
    def __init__(self):
        with open(config_file, 'r') as config:
            self.config = json.loads(config.read())
        self.folder_name = self.config['folder_name']
        self.folder_id = self.config['folder_id']

    def update(self, folder_name=None, folder_id=None):
        if folder_name:
            self.folder_name = self.config['folder_name'] = folder_name
        if folder_id:
            self.folder_id = self.config['folder_id'] = folder_id
        with open(config_file, 'w') as config:
            config.write(json.dumps(self.config))
        return self


config = Config()
FOLDER_NAME = config.folder_name
FOLDER_ID = config.folder_id
