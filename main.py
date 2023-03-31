import logging
import importlib
import dearpygui.dearpygui as dpg

import settings
from assets.parts.windows import open_settings_window
from assets.parts.file_dialog import select_hoi4_dir_callback, select_mod_dir_callback

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s | %(levelname)s]: %(message)s')

#

dpg.create_context()
dpg.create_viewport(title='HoI4 Modding Tool (1.12.x)', small_icon='assets/icon.ico', width=700, height=600, resizable=False)

dpg.add_file_dialog(directory_selector=True, show=False, callback=select_hoi4_dir_callback, tag='hoi4_dir_picker_file_dialog', width=400, height=300)
dpg.add_file_dialog(directory_selector=True, show=False, callback=select_mod_dir_callback, tag='mod_dir_picker_file_dialog', width=400, height=300)

with dpg.font_registry():
    with dpg.font('assets/ubuntu_regular.ttf', 14, default_font=True, id='Default font'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font('Default font')

#

with dpg.window(width=694, height=611, no_title_bar=True, no_resize=True, no_close=True, no_move=True):
    # importing modules (modules/cosmetic_tag.py; modules/country_creator.py; ...)
    for module in settings.MODULES:
        try:
            imported_module = importlib.import_module(module)
        except ImportError as err:
            logging.fatal(f'Critical error.\n\n{err}')

    dpg.add_button(label='Settings', pos=[2, 538], callback=open_settings_window)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
