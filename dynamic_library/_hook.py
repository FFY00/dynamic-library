# SPDX-FileCopyrightText: 2025-present Filipe Laíns <lains@riseup.net>
# SPDX-FileCopyrightText: 2025 Quansight, LLC
#
# SPDX-License-Identifier: MIT

import ctypes
import os

import dynamic_library


if os.environ.get('PYTHON_DYNAMIC_LIBRARY_DISABLE'):
    import warnings

    warnings.warn('Libraries registered via dynamic_library entrypoints will not be loaded!', RuntimeWarning)
else:
    for lib in dynamic_library.get_libraries():
        ctypes.CDLL(lib, ctypes.RTLD_GLOBAL)
