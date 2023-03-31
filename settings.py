from json import load, dump
from os.path import exists
import logging

# configure logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s | %(levelname)s]: %(message)s')

# if user-settings is not exist, create an empty one
if not exists('settings.json'):
    with open('settings.json', 'w') as file:
        file.write('{"hoi4_path": "", "mod_path": ""}')

#

MODULES = ['modules.cosmetic_tag']
SETTINGS = load(open('settings.json'))

#


def update_settings(param: str, value: str):
    SETTINGS[param] = value
    dump(SETTINGS, open('settings.json', 'w'))
