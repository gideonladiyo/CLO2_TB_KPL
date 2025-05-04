from app.utils.current_time import get_current_time_str

def test_get_current_time_format():
    result = get_current_time_str()
    assert isinstance(result, str)
    assert "-" in result and ":" in result
