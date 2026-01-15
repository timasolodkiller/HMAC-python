"""Функции помощники."""
import os


def get_config_path(file_name):
    """Функция, достающая путь до конфига."""
    script_dir = os.path.dirname(os.path.abspath(file_name))
    project_root = os.path.dirname(script_dir)
    config_path = os.path.join(project_root, 'config.json')
    return config_path
