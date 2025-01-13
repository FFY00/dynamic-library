project('uses-library', 'c', version: '1.0.0')

libfoo = dependency('foo')

py = import('python').find_installation(pure: false)
py.extension_module(
    'uses_library', 'uses_library.c',
    dependencies: libfoo,
    install: true,
    install_rpath: '',
)
