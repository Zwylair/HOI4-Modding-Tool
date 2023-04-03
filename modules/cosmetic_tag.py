import logging
import random
import shutil
from os.path import exists
from os import mkdir
import dearpygui.dearpygui as dpg
import settings

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s | %(levelname)s]: %(message)s')
colour_template = '<cosmetic tag> = {\n' \
                  '    color = rgb { <colour> }\n' \
                  '    color_ui = rgb { <colour> }\n' \
                  '}'
localization_template = '''
 <cosmetic tag>_democratic:0 "<name of the country>"
 <cosmetic tag>_democratic_ADJ:0 "<adjective name of the country>"
 <cosmetic tag>_democratic_DEF:0 "<name of the country which will be used in events>"
 <cosmetic tag>_fascism:0 "<name of the country>"
 <cosmetic tag>_fascism_ADJ:0 "<adjective name of the country>"
 <cosmetic tag>_fascism_DEF:0 "<name of the country which will be used in events>"
 <cosmetic tag>_neutrality:0 "<name of the country>"
 <cosmetic tag>_neutrality_ADJ:0 "<adjective name of the country>"
 <cosmetic tag>_neutrality_DEF:0 "<name of the country which will be used in events>"
 <cosmetic tag>_communism:0 "<name of the country>"
 <cosmetic tag>_communism_ADJ:0 "<adjective name of the country>"
 <cosmetic tag>_communism_DEF:0 "<name of the country which will be used in events>"
'''

#


def flags_dir_selector_callback(_, data: dict):
    dpg.set_value('folder_with_cosmetic_flags', data['file_path_name'])


#

with dpg.value_registry():
    dpg.add_string_value(tag='cosmetic_tag')
    dpg.add_string_value(tag='folder_with_cosmetic_flags')
    dpg.add_string_value(tag='country_name')
    dpg.add_string_value(tag='adj_country_name')
    dpg.add_string_value(tag='events_country_name')
    dpg.add_color_value(default_value=[random.randint(64, 191), random.randint(64, 191), random.randint(64, 191)], tag='colour_value')
    dpg.add_bool_value(default_value=True, tag='replace_flags_on_conflicts')

dpg.add_file_dialog(directory_selector=True, show=False, callback=flags_dir_selector_callback, tag='flags_dir_browser', width=400, height=300)

#


def flags_help_window():
    dpg.delete_item('flag_help_window')
    
    with dpg.window(label='How to create a flags', tag='flag_help_window', width=384, height=236, no_resize=True, no_collapse=True):
        dpg.add_text('Flags in HOI4 have 3 types: big (82x52), medium (41x26) and small\n(10x7)\n\n'
                     'How to create flags:\n'
                     '  1. Convert your flag-image into 3 copies in resolutions above\n'
                     '  2. Convert your images into .tga format\n'
                     '  3. If it necessary name your flags in all ideologies. For ex: (ABK_fasc\nism.tga, ABK_democratic.tga ...)\n'
                     '  4. Move your flags medium and small flag into relevant folders')


def cosmetic_tags_help_window():
    dpg.delete_item('cosmetic_tags_help_window')

    with dpg.window(label='How to create a cosmetic tag', tag='cosmetic_tags_help_window', width=384, height=236, no_resize=True, no_collapse=True):
        dpg.add_text('You can come up with a cosmetic tag using these rules:\n\n'
                     '  1. You can use more than 3 symbols\n'
                     '  2. You still should not use a space (" ") in the tags')


def done_window():
    dpg.delete_item('done_window')
    
    with dpg.window(label='Done!', tag='done_window', width=240, height=100, no_resize=True, no_collapse=True):
        dpg.add_text('Cosmetic tag successfully created!')


