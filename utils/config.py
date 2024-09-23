import json
import os

from models.profile import Profile

CONFIG_FILE = 'config.json'

def save_profiles(profiles):
    with open(CONFIG_FILE, 'w') as f:
        json.dump([profile.__dict__ for profile in profiles], f)

def load_profiles():
    if not os.path.exists(CONFIG_FILE):
        return []
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
    return [Profile(**profile_data) for profile_data in data]