import logging
import dearpygui.dearpygui as dpg
from assets.modules.funcs import is_dir_valid
from settings import update_settings

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s | %(levelname)s]: %(message)s')


def select_hoi4_dir_callback(_: str, data: dict):
    path = data['file_path_name'].replace('\\', '/')
    if not is_dir_valid(requirements=['hoi4.exe', 'common', 'gfx', 'localization'], path=path):
        logging.error('Is not a valid hoi4 dir')

    update_settings('hoi4_path', path)
    dpg.set_value('hoi4_path_input_field', path)


def select_mod_dir_callback(_: str, data: dict):
    path = data['file_path_name'].replace('\\', '/')

    update_settings('mod_path', path)
    dpg.set_value('mod_path_input_field', path)
