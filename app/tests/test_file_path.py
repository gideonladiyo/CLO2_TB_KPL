from app.utils.file_path import get_base_path

def test_get_base_path():
    result = get_base_path()
    assert isinstance(result, str)
    assert result.endswith("app") or "CLO2_TB_KPL" in result  # Uji asumsi umum
