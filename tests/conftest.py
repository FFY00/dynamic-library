import os
import pathlib

import environment_helpers
import environment_helpers.build
import pytest


ROOT = pathlib.Path(__file__).parent.parent


@pytest.fixture
def root():
    return ROOT


@pytest.fixture
def packages():
    return ROOT / 'tests' / 'packages'


@pytest.fixture(scope='session')
def self_wheel(tmp_path_factory):
    tmpdir = tmp_path_factory.mktemp('wheel')
    return environment_helpers.build.build_wheel(ROOT, tmpdir)


@pytest.fixture
def env(tmpdir, self_wheel, monkeypatch):
    """Make a virtual environment with our project installed."""
    env = environment_helpers.create_venv(tmpdir)
    env.install_wheel(self_wheel)
    for key, value in env.env.items():
        monkeypatch.setenv(key, value)
    return env