def create_cosmetic_tag():
    mod_dir = settings.SETTINGS['mod_path']

    cosmetic_tag: str = dpg.get_value('cosmetic_tag')
    cosmetic_flags_path: str = dpg.get_value('folder_with_cosmetic_flags')
    country_name: str = dpg.get_value('country_name')
    adj_country_name: str = dpg.get_value('adj_country_name')
    events_country_name: str = dpg.get_value('events_country_name')
    colour_value: list[str, str, str] = [f'{round(i)}' for i in dpg.get_value('colour_value')][:3]
    replace_flags_on_conflicts: bool = dpg.get_value('replace_flags_on_conflicts')

    changed_localization = localization_template
    for k, new_k in zip(['<cosmetic tag>', '<name of the country>', '<adjective name of the country>', '<name of the country which will be used in events>'],
                        [cosmetic_tag, country_name, adj_country_name, events_country_name]):
        changed_localization = changed_localization.replace(k, new_k)

    changed_colour_template = colour_template
    for k, new_k in zip(['<cosmetic tag>', '<colour>'],
                        [cosmetic_tag, ' '.join(colour_value)]):
        changed_colour_template = changed_colour_template.replace(k, new_k)

    # Creating folders
    for i in ['gfx', 'gfx/flags', 'gfx/flags/medium', 'gfx/flags/small', 'localization', 'localization/english', 'common', 'common/countries']:
        if not exists(f'{mod_dir}/{i}'):
            mkdir(f'{mod_dir}/{i}')

    # Copying flags
    shutil.copytree(cosmetic_flags_path, f'{mod_dir}/gfx/flags', dirs_exist_ok=replace_flags_on_conflicts)

    # Modifying localization file
    if not exists(f'{mod_dir}/localization/english/cosmetic_country_tags.yml'):
        entry = 'l_english:'
    else:
        with open(f'{mod_dir}/localization/english/cosmetic_country_tags.yml') as file:
            entry = file.read()

    with open(f'{mod_dir}/localization/english/cosmetic_country_tags.yml', 'w') as file:
        entry = f'{entry}\n{changed_localization}'
        file.write(entry)
    
    # Modifying colours
    entry = ''
    if exists(f'{mod_dir}/common/countries/cosmetic_tags.txt'):
        with open(f'{mod_dir}/common/countries/cosmetic_tags.txt') as file:
            entry = file.read()

    with open(f'{mod_dir}/common/countries/cosmetic_tags.txt', 'w') as file:
        file.write(f'{entry}\n{changed_colour_template}')

    done_window()


def cosmetic_tag_window():
    dpg.delete_item('cosmetic_tag_window')

    with dpg.window(label='Create a new cosmetic tag', tag='cosmetic_tag_window', width=510, height=336, no_resize=True, no_collapse=True):
        with dpg.group(horizontal=True):
            dpg.add_input_text(label='New cosmetic tag', source='cosmetic_tag', parent='cosmetic_tag_div', width=100)
            dpg.add_button(label='Help', parent='cosmetic_tag_div', callback=cosmetic_tags_help_window)

        dpg.add_separator()

        with dpg.group(horizontal=True):
            dpg.add_input_text(label='Flags folder path', tag='flags_folder_path_input_field', source='folder_with_cosmetic_flags', width=250)
            dpg.add_button(label='Select', callback=lambda: dpg.show_item('flags_dir_browser'))
            dpg.add_button(label='Help', callback=flags_help_window)
        dpg.add_checkbox(label='Replace flags on conflicts', source='replace_flags_on_conflicts')

        dpg.add_separator()

        dpg.add_color_picker(label='Colour of country on the map', no_alpha=True, source='colour_value', width=200)

        dpg.add_separator()

        dpg.add_input_text(label='Default name of the country', source='country_name', width=200)
        dpg.add_input_text(label='Adjective name of the country', source='adj_country_name', width=200)
        dpg.add_input_text(label='Name of the country, which will be used in events', source='events_country_name', width=200)

        dpg.add_separator()

        dpg.add_text('Info: country names will be duplicated in all 4 vanilla ideologies. Country localization\n'
                     'will be added only on applied language (localization/english/cosmetic_country_tags.yml).\n'
                     'File will be created if it does not exist || will be supplemented if exists')
        dpg.add_button(label='Submit', callback=create_cosmetic_tag)


dpg.add_button(label='Create cosmetic tag', callback=cosmetic_tag_window)
