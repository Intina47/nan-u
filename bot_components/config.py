# path: config.py
import yaml

def load_config():
    with open('./config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config