from datetime import datetime, timezone

def get_current_time_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")