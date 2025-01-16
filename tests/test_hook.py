import os
import subprocess
import sys
import sysconfig

import pytest

import environment_helpers.build

import dynamic_library


def test_extension_with_dependency(env, tmp_path, packages, monkeypatch):
    env.install(['pkgconf'])

    # Install library package
    wheel = environment_helpers.build.build_wheel(packages / 'register-library', tmp_path, isolated=False)
    env.install_wheel(wheel)

    # Build and install consumer package
    wheel = environment_helpers.build.build_wheel(packages / 'uses-library', tmp_path, isolated=False)
    env.install_wheel(wheel)

    # Remove rpath, as meson insists on setting it
    libfoo_path = os.path.join(env.scheme['platlib'], 'register_library', 'libfoo' + dynamic_library._EXT)
    uses_library_path = os.path.join(env.scheme['platlib'], 'uses_library' + sysconfig.get_config_var('EXT_SUFFIX'))
    if sys.platform == 'linux':
        subprocess.check_call(['patchelf', '--remove-rpath', uses_library_path])
    elif sys.platform == 'darwin':
        subprocess.check_call(['install_name_tool', '-id', 'libfoo.dylib', libfoo_path])
        subprocess.check_call(['install_name_tool', '-change', '@rpath/libfoo.dylib', 'libfoo.dylib', uses_library_path])

    # Make sure uses_library.foo() works
    assert env.introspectable.call('uses_library.foo', 1, 2) == 3
    # Make sure it doesn't work when we disable the hook (sanity check)
    monkeypatch.setenv('PYTHON_DYNAMIC_LIBRARY_DISABLE', 'true')
    with pytest.raises(subprocess.CalledProcessError):
        assert env.introspectable.call('uses_library.foo', 1, 2) == 3
