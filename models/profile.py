from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class Profile:
    name: str
    proxy_settings: Dict[str, str]
    fingerprint_data: Dict[str, Any] = field(default_factory=lambda: {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'viewport': {'width': 1920, 'height': 1080},
        'locale': 'en-US',
        'timezone': 'America/New_York',
        'geolocation': {'latitude': 40.7128, 'longitude': -74.0060},
        'permissions': ['geolocation']
    })