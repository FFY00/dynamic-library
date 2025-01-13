import os
import subprocess

import pytest

import environment_helpers.build


def test_header_only_library(env, tmp_path, packages, monkeypatch):
    env.install(['pkgconf'])

    # Install library package
    wheel = environment_helpers.build.build_wheel(packages / 'register-library', tmp_path, isolated=False)
    env.install_wheel(wheel)

    # Build and install consumer package
    wheel = environment_helpers.build.build_wheel(packages / 'uses-library', tmp_path, isolated=False)
    env.install_wheel(wheel)

    # Remove rpath, as meson insists on setting it
    uses_library_path = os.path.join(env.scheme['platlib'], 'uses_library.cpython-313-x86_64-linux-gnu.so')
    subprocess.check_call(['patchelf', '--remove-rpath', uses_library_path])

    # Make sure uses_library.foo() works
    assert env.introspectable.call('uses_library.foo', 1, 2) == 3
    # Make sure it doesn't work when we disable the hook (sanity check)
    monkeypatch.setenv('PYTHON_DYNAMIC_LIBRARY_DISABLE', 'true')
    with pytest.raises(subprocess.CalledProcessError):
        assert env.introspectable.call('uses_library.foo', 1, 2) == 3
