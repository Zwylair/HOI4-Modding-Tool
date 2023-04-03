import logging
import dearpygui.dearpygui as dpg
import settings

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s | %(levelname)s]: %(message)s')


def open_settings_window():
    dpg.delete_item('settings_window')
    hoi4_text_field_value = settings.SETTINGS['hoi4_path']
    mod_text_field_value = settings.SETTINGS['mod_path']

    with dpg.window(label='Settings', tag='settings_window', width=384, height=236, no_resize=True, no_collapse=True):
        dpg.add_text(default_value='HOI4 folder')
        dpg.add_input_text(tag='hoi4_path_input_field', default_value=hoi4_text_field_value, readonly=True)
        dpg.add_button(label='Select', pos=[270, 52], callback=lambda: dpg.show_item('hoi4_dir_picker_file_dialog'))
        dpg.add_separator()
        dpg.add_text(default_value='Mod folder')
        dpg.add_input_text(tag='mod_path_input_field', default_value=mod_text_field_value, readonly=True)
        dpg.add_button(label='Select', pos=[270, 104], callback=lambda: dpg.show_item('mod_dir_picker_file_dialog'))
