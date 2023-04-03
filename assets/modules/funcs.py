from os.path import exists
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s | %(levelname)s]: %(message)s')


def is_dir_valid(requirements: list, path: str) -> bool:
    for req in requirements:
        if not exists(f'{path}/{req}'):
            logging.error('Does not match with requirements [funcs.py: for req in requirements)]')
            return False

    logging.debug(f'hoi4 dir selected: {path}')
    return True
