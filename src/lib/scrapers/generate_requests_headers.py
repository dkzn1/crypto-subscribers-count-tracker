import random
from user_agent import generate_user_agent


def generate_requests_headers(referers):
    headers = {
        "User-Agent": generate_user_agent(),
        "Referer": random.choice(referers),
        "Accept-Language": "en-US,en;q=0.9",
    }

    return headers
