import re
from datetime import datetime
from typing import Optional


def format_date(timestamp: float) -> str:
    dt = datetime.utcfromtimestamp(timestamp)
    return dt.isoformat() + "Z"


def parse_date(date_string: str) -> Optional[float]:
    try:
        dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return dt.timestamp()
    except ValueError:
        return None


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def sanitize_input(text: str) -> str:
    dangerous_chars = ["<", ">", '"', "'", "&"]
    result = text
    for char in dangerous_chars:
        result = result.replace(char, "")
    return result


def truncate_string(text: str, max_length: int) -> str:
    return text[:max_length] if len(text) > max_length else text


def is_valid_username(username: str) -> bool:
    if not username or len(username) < 3 or len(username) > 20:
        return False
    return username.replace("_", "").replace("-", "").isalnum()
