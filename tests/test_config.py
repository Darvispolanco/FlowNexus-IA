import importlib

import pytest


def test_config_has_project_directories():
    from src import config

    assert config.BASE_DIR.exists()
    assert config.WORKSPACE_DIR.exists()
    assert config.MEMORY_DIR.exists()


def test_config_has_default_values():
    from src import config

    assert config.FLOWNEXUS_NAME
    assert config.FLOWNEXUS_ENV
    assert config.OPENAI_MODEL
    assert config.MAX_SEARCH_RESULTS > 0
    assert config.REQUEST_TIMEOUT > 0


def test_memory_file_is_inside_memory_directory():
    from src import config

    assert (
        config.MEMORY_DIR
        in config.MEMORY_FILE.parents
    )


def test_validate_config_requires_api_key(monkeypatch):
    from src import config

    monkeypatch.setattr(
        config,
        "OPENAI_API_KEY",
        None
    )

    with pytest.raises(ValueError):
        config.validate_config()


def test_validate_config_requires_model(monkeypatch):
    from src import config

    monkeypatch.setattr(
        config,
        "OPENAI_API_KEY",
        "test-api-key"
    )

    monkeypatch.setattr(
        config,
        "OPENAI_MODEL",
        ""
    )

    with pytest.raises(ValueError):
        config.validate_config()


def test_validate_config_accepts_valid_configuration(
    monkeypatch
):
    from src import config

    monkeypatch.setattr(
        config,
        "OPENAI_API_KEY",
        "test-api-key"
    )

    monkeypatch.setattr(
        config,
        "OPENAI_MODEL",
        "test-model"
    )

    config.validate_config()


def test_environment_can_be_reloaded(monkeypatch):
    monkeypatch.setenv(
        "FLOWNEXUS_NAME",
        "TestFlowNexus"
    )

    import src.config as config

    importlib.reload(config)

    assert config.FLOWNEXUS_NAME == "TestFlowNexus"
