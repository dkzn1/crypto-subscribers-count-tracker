import random
from typing import Dict, Any
from .headers_config import referers, viewports


def create_pw_headers() -> Dict[str, Any]:
    headers: Dict[str, Any] = {
        "extra_http_headers": {"referer": random.choice(referers)},
        "viewport": random.choice(viewports),
        "bypass_csp": True,
        "permissions": ["geolocation"],
    }

    return headers
