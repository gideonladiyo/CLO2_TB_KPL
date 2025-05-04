import os
from app.config import settings

def test_settings_from_env():
    assert settings.app_name == "Simple Ordering System"
    assert settings.app_version == "v1.0.0"
    assert settings.debug is True
    assert settings.max_orders_per_day == 50
    assert settings.maintenance_mode is False

def test_settings_types():
    assert isinstance(settings.app_name, str)
    assert isinstance(settings.app_version, str)
    assert isinstance(settings.debug, bool)
    assert isinstance(settings.max_orders_per_day, int)
    assert isinstance(settings.maintenance_mode, bool)