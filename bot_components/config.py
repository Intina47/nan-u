# path: config.py
import yaml

def load_config(channel_id):
    file_path = f'./config/config_{channel_id}.yaml'
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config