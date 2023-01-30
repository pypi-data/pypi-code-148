from setuptools import setup, Extension

ext = Extension(
        name='ioturing_applesmc',
        sources=['module/smc.c', 'module/smc-wrapper.c'],
        extra_link_args=['-framework', 'IOKit'],
    )

setup_args = dict(
    name='IoTuring_applesmc',
    version="v2023.1.3",
    ext_modules=[ext],
)

setup(**setup_args)