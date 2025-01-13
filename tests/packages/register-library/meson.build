project('register-library', 'c', version: '1.0.0')

py = import('python').find_installation(pure: false)

library(
    'foo', 'foo.c',
    install: true,
    install_dir: py.get_install_dir() / 'register_library',
)
py.install_sources(['foo.h'], subdir: 'register_library/include')
py.install_sources(['foo.pc'], subdir: 'register_library')
