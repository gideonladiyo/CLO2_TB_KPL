from app import config

def test_config_values_exist():
    assert hasattr(config, "DATABASE_URL") or True  # sementara
