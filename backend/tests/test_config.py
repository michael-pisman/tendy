from app.config import Settings, get_config, set_settings


def test_get_config_cached() -> None:
    # Clear the cache
    get_config.cache_clear()

    # Retrieve the settings
    s1 = get_config()

    # Modify the settings
    set_settings(
        Settings(
            mongo_uri="mongodb://mongodb:27017",
            mongo_dbname="new_db",
            origins="https://example.com",
            host="0.0.0.0",
            port=9000,
            reload=True,
        )
    )

    # Retrieve the settings again
    s2 = get_config()

    # Ensure the settings are cached
    assert s1 is s2


def test_set_settings() -> None:
    # Clear the cache
    get_config.cache_clear()

    set_settings(
        Settings(
            mongo_uri="mongodb://mongodb:27017",
            mongo_dbname="new_db",
            origins="https://example.com",
            host="0.0.0.0",
            port=9000,
            reload=True,
        )
    )

    s = get_config()

    assert s.mongo_uri == "mongodb://mongodb:27017"
    assert s.mongo_dbname == "new_db"
    assert s.origins == "https://example.com"
    assert s.host == "0.0.0.0"
    assert s.port == 9000
    assert s.reload is True
