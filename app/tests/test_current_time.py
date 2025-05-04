from datetime import datetime
from app.utils.current_time import get_current_time_str


def test_get_current_time_str():
    result = get_current_time_str()
    assert datetime.fromisoformat(result)
