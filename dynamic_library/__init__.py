# SPDX-FileCopyrightText: 2025 Filipe Laíns <lains@riseup.net>
# SPDX-FileCopyrightText: 2025 Quansight, LLC
#
# SPDX-License-Identifier: MIT

import operator
import os
import pathlib
import sys
import sysconfig
import warnings

from collections.abc import Sequence

import dynamic_library._import


if sys.version_info >= (3, 10):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata


__version__ = '0.1.1'


_EXT = '.dll' if os.name == 'nt' else sysconfig.get_config_var('SHLIB_SUFFIX')


def _get_module_path(name: str) -> list[str]:
    module = dynamic_library._import.import_module_no_exec(name)
    if not hasattr(module, '__path__'):
        raise ValueError(f"{module} isn't a package")
    return module.__path__


def _find_library(entrypoint: importlib_metadata.EntryPoint) -> str | None:
    found = []
    for path in _get_module_path(entrypoint.value):
        lib = pathlib.Path(path, f'lib{entrypoint.name}{_EXT}')
        if lib.exists():
            found.append(lib)
    if len(found) > 1:
        warnings.warn(
            f'Multiple candidates found for library {entrypoint.name!r}: '
            + ', '.join(os.path(candidate) for candidate in found),
            stacklevel=2,
        )
        return
    if len(found) == 0:
        warnings.warn(f"Didn't find object file for library {entrypoint.name!r}", stacklevel=2)
        return
    return found[0]


def get_libraries() -> Sequence[pathlib.Path]:
    entrypoints = importlib_metadata.entry_points(group='dynamic_library')
    sorted_entrypoints = sorted(entrypoints, key=operator.attrgetter('name'))
    return list(filter(None, map(_find_library, sorted_entrypoints)))
