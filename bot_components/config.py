# path: bot_components/config.py
import yaml
import os

def load_config(channel_id):
    file_path = f'/app/config/config_{channel_id}.yaml'
    if not os.path.exists(file_path):
        print(f"Config file {file_path} does not exist")
        return None
    try:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Failed to load config from {file_path}: {e}")
        return None