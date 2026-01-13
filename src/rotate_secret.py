"""Утилита для ротации секрета."""

import base64
import json
import os
import secrets


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config.json')


def generate_secret(length: int = 32) -> str:
    """Генерирует случайный секрет в формате base64."""
    random_bytes = secrets.token_bytes(length)
    return base64.b64encode(random_bytes).decode('ascii')


def rotate_secret():
    """Обновляет секрет в конфигурационном файле."""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    new_secret = generate_secret()
    config['secret'] = new_secret
    
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print('Секрет успешно обновлён!')
    print(f'Новый секрет: {new_secret[:10]}...')

if __name__ == '__main__':
    rotate_secret()